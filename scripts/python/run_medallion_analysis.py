#!/usr/bin/env python
# Mineral Export Analysis with Medallion Architecture

import os
import subprocess
import sys

def main():
    print("=== Mineral Export Analysis with Medallion Architecture ===")
    print("Starting analysis with bronze, silver, and gold layers...")
    
    # Create the analysis script
    script_content = """
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg, count, desc
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType

print('=== Initializing Spark Session ===')
spark = SparkSession.builder \\
    .appName('Mineral Export Analysis') \\
    .master('local[*]') \\
    .getOrCreate()

print('\\n=== BRONZE LAYER: Raw Data Ingestion ===')
# Read the CSV data
df = spark.read.format('csv') \\
    .option('header', 'true') \\
    .load('/tmp/ekspor_mineral_indonesia_WITS.csv')

print(f'Bronze layer loaded with {df.count()} records')
print('Sample data (Bronze layer):')
df.show(5)

print('\\n=== SILVER LAYER: Data Cleaning and Transformation ===')
# Convert column names for easier processing
df = df.toDF(*[c.replace(' ', '_') for c in df.columns])
print('Columns after renaming:')
for column in df.columns:
    print(f'- {column}')

# Clean and transform data (Silver layer)
try:
    silver_df = df \\
        .filter(col('Reporter') == 'Indonesia') \\
        .filter(col('TradeFlow') == 'Export') \\
        .withColumn('TradeValueUSD', col('Trade_Value_1000USD') * 1000) \\
        .withColumn('QuantityKg', col('Quantity')) \\
        .withColumn('UnitPriceUSD', col('TradeValueUSD') / col('QuantityKg'))
    
    print(f'Silver layer created with {silver_df.count()} records')
    print('Sample silver data:')
    silver_df.show(5)
    
    print('\\n=== GOLD LAYER: Business Metrics and Aggregations ===')
    # Exports by Country (Gold layer)
    exports_by_country = silver_df.groupBy('Partner').agg(
        sum('TradeValueUSD').alias('TotalExportValueUSD'),
        sum('QuantityKg').alias('TotalExportQuantityKg'),
        avg('UnitPriceUSD').alias('AvgUnitPriceUSD')
    ).orderBy(desc('TotalExportValueUSD'))
    
    print('Gold layer - Exports by Country:')
    exports_by_country.show(10)
    
    # Exports by Product (Gold layer)
    exports_by_product = silver_df.groupBy('ProductCode', 'Product_Description').agg(
        sum('TradeValueUSD').alias('TotalExportValueUSD'),
        sum('QuantityKg').alias('TotalExportQuantityKg'),
        count('Partner').alias('NumberOfCountriesExportedTo')
    ).orderBy(desc('TotalExportValueUSD'))
    
    print('Gold layer - Exports by Product:')
    exports_by_product.show(10)
except Exception as e:
    print(f'Error in processing: {e}')

print('\\n=== Analysis Complete ===')
spark.stop()
"""
    
    # Write the script to a temporary file
    script_path = "analyze_minerals_temp.py"
    with open(script_path, "w") as f:
        f.write(script_content)
    
    try:
        # Copy CSV file to container
        subprocess.run(["docker", "cp", "ekspor_mineral_indonesia_WITS.csv", "spark-master:/tmp/"], check=True)
        
        # Copy script to container
        subprocess.run(["docker", "cp", script_path, "spark-master:/tmp/analyze_minerals.py"], check=True)
        
        # Run the script in the container
        subprocess.run(["docker", "exec", "-t", "spark-master", "python", "/tmp/analyze_minerals.py"], check=True)
        
        print("Analysis completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error running analysis: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        # Clean up temporary file
        if os.path.exists(script_path):
            os.remove(script_path)
            
if __name__ == "__main__":
    main()
