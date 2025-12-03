# Final Dockerfile
FROM quay.io/jupyter/minimal-notebook:afe30f0c9ad8

USER root

# install LaTeX fonts for Quarto PDF rendering and libxml2 for mamba
RUN apt update \
    && apt install -y lmodern libxml2-dev texlive-fonts-recommended texlive-latex-extra

RUN fix-permissions "${CONDA_DIR}"
RUN fix-permissions "/home/${NB_USER}"

COPY . .

RUN conda update -n base -c conda-forge conda

RUN conda env update --name base --file environment.yml

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8000", "--no-browser", "--allow-root"]