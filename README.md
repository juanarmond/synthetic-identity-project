# Synthetic Identity Islands Project

## Project Overview

This project aims to generate synthetic identity data, introduce anomalies, and use various machine learning models to detect these anomalies. The project leverages AWS Neptune for graph database capabilities and EC2 for running machine learning models.

### Key Features
- **Synthetic Data Generation:** Create synthetic identity data for testing and development purposes.
- **Anomaly Introduction:** Introduce anomalies into the synthetic data to simulate real-world data issues.
- **AWS Neptune Integration:** Ingest data into AWS Neptune and use Gremlin queries to explore the graph data.
- **Anomaly Detection:** Utilize machine learning models on EC2 to detect anomalies within the data.

## Project Structure

```plaintext
synthetic-identity-project/
├── notebooks/
│   ├── data_generation.ipynb
│   ├── introduce_anomalies.ipynb
│   ├── data_ingestion.ipynb
│   ├── gremlin_queries.ipynb
│   └── anomaly_detection.ipynb
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── aws/
│   │   ├── neptune.tf
│   │   └── ec2.tf
├── gremlin/
│   ├── queries.txt
├── scripts/
│   ├── deploy.sh
│   ├── destroy.sh
│   ├── generate_data.py
│   ├── introduce_anomalies.py
│   ├── ingest_to_neptune.py
│   ├── train_model.py
│   └── detect_anomalies.py
├── data/
│   ├── synthetic_data/
│   ├── anomalies/
│   └── ingested_data/
├── models/
│   └── trained_models/
├── README.md
├── requirements.txt
└── .gitignore
```

## Getting Started

### Prerequisites

- **Python 3.10+**: Make sure you have Python installed. You can download it from [python.org](https://www.python.org/downloads/).
- **Terraform**: Install Terraform for managing AWS resources. Follow the installation guide on the [Terraform website](https://www.terraform.io/downloads.html).
- **AWS CLI**: Install the AWS Command Line Interface. Instructions are available on the [AWS CLI website](https://aws.amazon.com/cli/).

### Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/yourusername/synthetic-identity-project.git
   cd synthetic-identity-project
   ```

2. **Install Python dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to [OpenAI](https://openai.com/) for providing the AI assistance.
- Inspired by various synthetic data generation and anomaly detection projects.# synthetic-identity-project
