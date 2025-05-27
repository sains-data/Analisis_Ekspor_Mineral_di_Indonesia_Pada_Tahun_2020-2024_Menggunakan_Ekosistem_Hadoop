# Script to open all web interfaces for Hadoop Big Data stack
Write-Host "Opening all web interfaces for Hadoop Big Data Analytics..." -ForegroundColor Green

# Test connections first
Write-Host "`nTesting connections..." -ForegroundColor Yellow
$services = @(
    @{Name="Hadoop NameNode"; Port=9870; URL="http://localhost:9870"},
    @{Name="Spark Master"; Port=8080; URL="http://localhost:8080"},
    @{Name="Spark Worker"; Port=8081; URL="http://localhost:8081"},
    @{Name="HBase Master"; Port=16010; URL="http://localhost:16010"},
    @{Name="Hadoop DataNode"; Port=9864; URL="http://localhost:9864"}
)

foreach ($service in $services) {
    $connection = Test-NetConnection -ComputerName localhost -Port $service.Port -WarningAction SilentlyContinue
    if ($connection.TcpTestSucceeded) {
        Write-Host "✓ $($service.Name) - Port $($service.Port) - AVAILABLE" -ForegroundColor Green
    } else {
        Write-Host "✗ $($service.Name) - Port $($service.Port) - NOT AVAILABLE" -ForegroundColor Red
    }
}

Write-Host "`nOpening web interfaces in browser..." -ForegroundColor Yellow

foreach ($service in $services) {
    $connection = Test-NetConnection -ComputerName localhost -Port $service.Port -WarningAction SilentlyContinue
    if ($connection.TcpTestSucceeded) {
        Write-Host "Opening $($service.Name)..." -ForegroundColor Cyan
        Start-Process $service.URL
        Start-Sleep -Seconds 2
    }
}

Write-Host "`n🎉 All available web interfaces have been opened!" -ForegroundColor Green
Write-Host "`nWeb Interface URLs:" -ForegroundColor Yellow
Write-Host "• Hadoop NameNode (HDFS): http://localhost:9870" -ForegroundColor White
Write-Host "• Spark Master: http://localhost:8080" -ForegroundColor White  
Write-Host "• Spark Worker: http://localhost:8081" -ForegroundColor White
Write-Host "• HBase Master: http://localhost:16010" -ForegroundColor White
Write-Host "• Hadoop DataNode: http://localhost:9864" -ForegroundColor White
