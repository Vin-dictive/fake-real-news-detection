# Fake Real News Detection

## About

This project implements a machine learning solution to classify news articles as real or fake using Naive Bayes classification techniques. With the increasing prevalence of misinformation in digital media, this tool aims to help identify potentially false news articles through statistical analysis.

![Word Cloud Analysis](img/fake_text_word_cloud.png)

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/Vin-dictive/fake-real-news-detection
cd fake-real-news-detection
```

**Note:** The initial clone may take some time as the repository contains dataset files (CSV files in the `data/` directory).

#### Development Environment

- **Jupyter** - Interactive notebook environment

## Dependencies

This project requires the following main dependencies:

- **Python 3.11**
- **Docker** (for containerized environment)
- **Data Science Libraries:**
  - pandas 2.3.3
  - numpy 2.3.5
  - scipy 1.16.3
  - scikit-learn 1.7.2
- **Visualization:**
  - matplotlib 3.10.8
  - wordcloud 1.9.4
- **Development Tools:**
  - jupyter
  - notebook 7.5.0
  - ipykernel 7.1.0
- **Data Validation:**
  - pandera 0.27.0
- **Utilities:**
  - click 8.3.1
  - requests 2.32.5
  - tabulate 0.9.0
  - quarto-cli
  - conda-lock

All dependencies are specified in `environment.yml` for conda or `conda-lock.yml` for reproducible builds.

### Environment Setup

<details>
<summary><strong>Option 1: Using Docker (Recommended)</strong></summary>

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

</details>

<details>
<summary><strong>Option 2: Using conda-lock</strong></summary>

1. Install from lock file for your platform:

   ```bash
   conda-lock install --name fake-news-detection conda-lock.yml
   conda activate fake-news-detection
   ```

</details>

<details>
<summary><strong>Option 3: Using environment.yml</strong></summary>

1. Create conda environment:

   ```bash
   conda env create -f environment.yml
   conda activate fake-news-detection
   ```

</details>

### Running the analysis

<details>
<summary><strong>Option 1: Using Makefile (Recommended)</strong></summary>

Run the complete analysis pipeline:

```bash
make all
```

Or run individual steps:

```bash
make download      # Download raw data
make validate      # Validate processed data
make split         # Split into train/test sets
make preprocess    # Preprocess data
make eda          # Run exploratory data analysis
make model        # Train the model
make evaluate     # Evaluate the model
make report       # Generate final report
make test         # To run tests
make clean        # Remove generated files
```

</details>

<details>
<summary><strong>Option 2: Using Docker with Makefile</strong></summary>

1. Start Docker container:

   ```bash
   docker compose up --build
   ```

2. In the terminal, look for a URL starting with `http://127.0.0.1:8888/lab?token=` and open it in your browser.

3. Run the analysis:

   ```bash
   make all
   ```

</details>

<details>
<summary><strong>Option 3: Running Scripts Manually</strong></summary>

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

python scripts/06_EDA.py \
   --train_data_path=data/processed/train_data.csv

python scripts/07_model_fitting.py \
   --train_data_path=data/processed/train_data.csv \
   --test_data_path=data/processed/test_data.csv

python scripts/08_model_evaluation.py \
   --test_data_path=data/processed/test_data.csv \
   --model_path=models/naive_bayes.pkl

quarto render
```

</details>

### Running the function tests

Function tests are written in python scripts. To run these tests to see whether they pass, 
please run the following command in the root project directory using bash terminal:

```bash
pytest tests/
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

<!-- ## Repository Structure

```
fake-real-news-detection/
├── .github/
│   └── workflows/
│       └── docker-publish.yml    # GitHub Actions workflow
├── data/
│   ├── processed/                # Processed datasets
│   ├── raw/                      # Raw datasets
│   │   ├── Fake.csv              # Fake news articles dataset
│   │   └── True.csv              # Real news articles dataset
│   └── text/                     # Generated text outputs
│       ├── classification_report.txt
│       ├── target_value_counts.txt
│       └── train_df_info.txt
├── docs/
│   ├── img/                      # Generated visualizations
│   └── reports/                  # Generated reports
├── img/                          # Static images for README
├── models/                       # Trained models
│   └── naive_bayes.pkl
├── notebooks/
│   └── 001_fake_news_classification_analysis.ipynb  # Main analysis notebook
├── reports/                      # Report templates
│   ├── fake_news_classification_analysis.qmd
│   └── references.bib
├── scripts/                      # Analysis pipeline scripts
│   ├── 00_download_data.py       # Data download
│   ├── 01_clean_transform_data.py # Data cleaning
│   ├── 02_data_validation_1.py   # Initial validation
│   ├── 03_data_splitting.py      # Train/test split
│   ├── 04_data_validation_2.py   # Training data validation
│   ├── 05_data_preprocessing.py  # Text preprocessing
│   ├── 06_EDA.py                 # Exploratory analysis
│   ├── 07_model_fitting.py       # Model training
│   └── 08_model_evaluation.py    # Model evaluation
├── .gitignore
├── CODE_OF_CONDUCT.md
├── conda-lock.yml
├── CONTRIBUTING.md
├── docker-compose.yml
├── Dockerfile
├── environment.yml
├── LICENSE.md
├── Makefile
├── README.md
└── _quarto.yml
``` -->

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
