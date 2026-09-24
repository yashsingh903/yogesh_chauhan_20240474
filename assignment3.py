"""Assignment 3: Spark program - number of products sold in each category.
Install: pip install pyspark
Input CSV columns: OrderID,Product,Category,Quantity,Price   (header row)
Usage:   python assignment3_pyspark_sales.py sales.csv
If no file is given, a small sample dataset is used.
"""
import sys
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("SalesByCategory").master("local[*]").getOrCreate()

if len(sys.argv) > 1:
    sales = spark.read.csv(sys.argv[1], header=True, inferSchema=True)
else:
    sales = spark.createDataFrame([
        (1, "Laptop", "Electronics", 2, 55000.0),
        (2, "Phone", "Electronics", 3, 20000.0),
        (3, "T-Shirt", "Clothing", 5, 500.0),
        (4, "Jeans", "Clothing", 2, 1500.0),
        (5, "Rice 5kg", "Grocery", 10, 400.0),
        (6, "Novel", "Books", 4, 300.0),
        (7, "Phone", "Electronics", 1, 20000.0),
    ], ["OrderID", "Product", "Category", "Quantity", "Price"])

result = (sales.groupBy("Category")
               .agg(F.sum("Quantity").alias("Units_Sold"),
                    F.countDistinct("Product").alias("Distinct_Products"))
               .orderBy(F.desc("Units_Sold")))
result.show()

# RDD version (map -> reduceByKey)
rdd = (sales.rdd.map(lambda r: (r["Category"], r["Quantity"]))
                .reduceByKey(lambda a, b: a + b))
print(rdd.collect())
spark.stop()
