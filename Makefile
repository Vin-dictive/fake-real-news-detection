.PHONY: all clean download validate split preprocess eda model evaluate report help

# URLs for data download
FAKE_URL = "https://raw.githubusercontent.com/Vin-dictive/fake-real-news-detection/refs/heads/main/data/raw/Fake.csv"
TRUE_URL = "https://raw.githubusercontent.com/Vin-dictive/fake-real-news-detection/refs/heads/main/data/raw/True.csv"

# Default target
all: download validate split validate-train preprocess eda model evaluate report

# Download raw data
data/raw/Fake.csv:
	python scripts/00_download_data.py --url=$(FAKE_URL) --write_to=data/raw

data/raw/True.csv:
	python scripts/00_download_data.py --url=$(TRUE_URL) --write_to=data/raw

download: data/raw/Fake.csv data/raw/True.csv

# Clean and transform data
data/processed/complete_data.csv: data/raw/True.csv data/raw/Fake.csv
	python scripts/01_clean_transform_data.py --raw_true_data=data/raw/True.csv --raw_fake_data=data/raw/Fake.csv

# Validate processed data
validate: data/processed/complete_data.csv
	python scripts/02_data_validation_1.py --processed_data_path=data/processed/complete_data.csv

# Split data
data/processed/train_data.csv data/processed/test_data.csv: data/processed/complete_data.csv
	python scripts/03_data_splitting.py --data_path=data/processed/complete_data.csv

split: data/processed/train_data.csv data/processed/test_data.csv

# Validate training data
validate-train: data/processed/train_data.csv
	python scripts/04_data_validation_2.py --train_data_path=data/processed/train_data.csv

# Preprocess data
preprocess: data/processed/train_data.csv data/processed/test_data.csv
	python scripts/05_data_preprocessing.py --train_data_path=data/processed/train_data.csv --test_data_path=data/processed/test_data.csv

# Exploratory data analysis
eda: data/processed/train_data.csv
	python scripts/06_EDA.py --train_data_path=data/processed/train_data.csv

# Train model
models/naive_bayes.pkl: data/processed/train_data.csv data/processed/test_data.csv
	python scripts/07_model_fitting.py --train_data_path=data/processed/train_data.csv --test_data_path=data/processed/test_data.csv

model: models/naive_bayes.pkl

# Evaluate model
evaluate: models/naive_bayes.pkl data/processed/test_data.csv
	python scripts/08_model_evaluation.py --test_data_path=data/processed/test_data.csv --model_path=models/naive_bayes.pkl

# Render report
report: evaluate
	quarto render

# Clean generated files
clean:
	rm -rf data/processed/*
	rm -rf data/raw/*
	rm -rf data/text/*
	rm -rf models/*
	rm -rf img/*
	rm -rf docs/img/*
	rm -rf docs/reports/*

# Help target
help:
	@echo "Available targets:"
	@echo "  all          - Run complete pipeline (default)"
	@echo "  download     - Download raw data"
	@echo "  validate     - Validate processed data"
	@echo "  split        - Split data into train/test"
	@echo "  preprocess   - Preprocess train and test data"
	@echo "  eda          - Run exploratory data analysis"
	@echo "  model        - Train the model"
	@echo "  evaluate     - Evaluate the model"
	@echo "  report       - Generate final report"
	@echo "  clean        - Remove generated files"
	@echo "  help         - Show this help message"
