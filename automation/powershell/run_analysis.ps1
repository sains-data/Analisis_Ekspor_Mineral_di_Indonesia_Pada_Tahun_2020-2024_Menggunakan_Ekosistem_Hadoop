# Run mineral export analysis in Spark container using PowerShell

Write-Host "=== Mineral Export Analysis with Medallion Architecture ===" -ForegroundColor Green
Write-Host "Starting analysis with bronze, silver, and gold layers..." -ForegroundColor Green

# Define the Python script content
$pythonScript = @"
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg, count, desc
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType

print('=== Initializing Spark Session ===')
spark = SparkSession.builder \
    .appName('Mineral Export Analysis') \
    .master('local[*]') \
    .getOrCreate()

print('\n=== BRONZE LAYER: Raw Data Ingestion ===')
# Define schema for CSV data
schema = StructType([
    StructField('Reporter', StringType(), True),
    StructField('TradeFlow', StringType(), True),
    StructField('ProductCode', DoubleType(), True),
    StructField('Product Description', StringType(), True),
    StructField('Year', IntegerType(), True),
    StructField('Partner', StringType(), True),
    StructField('Trade Value 1000USD', DoubleType(), True),
    StructField('Quantity', DoubleType(), True),
    StructField('Quantity Unit', StringType(), True)
])

# Read CSV file (Bronze layer)
bronze_df = spark.read.format('csv') \
    .option('header', 'true') \
    .option('delimiter', ',') \
    .schema(schema) \
    .load('/data/ekspor_mineral_indonesia_WITS.csv')
    
print(f'Bronze layer loaded with {bronze_df.count()} records')
print('Sample bronze data:')
bronze_df.show(5, truncate=False)

print('\n=== SILVER LAYER: Data Cleaning and Transformation ===')
# Clean and transform data (Silver layer)
silver_df = bronze_df \
    .filter(col('Reporter') == 'Indonesia') \
    .filter(col('TradeFlow') == 'Export') \
    .withColumn('TradeValueUSD', col('Trade Value 1000USD') * 1000) \
    .withColumn('QuantityKg', col('Quantity')) \
    .withColumn('UnitPriceUSD', col('TradeValueUSD') / col('QuantityKg')) \
    .select(
        'ProductCode', 
        'Product Description', 
        'Year', 
        'Partner', 
        'TradeValueUSD', 
        'QuantityKg', 
        'UnitPriceUSD'
    )

print(f'Silver layer created with {silver_df.count()} records')
print('Sample silver data:')
silver_df.show(5, truncate=False)

print('\n=== GOLD LAYER: Business Metrics and Aggregations ===')
# Create exports by country (Gold layer)
exports_by_country = silver_df.groupBy('Partner').agg(
    sum('TradeValueUSD').alias('TotalExportValueUSD'),
    sum('QuantityKg').alias('TotalExportQuantityKg'),
    avg('UnitPriceUSD').alias('AvgUnitPriceUSD')
).orderBy(desc('TotalExportValueUSD'))

print('Gold layer - Exports by Country:')
exports_by_country.show(10, truncate=False)

# Create exports by product (Gold layer)
exports_by_product = silver_df.groupBy('ProductCode', 'Product Description').agg(
    sum('TradeValueUSD').alias('TotalExportValueUSD'),
    sum('QuantityKg').alias('TotalExportQuantityKg'),
    count('Partner').alias('NumberOfCountriesExportedTo')
).orderBy(desc('TotalExportValueUSD'))

print('Gold layer - Exports by Product:')
exports_by_product.show(10, truncate=False)

print('\n=== Analysis Complete ===')
spark.stop()
"@

# Save Python script to a temporary file
$tempFile = "$env:TEMP\mineral_analysis_temp.py"
$pythonScript | Out-File -FilePath $tempFile -Encoding utf8

# Copy the python file to the container
docker cp $tempFile spark-master:/tmp/mineral_analysis_temp.py

# Run the analysis
docker exec -it spark-master python /tmp/mineral_analysis_temp.py

# Clean up
Remove-Item $tempFile

Write-Host "Analysis completed!" -ForegroundColor Green
