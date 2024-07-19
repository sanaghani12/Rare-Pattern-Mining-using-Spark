from pyspark.sql import SparkSession
from pyspark.sql.functions import split, col, lit, concat_ws
from pyspark.sql.types import StructType, StructField, IntegerType, StringType
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
from pyspark.ml.fpm import FPGrowth
import time
from pyspark.sql.functions import udf
from pyspark.sql.types import DoubleType
from pyspark.ml.feature import MinHashLSH
from pyspark.ml.linalg import Vectors

# import findspark
# findspark.init()

os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

spark = SparkSession.builder \
    .appName("Your App Name") \
    .config("spark.driver.memory", "2g") \
    .config("spark.executor.memory", "2g") \
    .config("spark.driver.maxResultSize", "2g") \
    .config("spark.driver.bindAddress", "127.0.0.1") \
    .config("spark.driver.host", "127.0.0.1") \
    .getOrCreate()
# spark.sparkContext.setLogLevel("DEBUG")
# spark.sparkContext.setLogLevel("ERROR")
# Load data
data_path = "converted_heart_transactions.txt"

# Load data from TXT file
df = spark.read.text(data_path).toDF("items")

# Convert space-delimited string to array of integers
df = df.withColumn("items", split(col("items"), "\s+").cast("array<int>"))

min_support = 0.2

fpGrowth = FPGrowth(itemsCol="items", minSupport=0.2, minConfidence=0.6)
model = fpGrowth.fit(df)
total_count = df.count() 
start_time = time.time()
frequent = model.freqItemsets.withColumn("support", col("freq") / total_count)
print('Time to find frequent itemset')
print("--- %s seconds ---" % (time.time() - start_time))

# Display frequent itemsets
print("frequent itemsets: ")
# model.freqItemsets.show()

# Count the number of frequent itemsets
frequent_itemsets_count = model.freqItemsets.count()
print("Count of frequent itemsets:", frequent_itemsets_count)

# Assuming df is already defined and contains itemset data with a "freq" column
total_count = df.count()  # It's more efficient to call count() once and reuse the result
print("total count: ",total_count)

# Calculate the relative support for each itemset
frequent_itemsets = model.freqItemsets.withColumn("support", col("freq") / total_count)

# Define the clusters based on support ranges
rare_cluster = frequent_itemsets.filter((col("support") > 0.2) & (col("support") < 0.5)).withColumn("cluster", lit("rare"))
common_cluster = frequent_itemsets.filter(col("support") > 0.5).withColumn("cluster", lit("common"))

# rare_cluster.show()

# common_cluster.show()

print("generated association rules: ")
# Display generated association rules
# model.associationRules.show()

## Filter association rules for rare cluster
print("Association Rules for Rare Cluster:")
rare_cluster_rules = model.associationRules.filter((col("support") > 0.2) & (col("support") < 0.5))
rare_cluster_rules.show()

## Filter association rules for common cluster
print("Association Rules for Common Cluster:")
common_cluster_rules = model.associationRules.filter(col("support") > 0.5)
# common_cluster_rules.show()

def jaccard_similarity(list1, list2):
    intersection = set(list1).intersection(set(list2))
    union = set(list1).union(set(list2))
    return float(len(intersection)) / float(len(union))

# Register UDF
jaccard_udf = udf(jaccard_similarity, DoubleType())

# Cross join the dataframes
cross_joined_df = rare_cluster_rules.crossJoin(common_cluster_rules.withColumnRenamed("antecedent", "antecedents2").withColumnRenamed("consequent", "consequents2").withColumnRenamed("confidence", "confidence2").withColumnRenamed("lift", "lift2").withColumnRenamed("support", "support2"))

# Filter for similarity and different consequents
similar_rules_df = cross_joined_df.withColumn(
    "similarity",
    jaccard_udf("antecedent", "antecedents2")
).filter(
    (col("similarity") >= 0.8) & (col("consequent") != col("consequents2"))
)

# Show results
print("Interesting Rules (Similar Antecedents, Different Consequents):")
# Check if the column 'confidence' exists and rename it
# if 'confidence' in similar_rules_df.columns:
#     # Renaming the existing 'confidence' column to 'confidence_old'
#     similar_rules_df = similar_rules_df.withColumnRenamed('confidence', 'confidence_1')
# Convert array to string
similar_rules_df = similar_rules_df.withColumn("antecedent", concat_ws(",", col("antecedent"))).withColumn("consequent", concat_ws(",", col("consequent"))).withColumn("antecedents2", concat_ws(",", col("antecedents2"))).withColumn("consequents2", concat_ws(",", col("consequents2")))

#write to CSV
similar_rules_df.write.csv("similar_rules.csv", header=True, mode="overwrite")

similar_rules_df.show(100, truncate=False)
