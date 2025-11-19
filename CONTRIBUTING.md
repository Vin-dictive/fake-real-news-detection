# Contributing Guidelines

## Development Setup

1. Create and activate the conda environment:

   ```bash
   conda env create -f environment.yml
   conda activate fake-news-detection
   ```

## Adding New Dependencies

When adding new packages to the project:

1. Install the package in your environment:

   ```bash
   conda install package-name
   # or
   pip install package-name
   ```

2. Add the package with its version to `environment.yml`:

   ```yaml
   dependencies:
     - package-name=1.2.3
   ```

3. Also update `requirements.txt` with the exact version:

   ```bash
   pip freeze | grep package-name >> requirements.txt
   ```

## Code Standards

- Follow PEP 8 for Python code
- Add docstrings to functions and classes
- Write tests for new functionality
- Update documentation as needed

## Issue Tracking

Use GitHub Issues to:

- Report bugs
- Request new features
- Ask questions about usage
- Discuss improvements
