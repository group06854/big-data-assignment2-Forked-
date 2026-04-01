INPUT=/data
TMP1=/index/tmp1
TMP2=/index/tmp2
OUT=/index/final

hdfs dfs -rm -r -f /index || true

hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming*.jar \
 -D mapreduce.job.reduces=4 \
 -input ${INPUT}/*.txt \
 -output $TMP1 \
 -mapper "python3 mapper1.py" \
 -reducer "python3 reducer1.py" \
 -file /app/mapreduce/mapper1.py \
 -file /app/mapreduce/reducer1.py

hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming*.jar \
 -D mapreduce.job.reduces=1 \
 -input $TMP1 \
 -output $TMP2 \
 -mapper "python3 mapper2.py" \
 -reducer "python3 reducer2.py" \
 -file /app/mapreduce/mapper2.py \
 -file /app/mapreduce/reducer2.py

 hdfs dfs -mkdir -p $OUT
hdfs dfs -cp $TMP2/* $OUT/
hdfs dfs -rm -r $TMP1 $TMP2

echo "Create index using MapReduce pipelines"
