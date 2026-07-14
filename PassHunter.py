# =========================
# INPUT SECTION
# =========================

words = ["jack", "familyjack", "family"]
specials = ["!", "@", "#", "$", "_", "."]

YEAR_START = 0000
YEAR_END = 9999
MAX_PASSWORDS = 30_000_000
OUTPUT_FILE = "pass.txt"


# =========================
# LEET MAP
# =========================

LEET_MAP = {
    "a": ["@", "4"],
    "e": ["3"],
    "i": ["1"],
    "o": ["0"],
    "s": ["$", "5"],
    "t": ["7"],
    "z": ["2"],
}


# =========================
# ENGINE
# =========================

count = 0
seen = set()


def emit(pw, f):
    global count
    if pw not in seen:
        f.write(pw + "\n")
        seen.add(pw)
        count += 1


def casing(word):
    return [
        word.lower(),
        word.capitalize()
    ]


def multi_leet(word):
    """Generate variants with ANY number of leet substitutions"""
    out = {word}

    for i, c in enumerate(word):
        if c.lower() in LEET_MAP:
            new = set()
            for base in out:
                for r in LEET_MAP[c.lower()]:
                    new.add(base[:i] + r + base[i + 1:])
            out |= new

    return out


# =========================
# GENERATION (ORDERED)
# =========================

with open(OUTPUT_FILE, "w") as f:

    # 🔥 Priority 1 — Year patterns (WITH LEET)
    for w in words:
        for leet in multi_leet(w):
            for c in casing(leet):
                for y in range(YEAR_START, YEAR_END + 1):
                    for s in specials:
                        emit(c + s + str(y), f)
                        emit(c + str(y) + s, f)

    # 🔥 Priority 2 — Zero-padded numbers
    for w in words:
        for leet in multi_leet(w):
            for c in casing(leet):
                for n in range(100):
                    num = str(n).zfill(2)
                    for s in specials:
                        emit(c + num + s, f)
                        emit(c + s + num, f)

    # 🔥 Priority 3 — Short numbers ✅ THIS FIXES YOUR CASE
    for w in words:
        for leet in multi_leet(w):
            for c in casing(leet):
                for n in range(10):
                    emit(c + str(n), f)
                    for s in specials:
                        emit(c + s + str(n), f)
                        emit(c + str(n) + s, f)

    # 🔥 Priority 4 — Leet + numbers + specials (unchanged spirit)
    for w in words:
        for leet in multi_leet(w):
            for c in casing(leet):

                emit(c, f)

                for n in range(10000):
                    num = str(n)

                    emit(c + num, f)
                    emit(num + c, f)

                    for s in specials:
                        emit(c + num + s, f)
                        emit(c + s + num, f)

                    if count >= MAX_PASSWORDS:
                        break

                if count >= MAX_PASSWORDS:
                    break

            if count >= MAX_PASSWORDS:
                break


print(f"[+] Generated {count} passwords → {OUTPUT_FILE}")
