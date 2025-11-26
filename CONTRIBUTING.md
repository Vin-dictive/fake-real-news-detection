# Contributing to Fake Real News Detection

The following outlines the steps to propose a change and contribute to the project.

## Prerequisites

Before opening a new pull request, you are supposed to write an issue first and wait for someone from the team to approve your ideas. If a bug is found, please reach out to us by an associated issue where you demonstrate how the bug happens using a minimal reproducible example.

## Pull request process

* Only PR's created by project members are accepted at the moment.

## Code style

* Your suggested code is supposed to follow [PEP 8](https://pep8.org/) Python style guide.

* You could choose [black](https://black.readthedocs.io/) for automatic code formatting and [flake8](https://flake8.pycqa.org/) for linting.

* Using straightforward variable names and keeping functions focused on one single task are appreciated.

* Docstrings need to be documented under all functions and classes definitions using [Google style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).

* For Jupyter notebooks:
  * Please make use of markdown cells to literate ideas and your coding script
  * Code cells should be concise and well-commented
  * Visualizations should come with proper titles and labels

<!-- * We use [pytest](https://pytest.org/) for unit tests.
  Contributions with test cases included are easier to accept. -->

## Developer Notes

### Developer Dependencies

* conda (>= 25.9.1)
* conda-lock (>= 3.0.4)

### Instructions for Adding New Dependencies

1. Set the working directory to the root directory in your terminal. Install conda and conda-lock in the base environment if you haven't already done so.

2. Create "fake-news-detection", a conda environment, using the "conda-lock.yml" file. Specifically, execute the following code in terminal:

   ```bash
   conda-lock install --name fake-news-detection conda-lock.yml
   ```

3. Activate this newly installed conda environment "fake-news-detection":

   ```bash
   conda activate fake-news-detection
   ```

4. Install new packages using conda if needed:

   ```bash
   conda install {NEW-PACKAGE-NAME}
   ```

   If the package you intend to install is only available on PyPI, please use pip to install it and then note it down for requirements.txt updates.

5. Return to the root directory, and then create the lastest version of environment.yml by typing:

   ```bash
   conda env export --from-history > environment.yml
   ```

6. Utilize conda-lock on the updated environment that should be adaptable across different systems and platforms:

   ```bash
   conda-lock lock --file environment.yml
   conda-lock -k explicit --file environment.yml -p osx-64 -p linux-64 -p win-64
   ```

## Code of Conduct

Please note that the project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By contributing to this project you agree to abide by its terms.

---

## Citation

*This contributing guide is adapted from the [AI bias in farming project](https://github.com/skysheng7/AI_bias_in_farming/blob/main/CONTRIBUTING.md).*
