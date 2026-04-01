import sys
import re
import os

def tokenize(text):
    return re.sub(r'[^\w\s]', ' ', text.lower()).split()

filename = os.environ.get('mapreduce_map_input_file', '')
base = os.path.basename(filename).replace('.txt', '')

parts = base.split('_', 1)
if len(parts) != 2:
    sys.exit(0)

doc_id = parts[0]
title = parts[1]

for line in sys.stdin:
    tokens = tokenize(line)

    tf = {}
    for t in tokens:
        tf[t] = tf.get(t, 0) + 1

    dl = len(tokens)

    for term, f in tf.items():
        print(f"{term}\t{doc_id}\t{f}\t{dl}\t{title}")