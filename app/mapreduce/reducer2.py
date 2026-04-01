import sys

current_term = None
buffer = []

total_docs = 0
total_len = 0

def flush(term, buf):
    if not term or not buf:
        return
    df = len(buf)
    print(f"VOCAB\t{term}\t{df}")
    for doc, tf, dl, title in buf:
        print(f"POST\t{term}\t{doc}\t{tf}\t{dl}\t{title}\t{df}")


for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split()
    if len(parts) < 5:
        continue
    try:
        term = parts[0]
        doc = parts[1]
        tf = int(parts[2])
        dl = int(parts[3])
        title = " ".join(parts[4:])
    except:
        continue

    total_docs += 1
    total_len += dl
    if current_term and term != current_term:
        flush(current_term, buffer)
        buffer = []

    current_term = term
    buffer.append((doc, tf, dl, title))
if current_term:
    flush(current_term, buffer)
if total_docs > 0:
    avgdl = total_len / total_docs
    print(f"STATS\tN\t{total_docs}")
    print(f"STATS\tavgdl\t{avgdl}")