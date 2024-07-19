
# PySpark Frequent Pattern Mining Application

## Overview
This application leverages Apache Spark's powerful data processing capabilities to discover rare and valuable patterns in transaction data. These insights are vital for identifying significant but uncommon associations across various domains such as retail, finance, and e-commerce analytics.

## Features
- **Efficient Data Processing**: Utilizes Apache Spark for scalable and efficient analysis of large datasets.
- **Pattern Mining**: Implements the FP-Growth algorithm to find frequent itemsets without candidate generation, reducing computational overhead.
- **Cluster-Based Analysis**: Categorizes patterns into 'rare' and 'common' clusters for detailed analysis.
- **Association Rule Mining**: Derives meaningful association rules from frequent itemsets to uncover relationships between items.

## Setup and Configuration
### Docker Setup
1. **Pull the Docker Image**:
   Ensure Docker is installed on your system and pull the Apache Spark image:
   ```bash
   docker pull apache/spark-py
   ```
2. **Run the Docker Container**:
   Mount your project directory to the container to facilitate easy development and testing:
   ```bash
   docker run -d --name wonderful_mahavira --mount type=bind,src="$PWD",target=/data apache/spark-py
   ```
3. **Access Container**:
   Enter the container as root to perform setup operations:
   ```bash
   docker exec -u 0 -it wonderful_mahavira /bin/bash
   ```

### Running the Application
Navigate to the project directory inside the container and run the PySpark script:
```bash
cd /data
/opt/spark/bin/spark-submit main.py
```

## Data Preprocessing
Utilize the `filepreprocessing.py` script to convert raw transaction data into a format suitable for pattern mining, ensuring features are appropriately encoded as integers.

## Technology Stack
- **Apache Spark**: For robust distributed data processing.
- **Docker**: Ensures a consistent and isolated environment for development and deployment.
- **Python/PySpark**: Offers a high-level interface for Spark programming and rapid prototyping.

## Usage
To conduct pattern mining:
1. Prepare your transaction data according to the guidelines provided in `filepreprocessing.py`.
2. Adjust the script parameters such as support and confidence thresholds as needed.
3. Run the script using Spark to generate patterns and rules.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
