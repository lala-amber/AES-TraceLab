from typing import List, Dict

Rcon = [0x00, 0x01, 0x02, 0x04, 0x08,
        0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]

def gf_mul(a, b):
    result = 0
    for _ in range(8):
        if b & 1:
            result ^= a
        hi = a & 0x80
        a = (a << 1) & 0xFF
        if hi:
            a ^= 0x1B
        b >>= 1
    return result

def generate_sbox():
    def gf_inv(a):
        if a == 0:
            return 0
        for i in range(1, 256):
            if gf_mul(a, i) == 1:
                return i
        return 0

    def affine_transform(byte):
        result = 0
        for i in range(8):
            bit = (
                (byte >> i) & 1 ^
                (byte >> ((i + 4) % 8)) & 1 ^
                (byte >> ((i + 5) % 8)) & 1 ^
                (byte >> ((i + 6) % 8)) & 1 ^
                (byte >> ((i + 7) % 8)) & 1 ^
                (0x63 >> i) & 1
            )
            result |= (bit << i)
        return result

    return [affine_transform(gf_inv(i)) for i in range(256)]

def rot_word(word):
    return word[1:] + word[:1]

def sub_word(word, sbox):
    return [sbox[b] for b in word]

def key_expansion(key: List[int]) -> List[List[int]]:
    sbox = generate_sbox()
    Nk = 4
    Nr = 10
    Nb = 4
    key_schedule = [list(key[i:i+4]) for i in range(0, 16, 4)]

    for i in range(Nk, Nb * (Nr + 1)):
        temp = key_schedule[i - 1][:]
        if i % Nk == 0:
            temp = sub_word(rot_word(temp), sbox)
            temp[0] ^= Rcon[i // Nk]
        word = [a ^ b for a, b in zip(key_schedule[i - Nk], temp)]
        key_schedule.append(word)

    round_keys = [sum(key_schedule[i:i+4], []) for i in range(0, len(key_schedule), 4)]
    return round_keys

def bytes_to_state(bytes_block: List[int]) -> List[List[int]]:
    return [[bytes_block[r + 4 * c] for r in range(4)] for c in range(4)]

def state_to_bytes(state: List[List[int]]) -> List[int]:
    return [state[r][c] for c in range(4) for r in range(4)]

def sub_bytes(state, sbox):
    return [[sbox[b] for b in col] for col in state]

def shift_rows(state):
    new_state = [list(col) for col in state]
    for r in range(4):
        row = [state[c][r] for c in range(4)]
        row = row[r:] + row[:r]
        for c in range(4):
            new_state[c][r] = row[c]
    return new_state

def mix_columns(state):
    new_state = []
    for col in state:
        a0, a1, a2, a3 = col
        new_col = [
            gf_mul(a0, 2) ^ gf_mul(a1, 3) ^ a2 ^ a3,
            a0 ^ gf_mul(a1, 2) ^ gf_mul(a2, 3) ^ a3,
            a0 ^ a1 ^ gf_mul(a2, 2) ^ gf_mul(a3, 3),
            gf_mul(a0, 3) ^ a1 ^ a2 ^ gf_mul(a3, 2),
        ]
        new_state.append(new_col)
    return new_state

def add_round_key(state, round_key):
    return [[b ^ round_key[i * 4 + j] for j, b in enumerate(col)] for i, col in enumerate(state)]

def flatten_state(state: List[List[int]]) -> List[str]:
    return [f"{state[c][r]:02x}" for r in range(4) for c in range(4)]

def flatten_state(state: List[List[int]]) -> List[str]:
    """将 4x4 矩阵的列主序 state 扁平为 16 个十六进制字符串（用于前端渲染）"""
    return [f"{state[c][r]:02x}" for r in range(4) for c in range(4)]

def aes_encrypt_with_trace(plaintext: List[int], key: List[int]) -> Dict:
    sbox = generate_sbox()
    round_keys = key_expansion(key)
    state = bytes_to_state(plaintext)

    trace = []

    def capture(label, st, previous=None):
        flat = flatten_state(st)
        changed = []
        if previous:
            prev_flat = flatten_state(previous)
            changed = [i for i in range(16) if flat[i] != prev_flat[i]]
        trace.append({
            "step": label,
            "state": flat,
            "changed_bytes": changed
        })

    # 初始状态
    capture("Initial", state)

    # 初始轮密钥
    state = add_round_key(state, round_keys[0])
    capture("AddRoundKey 0", state)

    # 1~9轮加密
    for rnd in range(1, 10):
        prev = [col[:] for col in state]
        state = sub_bytes(state, sbox)
        capture(f"SubBytes {rnd}", state, prev)

        prev = [col[:] for col in state]
        state = shift_rows(state)
        capture(f"ShiftRows {rnd}", state, prev)

        prev = [col[:] for col in state]
        state = mix_columns(state)
        capture(f"MixColumns {rnd}", state, prev)

        prev = [col[:] for col in state]
        state = add_round_key(state, round_keys[rnd])
        capture(f"AddRoundKey {rnd}", state, prev)

    # 最后一轮（无 MixColumns）
    prev = [col[:] for col in state]
    state = sub_bytes(state, sbox)
    capture("SubBytes 10", state, prev)

    prev = [col[:] for col in state]
    state = shift_rows(state)
    capture("ShiftRows 10", state, prev)

    prev = [col[:] for col in state]
    state = add_round_key(state, round_keys[10])
    capture("AddRoundKey 10", state, prev)

    # 输出密文
    final_bytes = state_to_bytes(state)
    return {
        "ciphertext": "".join(f"{b:02x}" for b in final_bytes),
        "rounds": trace
    }



def generate_inv_sbox(sbox: List[int]) -> List[int]:
    inv = [0] * 256
    for i, val in enumerate(sbox):
        inv[val] = i
    return inv
