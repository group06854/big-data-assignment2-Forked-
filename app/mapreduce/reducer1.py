import sys

current = None
tf_sum = 0
dl = 0

for line in sys.stdin:
    term, doc_id, tf, doc_len, title = line.strip().split('\t')
    key = (term, doc_id)

    if current and key != current:
        print(f"{current[0]}\t{current[1]}\t{tf_sum}\t{dl}\t{title}")
        tf_sum = 0

    current = key
    tf_sum += int(tf)
    dl = int(doc_len)

if current:
    print(f"{current[0]}\t{current[1]}\t{tf_sum}\t{dl}\t{title}")