# PassHunter

A targeted **password-candidate (wordlist) generator** written in pure Python.

Given a handful of seed words gathered during OSINT profiling (a name, a pet, a
company, a hobby), PassHunter expands them into a large, prioritized wordlist by
combining **casing**, **leet-speak substitutions**, **years**, and **numeric /
special-character suffixes** — modeling the way real people actually build
passwords.

The output is a plain `pass.txt` file, one candidate per line, ready to feed into
tools like `hashcat`, `john`, or `hydra` for authorized dictionary-based attacks.

> ⚠️ **Authorized use only.** PassHunter is intended for legitimate purposes:
> recovering your *own* forgotten passwords, authorized penetration testing and
> red-team engagements, security research, and CTF challenges. **Do not** use it
> against systems or accounts you do not own or lack explicit written permission
> to test. You are solely responsible for how you use it.

---

## Why it exists

During the profiling stage of an authorized red-team engagement, OSINT-gathered
details about a target rarely map to a password directly — but they *seed* one.
PassHunter turns those seeds into a prioritized candidate list that reflects
common, target-specific password habits (capitalizing the first letter, swapping
`a → @`, tacking on a birth year and a `!`), so the most probable guesses are
tried first.

---

## Features

- **Seed words** — start from any list of base words.
- **Casing variants** — lowercase and Capitalized forms of every word.
- **Multi-leet substitution** — generates *every* combination of leet-speak
  swaps: `a → @/4`, `e → 3`, `i → 1`, `o → 0`, `s → $/5`, `t → 7`, `z → 2`.
- **Prioritized generation** — the most likely patterns are written first, so you
  can start cracking before the full list finishes:
  1. Word + year with a special character
  2. Word + zero-padded 2-digit numbers (`00`–`99`) with a special
  3. Word + short single-digit numbers
  4. Word + longer numbers and special characters
- **De-duplication** — every candidate is emitted at most once.
- **Configurable cap** — stops cleanly after `MAX_PASSWORDS` candidates.
- **Zero dependencies** — standard library only.

---

## Requirements

- Python 3.6+
- No third-party dependencies

---

## Usage

1. Rename the script to `passhunter.py` so it's clearly a Python module and
   easy to run or import.

2. Edit the **input section** at the top of the script:

   ```python
   words    = ["jack", "familyjack", "family"]   # your seed words
   specials = ["!", "@", "#", "$", "_", "."]     # special chars to append
   YEAR_START    = 1970                           # first year to try
   YEAR_END      = 2026                           # last year to try
   MAX_PASSWORDS = 30_000_000                     # safety cap on output size
   OUTPUT_FILE   = "pass.txt"                     # where to write results
   ```

3. Run it:

   ```bash
   python passhunter.py
   ```

4. Collect your wordlist from `pass.txt`:

   ```
   [+] Generated 12345678 candidates → pass.txt
   ```

---

## Configuration reference

| Setting         | Description                                                       | Default       |
| --------------- | ---------------------------------------------------------------- | ------------- |
| `words`         | Seed words the wordlist is built from.                           | example names |
| `specials`      | Special characters appended/prepended to candidates.             | `! @ # $ _ .` |
| `YEAR_START`    | First year value used in year-based patterns.                    | `1970`        |
| `YEAR_END`      | Last year value used in year-based patterns.                     | `2026`        |
| `MAX_PASSWORDS` | Hard cap on the number of candidates generated.                  | `30_000_000`  |
| `OUTPUT_FILE`   | Path of the generated wordlist.                                  | `pass.txt`    |
| `LEET_MAP`      | Character → leet substitution table. Add/remove mappings freely. | see script    |

---

## How it works

Each seed word is walked through a short pipeline:

```
word ──▶ multi_leet() ──▶ casing() ──▶ suffix / number / special patterns ──▶ emit()
```

- **`multi_leet(word)`** returns the set of all leet variants (including the
  original) by expanding every substitutable character.
- **`casing(word)`** yields the lowercase and Capitalized forms.
- **`emit(pw, f)`** writes a candidate only if it hasn't been seen before, and
  increments the global counter.

Generation runs in four priority passes (see [Features](#features)). Once the
running total reaches `MAX_PASSWORDS`, generation stops early.

---

## Performance & size notes

- The full parameter space is **enormous**. Broad ranges (e.g. `YEAR_START=0`,
  `YEAR_END=9999`, plus the wide number pass) combined with many seed words and
  leet variants can produce **tens of millions** of lines and a multi-GB file.
- Keep `MAX_PASSWORDS` sane and narrow `YEAR_START`/`YEAR_END` to a realistic
  range (e.g. `1970`–`2026`) to keep the list focused and fast.
- The de-duplication `seen` set is held in memory; very large runs use
  significant RAM. For huge lists, consider streaming to disk and de-duplicating
  with `sort -u` afterward.

---

## License

No license file is currently included. Add one (e.g. MIT) if you intend to share
or open-source this project.
