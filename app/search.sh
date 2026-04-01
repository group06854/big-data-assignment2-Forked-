echo "This script will include commands to search for documents given the query using Spark RDD"

QUERY="$1"

spark-submit \
  --master yarn \
  --deploy-mode client \
  --conf spark.yarn.appMasterEnv.PYSPARK_PYTHON=/usr/bin/python3 \
  --conf spark.executorEnv.PYSPARK_PYTHON=/usr/bin/python3 \
  --packages com.datastax.spark:spark-cassandra-connector_2.12:3.5.0 \
  query.py "artemis diesel"