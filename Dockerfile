# Final Dockerfile
FROM quay.io/jupyter/minimal-notebook:afe30f0c9ad8

COPY conda-linux-aarch64.lock /tmp/conda-linux-aarch64.lock

RUN conda update --quiet --file /tmp/conda-linux-aarch64.lock
RUN fix-permissions "${CONDA_DIR}"
RUN fix-permissions "/home/${NB_USER}"

COPY . .

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8000", "--no-browser", "--allow-root"]