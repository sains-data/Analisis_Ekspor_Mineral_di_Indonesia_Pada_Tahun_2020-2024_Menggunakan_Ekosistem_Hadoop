# Install required packages in Spark container using PowerShell

Write-Host "=== Installing required Python packages ===" -ForegroundColor Green

docker exec -it spark-master pip install pandas matplotlib seaborn plotly

Write-Host "Packages installed. Ready for analysis." -ForegroundColor Green
