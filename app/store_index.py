from cassandra.cluster import Cluster
import subprocess

def hdfs_cat(path):
    try:
        return subprocess.check_output(["hdfs", "dfs", "-cat", path]).decode()
    except subprocess.CalledProcessError:
        return ""

cluster = Cluster(['cassandra-server'])
session = cluster.connect()

session.execute("""
CREATE KEYSPACE IF NOT EXISTS search
WITH replication = {'class':'SimpleStrategy','replication_factor':1}
""")

session.set_keyspace("search")

session.execute("""
CREATE TABLE IF NOT EXISTS docs(
    doc_id text PRIMARY KEY,
    length int,
    title text
)
""")

session.execute("""
CREATE TABLE IF NOT EXISTS vocabulary(
    term text PRIMARY KEY,
    df int
)
""")

session.execute("""
CREATE TABLE IF NOT EXISTS postings(
    term text,
    doc_id text,
    tf int,
    dl int,
    PRIMARY KEY(term, doc_id)
)
""")

session.execute("""
CREATE TABLE IF NOT EXISTS stats(
    name text PRIMARY KEY,
    value double
)
""")

all_data_lines = []
dir_path = "/index/final"

try:
    ls_out = subprocess.check_output(["hdfs", "dfs", "-ls", dir_path]).decode()

    for line in ls_out.split('\n'):
        parts = line.split()
        if len(parts) >= 7 and 'part-' in parts[-1]:
            content = hdfs_cat(parts[-1])
            if content:
                lines = content.splitlines()
                all_data_lines.extend(lines)
                print("LINES:", len(all_data_lines))
except Exception as e:
    print("HDFS ERROR:", e)

for line in all_data_lines:
    parts = line.strip().split()

    if len(parts) < 2:
        continue

    try:
        if parts[0] == "VOCAB" and len(parts) >= 3:
            term = parts[1]
            df = int(parts[2])

            session.execute(
                "INSERT INTO vocabulary (term, df) VALUES (%s, %s)",
                (term, df)
            )

        elif parts[0] == "POST" and len(parts) >= 7:
            term = parts[1]
            doc = parts[2]
            tf = int(parts[3])
            dl = int(parts[4])
            title = parts[5]

            session.execute(
                "INSERT INTO postings (term, doc_id, tf, dl) VALUES (%s, %s, %s, %s)",
                (term, doc, tf, dl)
            )

            session.execute(
                "INSERT INTO docs (doc_id, length, title) VALUES (%s, %s, %s)",
                (doc, dl, title)
            )

        elif parts[0] == "STATS" and len(parts) >= 3:
            key = parts[1]
            val = float(parts[2])

            session.execute(
                "INSERT INTO stats (name, value) VALUES (%s, %s)",
                (key, val)
            )

    except Exception as e:
        print("BAD LINE:", line)
        print("ERROR:", e)

cluster.shutdown()