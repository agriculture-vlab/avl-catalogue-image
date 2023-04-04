# Using this mambaforge version to ensure Python 3.9 in base environment
ARG ROOT_CONTAINER=quay.io/condaforge/mambaforge:4.11.0-4

FROM $ROOT_CONTAINER

LABEL maintainer="Agriculture Virtual Laboratory <support@agriculturevlab.eu>"
LABEL name="avl-catalogue-image"
LABEL version="0.0.0"
LABEL description="AVL catalogue generator"

ENV PROJ_LIB /opt/conda/share/proj

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update --yes && \
    apt-get upgrade --yes && \
    apt-get install --yes --no-install-recommends \
    unzip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mamba install --quiet --yes \
        cartopy \
        cryptography==38.0.4 \
        tenacity \
        xcube \
        xcube-cds \
        xcube-cmems \
        xcube-sh \
        xcube-cci \
        mkdocs && \
    mamba install --yes --only-deps agriculture-vlab && \
    mamba clean --all -f --yes && \
    pip install --no-deps git+https://github.com/agriculture-vlab/agriculture-vlab@pont-9-catalogue

WORKDIR /root

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64-2.11.7.zip" \
    -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install

COPY --chmod=a+x generate_catalogue.py /root/
COPY mkdocs.yml /root/

ENTRYPOINT ["/usr/bin/bash", "-c"]
CMD ["/root/generate_catalogue.py"]
