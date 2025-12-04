# Fake Real News Detection

## About

This project implements a machine learning solution to classify news articles as real or fake using Naive Bayes classification techniques. With the increasing prevalence of misinformation in digital media, this tool aims to help identify potentially false news articles through statistical analysis.

![Word Cloud Analysis](img/readme_1.png)

![Word Cloud Analysis](img/readme_2.png)

![Word Cloud Analysis](img/readme_3.png)

![Word Cloud Analysis](img/readme_4.png)

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/Vin-dictive/fake-real-news-detection
cd fake-real-news-detection
```

**Note:** The initial clone may take some time as the repository contains dataset files (CSV files in the `data/` directory).

#### Development Environment

- **Jupyter** - Interactive notebook environment

### Environment Setup

#### Option 1: If you have conda-lock installed, use conda-lock (Recommended)

1. Install from lock file for your platform:

   ```bash
   conda-lock install --name fake-news-detection conda-lock.yml
   conda activate fake-news-detection
   ```

#### Option 2: Using environment.yml

1. Create conda environment:

   ```bash
   conda env create -f environment.yml
   conda activate fake-news-detection
   ```

#### Option 3: Using Docker

1. Build and run with Docker Compose for running image from docker hub:

   ```bash
   docker compose up --build
   ```

   For ARM based chips run with platform as linux/arm64 in docker-compose.yml

2. Or build and run directly:

   ```bash
   docker build -t fake-news-detection . 
   docker run --rm -p 8000:8000 fake-news-detection
   ```

3. Access Jupyter Lab at <http://127.0.0.1:8000/lab>

### Running the analysis

1. Navigate to the root of this project on your computer using the
   command line and enter the following command:

   ```bash
   docker compose up --build
   ```

2. In the terminal, look for a URL that starts with
`http://127.0.0.1:8888/lab?token=`
Copy and paste that URL into your browser.

3. To run the analysis,
open a terminal and run the following commands:

   ```bash
   python scripts/00_download_data.py \
      --url="https://raw.githubusercontent.com/Vin-dictive/fake-real-news-detection/refs/heads/main/data/raw/Fake.csv" \
      --write_to=data/raw
   
   python scripts/00_download_data.py \
      --url="https://raw.githubusercontent.com/Vin-dictive/fake-real-news-detection/refs/heads/main/data/raw/True.csv" \
      --write_to=data/raw
   
   python scripts/01_clean_transform_data.py \
      --raw_true_data=data/raw/True.csv \
      --raw_fake_data=data/raw/Fake.csv

   python scripts/02_data_validation_1.py \
      --processed_data_path=data/processed/complete_data.csv

   python scripts/03_data_splitting.py \
      --data_path=data/processed/complete_data.csv

   python scripts/04_data_validation_2.py \
      --train_data_path=data/processed/train_data.csv

   python scripts/05_data_preprocessing.py \
      --train_data_path=data/processed/train_data.csv \
      --test_data_path=data/processed/test_data.csv

   quarto render
   ```

### Clean up

1. To shut down the container and clean up the resources,
type `Ctrl` + `C` in the terminal
where you launched the container, and then type `docker compose rm`

## Dataset Information

This project uses a news classification dataset containing:

- **True.csv**: Contains real news articles
- **False.csv**: Contains fake news articles

### Dataset Details

- **Source**: <https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset>
- **Size**: 116.37 MB

*Note: Please refer to the original dataset documentation for detailed information about data collection methodology and licensing terms.*

## Repository Structure

```
fake-real-news-detection/
├── .github/
│   └── workflows/
│       └── docker-publish.yml    # GitHub Actions workflow
├── data/
│   └── raw/
│       ├── Fake.csv              # Fake news articles dataset
│       └── True.csv              # Real news articles dataset
├── img/
│   ├── readme_1.png              
│   ├── readme_2.png
│   ├── readme_3.png              
│   └── readme_4.png
├── notebooks/
│   └── 001_fake_news_classification_analysis.ipynb  # Main analysis and modeling notebook
├── reports/                      # Generated reports and outputs
├── scripts/
│   └── 00_download_data.py       # Data download script
├── .gitignore
├── CODE_OF_CONDUCT.md
├── conda-lock.yml
├── CONTRIBUTING.md
├── docker-compose.yml
├── Dockerfile
├── environment.yml
├── LICENSE
└── README.md
```

## Contributors

### Jessie Liang

- **Affiliation**: University of British Columbia
- **Email**: <rnliang.jessie@gmail.com>
- **GitHub**: [@jessie-liang](https://github.com/jessie-liang)

### Sarah Gauthier

- **Affiliation**: University of British Columbia
- **Email**: <sgauth01@student.ubc.ca>
- **GitHub**: [@sgauth01](https://github.com/sgauth01)

### Vinay Valson

- **Affiliation**: University of British Columbia
- **Email**: <vinay.valson@gmail.com>
- **GitHub**: [@Vin-dictive](https://github.com/Vin-dictive)

## Contributing

We welcome contributions to this project! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on how to get started.

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

## License

This project’s source code is licensed under the MIT License.  The documentation, reports, and written materials in this repository are licensed under the [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) license. See the [LICENSE](LICENSE) file for details.
