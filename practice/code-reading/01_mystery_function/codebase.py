def transform(text, key):
    result = []
    for ch in text:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            shifted = (ord(ch) - base + key) % 26
            result.append(chr(base + shifted))
        else:
            result.append(ch)
    return "".join(result)


def analyze(text):
    counts = {}
    total = 0
    for ch in text.lower():
        if ch.isalpha():
            counts[ch] = counts.get(ch, 0) + 1
            total += 1
    return {ch: round(count / total, 4) for ch, count in counts.items()} if total else {}


REFERENCE = {
    "e": 0.127, "t": 0.091, "a": 0.082, "o": 0.075, "i": 0.070,
    "n": 0.067, "s": 0.063, "h": 0.061, "r": 0.060, "d": 0.043,
}


def score(freq):
    total = 0.0
    for ch, expected in REFERENCE.items():
        actual = freq.get(ch, 0)
        total += (actual - expected) ** 2
    return total


def solve(ciphertext):
    best_key = 0
    best_score = float("inf")
    for candidate in range(26):
        decrypted = transform(ciphertext, candidate)
        freq = analyze(decrypted)
        s = score(freq)
        if s < best_score:
            best_score = s
            best_key = candidate
    return best_key, transform(ciphertext, best_key)
