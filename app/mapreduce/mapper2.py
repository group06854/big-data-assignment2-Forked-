import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    parts = line.split()

    if len(parts) < 5:
        continue

    term = parts[0]
    doc = parts[1]
    tf = parts[2]
    dl = parts[3]
    title = " ".join(parts[4:])

    print(f"{term}\t{doc}\t{tf}\t{dl}\t{title}")