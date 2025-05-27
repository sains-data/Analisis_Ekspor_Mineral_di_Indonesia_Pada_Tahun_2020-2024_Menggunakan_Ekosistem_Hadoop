#!/bin/bash
# Setup script for HDFS directories

echo "=== Setting up HDFS directories for mineral export analysis ==="

# Create HDFS directories for medallion architecture
echo "Creating HDFS directories..."
hadoop fs -mkdir -p /user/mineral_exports/bronze
hadoop fs -mkdir -p /user/mineral_exports/silver
hadoop fs -mkdir -p /user/mineral_exports/gold/by_country
hadoop fs -mkdir -p /user/mineral_exports/gold/by_product

# Set permissions
echo "Setting permissions..."
hadoop fs -chmod -R 777 /user/mineral_exports

echo "HDFS setup completed!"
