# Contributing to Fake Real News Detection

This outlines how to propose a change to the project.

## Prerequisites

Before you make a substantial pull request, you should always file an issue and make sure someone from the team agrees that it's a problem. If you've found a bug, create an associated issue and illustrate the bug with a minimal reproducible example.

## Pull request process

* We are accepting PR's only from project members at the moment.

## Code style

* New code should follow [PEP 8](https://pep8.org/) Python style guide.
  You can use [black](https://black.readthedocs.io/) for automatic code formatting and [flake8](https://flake8.pycqa.org/) for linting.

* Use meaningful variable names and keep functions focused on a single task.

* Add docstrings to all functions and classes using [Google style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).

* For Jupyter notebooks:
  * Use clear markdown cells to explain analysis steps
  * Keep code cells concise and well-commented
  * Include visualizations with proper titles and labels

<!-- * We use [pytest](https://pytest.org/) for unit tests.
  Contributions with test cases included are easier to accept. -->

## Developer Notes

### Developer Dependencies

* conda (>= 25.9.1)
* conda-lock (>= 3.0.4)

### Instructions for Adding New Dependencies

1. Open your terminal locally, direct to the root directory. Make sure you have conda and conda-lock installed on your local computer.

2. Create a conda environment called "fake-news-detection" using the "conda-lock.yml" by running in your terminal:

   ```bash
   conda-lock install --name fake-news-detection conda-lock.yml
   ```

3. Activate the conda environment:

   ```bash
   conda activate fake-news-detection
   ```

4. Use conda to install new packages:

   ```bash
   conda install {NEW-PACKAGE-NAME}
   ```

   If installing a package only available on PyPI, use pip and note it for requirements.txt updates.

5. At root directory, update environment.yml using:

   ```bash
   conda env export --from-history > environment.yml
   ```

6. Use conda-lock to solve and lock the updated environment for multiple platforms:

   ```bash
   conda-lock lock --file environment.yml
   conda-lock -f environment.yml -p osx-64 -p linux-64 -p win-64
   ```

## Code of Conduct

Please note that the project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By contributing to this project you agree to abide by its terms.

---

*This contributing guide is adapted from the [AI bias in farming project](https://github.com/skysheng7/AI_bias_in_farming/blob/main/CONTRIBUTING.md).*
