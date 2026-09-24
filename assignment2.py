"""Assignment 2: MapReduce - number of students in each grade (S,A,B,C,D,E,F).
Works on one or many grade-sheet .txt files (one per subject).
Usage: python assignment2_mapreduce_grades.py CD204A1-1.txt [other_subject.txt ...]
"""
import re, sys
from collections import defaultdict
from functools import reduce

GRADES = ["S", "A", "B", "C", "D", "E", "F"]
ROW = re.compile(r"^\s*(\d{9})\s+\S+\s+\S+\s+\S+\s+([A-Z]+)\s*$")

def read_subject(path):
    """Return (subject_code, list_of_lines)."""
    lines = open(path, encoding="utf-8", errors="ignore").read().splitlines()
    code = path
    for l in lines:
        m = re.search(r"Subject Title\s*:\s*(.+)", l)
        if m:
            code = m.group(1).strip()
            break
    return code, lines

# ---------- MAP: each record -> ((subject, grade), 1) ----------
def mapper(subject, line):
    m = ROW.match(line)
    if m:
        yield (subject, m.group(2)), 1

# ---------- SHUFFLE: group values by key ----------
def shuffle(pairs):
    groups = defaultdict(list)
    for k, v in pairs:
        groups[k].append(v)
    return groups

# ---------- REDUCE: sum the 1s for each key ----------
def reducer(key, values):
    return key, reduce(lambda a, b: a + b, values)

def main(files):
    pairs = []
    for f in files:
        subject, lines = read_subject(f)
        for line in lines:
            pairs.extend(mapper(subject, line))
    reduced = dict(reducer(k, v) for k, v in shuffle(pairs).items())

    subjects = sorted({s for s, _ in reduced})
    for s in subjects:
        print(f"\n{s}")
        print("Grade  Students")
        for g in GRADES:
            print(f"  {g}      {reduced.get((s, g), 0)}")
        others = {g: c for (sub, g), c in reduced.items()
                  if sub == s and g not in GRADES}
        for g, c in sorted(others.items()):
            label = {"I": "Absent (I)", "DT": "Detained (DT)"}.get(g, g)
            print(f"  {label}: {c}")

if __name__ == "__main__":
    main(sys.argv[1:] or ["/mnt/user-data/uploads/CD204A1-1.txt"])
