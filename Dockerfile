# Final Dockerfile
FROM quay.io/jupyter/minimal-notebook:afe30f0c9ad8

USER root

# Install full LaTeX stack for PDF rendering
RUN apt update && apt install -y \
    lmodern \
    texlive \
    texlive-luatex

RUN fix-permissions "${CONDA_DIR}"
RUN fix-permissions "/home/${NB_USER}"

COPY . .

RUN conda update -n base -c conda-forge conda

RUN conda env update --name base --file environment.yml

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8000", "--no-browser", "--allow-root"]