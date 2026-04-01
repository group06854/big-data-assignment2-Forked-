from pyspark.sql import SparkSession
import sys, re, math

def tokenize(q):
    return re.sub(r'[^\w\s]', ' ', q.lower()).split()

def bm25(tf, df, dl, avgdl, N, k1=1.2, b=0.75):
    idf = math.log((N - df + 0.5) / (df + 0.5) + 1)
    return idf * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * dl / avgdl))

terms = tokenize(sys.argv[1])

spark = SparkSession.builder \
    .appName("search") \
    .config("spark.cassandra.connection.host", "cassandra-server") \
    .config("spark.jars.packages", "com.datastax.spark:spark-cassandra-connector_2.12:3.5.0") \
    .config("spark.cassandra.connection.localDC", "datacenter1")\
    .getOrCreate()

# читаем таблицы
postings = spark.read.format("org.apache.spark.sql.cassandra") \
    .options(table="postings", keyspace="search").load()

vocab = spark.read.format("org.apache.spark.sql.cassandra") \
    .options(table="vocabulary", keyspace="search").load()

docs = spark.read.format("org.apache.spark.sql.cassandra") \
    .options(table="docs", keyspace="search").load()

stats = spark.read.format("org.apache.spark.sql.cassandra") \
    .options(table="stats", keyspace="search").load()

stats_map = {row.name: row.value for row in stats.collect()}

N = int(stats_map.get("N", 1))
avgdl = float(stats_map.get("avgdl", 1))

df_rows = vocab.filter(vocab.term.isin(terms)).collect()
df_map = {row.term: row.df for row in df_rows}

scores = postings.filter(postings.term.isin(terms)).rdd \
    .map(lambda x: (
        x.doc_id,
        bm25(x.tf, df_map.get(x.term, 1), x.dl, avgdl, N)
    )) \
    .reduceByKey(lambda a, b: a + b)

top = scores.takeOrdered(10, key=lambda x: -x[1])

doc_ids = [doc for doc, _ in top]
doc_map = {
    row.doc_id: row.title
    for row in docs.filter(docs.doc_id.isin(doc_ids)).collect()
}

print("\nTop 10 results:")
for doc, score in top:
    print(f"{doc}: {doc_map.get(doc, 'Unknown')} ({round(score,4)})")

spark.stop()