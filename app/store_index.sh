echo "[store_index] START"

echo "[store_index] Reading index from HDFS"
hdfs dfs -cat /index/final/part-* > /tmp/index.txt

echo "[store_index] Preview index"
head -n 10 /tmp/index.txt

echo "[store_index] Running Python loader"
python3 /app/store_index.py

echo "[store_index] DONE"