# Indonesian Mineral Export Analysis - Web Interface Access
# PowerShell script to open all web interfaces

Write-Host "=== Indonesian Mineral Export Analysis - Web Interfaces ===" -ForegroundColor Green
Write-Host "Opening web interfaces for the big data infrastructure..." -ForegroundColor Yellow

# Check if Docker containers are running
Write-Host "`nChecking Docker container status..." -ForegroundColor Cyan
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

Write-Host "`nOpening web interfaces..." -ForegroundColor Cyan

# Open Hadoop NameNode Web UI
Write-Host "Opening Hadoop NameNode Web UI (http://localhost:9870)..." -ForegroundColor White
Start-Process "http://localhost:9870"

# Wait a moment
Start-Sleep -Seconds 2

# Open Spark Master Web UI  
Write-Host "Opening Spark Master Web UI (http://localhost:8080)..." -ForegroundColor White
Start-Process "http://localhost:8080"

# Wait a moment
Start-Sleep -Seconds 2

# Open HBase Master Web UI
Write-Host "Opening HBase Master Web UI (http://localhost:16010)..." -ForegroundColor White
Start-Process "http://localhost:16010"

Write-Host "`n=== Web Interfaces Opened ===" -ForegroundColor Green
Write-Host "You can now access:" -ForegroundColor Yellow
Write-Host "1. Hadoop HDFS Status: http://localhost:9870" -ForegroundColor White
Write-Host "2. Spark Cluster Status: http://localhost:8080" -ForegroundColor White  
Write-Host "3. HBase Database Status: http://localhost:16010" -ForegroundColor White

Write-Host "`n=== Data Access Information ===" -ForegroundColor Green
Write-Host "HDFS Medallion Architecture:" -ForegroundColor Yellow
Write-Host "- Bronze Layer: /user/mineral_exports/bronze/" -ForegroundColor White
Write-Host "- Silver Layer: /user/mineral_exports/silver/" -ForegroundColor White
Write-Host "- Gold Layer: /user/mineral_exports/gold/" -ForegroundColor White

Write-Host "`nData File: ekspor_mineral_indonesia_WITS.csv" -ForegroundColor White
Write-Host "Total Records: 1,000,000 Indonesian mineral export transactions" -ForegroundColor White
Write-Host "Time Period: 2020-2024" -ForegroundColor White

Write-Host "`nPress any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
