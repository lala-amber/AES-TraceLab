from flask import Flask, request, jsonify, send_file, render_template
from sbox_core import aes_encrypt_with_trace, generate_sbox, generate_inv_sbox
from io import BytesIO
import csv
from flask import request
import ipaddress
from datetime import datetime
from time import time

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/sbox_outputs")
def list_sbox_outputs():
    outputs = sorted(set(sbox))
    return jsonify([f"0x{v:02x}" for v in outputs])
@app.route("/aes_full_rounds", methods=["POST"])
def aes_full_rounds():
    data = request.get_json()
    block = data.get("block", [])
    key = data.get("key", [])
    if len(block) != 16 or len(key) != 16:
        return jsonify({"error": "明文和密钥必须是 16 字节"}), 400

    try:
        trace = aes_encrypt_with_trace(block, key)
        return jsonify(trace)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ======== S-box 初始化 ========
def format_matrix(lst):
    return [[f"{lst[r*16 + c]:02x}" for c in range(16)] for r in range(16)]

sbox = generate_sbox()
inv_sbox = generate_inv_sbox(sbox)

sbox_matrix = format_matrix(sbox)
inv_sbox_matrix = format_matrix(inv_sbox)

@app.route("/tables")
def get_tables():
    return jsonify({
        "sbox": sbox_matrix,
        "inv_sbox": inv_sbox_matrix
    })

# ======== 实时访客记录（缓存去重） ========
visit_records = []
ip_set = set()
visit_cache = {}  # (ip, ua) -> last_time

@app.before_request
def log_visitor():
    forwarded = request.headers.get("X-Forwarded-For", "")
    ip = forwarded.split(",")[0].strip() if forwarded else request.remote_addr

    ua = request.user_agent.string
    now = time()
    key = (ip, ua)
    cooldown = 60

    if key in visit_cache and now - visit_cache[key] < cooldown:
        return

    visit_cache[key] = now

    try:
        is_private = ipaddress.ip_address(ip).is_private
        ip_type = "🏠内网" if is_private else "🌐公网"
    except ValueError:
        ip_type = "❓未知"

    try:
        geo = requests.get(f"http://ip-api.com/json/{ip}").json()
        loc = f"{geo.get('country', '')} - {geo.get('city', '')}"
    except:
        loc = "未知"

    # ✅ 添加访问时间
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    visit_records.append({
        "ip": ip,
        "type": ip_type,
        "loc": loc,
        "ua": ua,
        "ts": timestamp
    })
    ip_set.add(ip)

    if len(visit_records) > 100:
        visit_records[:] = visit_records[-100:]

@app.route("/visitors")
def visitors():
    return jsonify({
        "count": len(visit_records),
        "ip_count": len(ip_set),
        "list": visit_records[-30:]
    })


# ======== 逆 S-box 查找 ========
@app.route("/reverse_sbox", methods=["POST"])
def reverse_sbox():
    data = request.get_json()
    value = data.get("value", "").lower().replace("0x", "")
    try:
        target = int(value, 16)
    except:
        return jsonify({"error": "Invalid hex input"}), 400

    result = [i for i, v in enumerate(sbox) if v == target]
    return jsonify({
        "value": value,
        "matches": [f"0x{i:02x}" for i in result]
    })

# ======== AES 加密过程可视化 ========
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    values = data.get("values", [])
    try:
        result = []
        for v in values:
            sbox_val = sbox[v]
            xor_val = v ^ sbox_val
            hamming = bin(xor_val).count("1")
            result.append({
                "input": f"0x{v:02x}",
                "input_bin": f"{v:08b}",
                "sbox": f"0x{sbox_val:02x}",
                "sbox_bin": f"{sbox_val:08b}",
                "xor": f"{xor_val:02x}",
                "hamming": hamming,
                "check": "✔️" if v == inv_sbox[sbox_val] else "❌"
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ======== 状态导出接口 ========
from io import StringIO

@app.route("/export", methods=["POST"])
def export_csv():
    data = request.get_json()
    csv_str = StringIO()
    writer = csv.writer(csv_str)

    try:
        for round_data in data.get("rounds", []):
            writer.writerow(["Round", round_data.get("round", "")])
            for row in round_data.get("state", []):
                writer.writerow(row)
            writer.writerow([])

        # 转成字节流给 send_file
        output = BytesIO()
        output.write(csv_str.getvalue().encode("utf-8"))
        output.seek(0)

        return send_file(output, mimetype="text/csv", as_attachment=True, download_name="aes_rounds.csv")

    except Exception as e:
        return jsonify({"error": f"导出失败: {str(e)}"}), 500
# ======== 启动服务 ========
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
