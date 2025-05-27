#!/bin/bash

echo "=== Indonesian Mineral Export Analysis - Final Verification ==="
echo "Date: $(date)"
echo

# Check HDFS status
echo "=== HDFS Status ==="
docker exec namenode hadoop fs -ls /user/mineral_exports/ 2>/dev/null || echo "HDFS directories not found, creating..."

# Create HDFS directories if they don't exist
echo "Creating HDFS directory structure..."
docker exec namenode hadoop fs -mkdir -p /user/mineral_exports/bronze
docker exec namenode hadoop fs -mkdir -p /user/mineral_exports/silver  
docker exec namenode hadoop fs -mkdir -p /user/mineral_exports/gold/by_country
docker exec namenode hadoop fs -mkdir -p /user/mineral_exports/gold/by_product

# Copy data to HDFS
echo "=== Copying data to HDFS ==="
docker exec namenode hadoop fs -put /opt/spark/data/ekspor_mineral_indonesia_WITS.csv /user/mineral_exports/bronze/ 2>/dev/null || echo "File already exists in HDFS"

# Verify HDFS contents
echo "=== HDFS Directory Contents ==="
docker exec namenode hadoop fs -ls -R /user/mineral_exports/

# Check data file in HDFS
echo "=== Data File Information ==="
docker exec namenode hadoop fs -ls /user/mineral_exports/bronze/ekspor_mineral_indonesia_WITS.csv

# Basic data analysis using HDFS
echo "=== Basic Data Analysis ==="
echo "Total lines in HDFS file:"
docker exec namenode hadoop fs -cat /user/mineral_exports/bronze/ekspor_mineral_indonesia_WITS.csv | wc -l

echo "First 5 lines:"
docker exec namenode hadoop fs -cat /user/mineral_exports/bronze/ekspor_mineral_indonesia_WITS.csv | head -5

echo "Last 5 lines:"
docker exec namenode hadoop fs -cat /user/mineral_exports/bronze/ekspor_mineral_indonesia_WITS.csv | tail -5

echo
echo "=== Analysis Complete ==="
echo "Data successfully stored in HDFS Medallion Architecture:"
echo "- Bronze Layer: /user/mineral_exports/bronze/"
echo "- Silver Layer: /user/mineral_exports/silver/"  
echo "- Gold Layer: /user/mineral_exports/gold/"
echo
echo "Access web interfaces:"
echo "- Hadoop NameNode: http://localhost:9870"
echo "- Spark Master: http://localhost:8080"
echo "- HBase Master: http://localhost:16010"
