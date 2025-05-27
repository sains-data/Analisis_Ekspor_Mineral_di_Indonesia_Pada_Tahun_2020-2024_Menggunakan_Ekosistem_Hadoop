#!/bin/bash
# Install required packages in Spark container

echo "=== Installing required Python packages ==="

docker exec -it spark-master bash -c "pip install pandas matplotlib seaborn plotly"

echo "Packages installed. Ready for analysis."
