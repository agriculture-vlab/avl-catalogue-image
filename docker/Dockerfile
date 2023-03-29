# https://hub.docker.com/_/ubuntu/
ARG ROOT_CONTAINER=ubuntu:20.04

FROM $ROOT_CONTAINER

LABEL maintainer="Agriculture Virtual Laboratory <support@agriculturevlab.eu>"
LABEL name="avl-catalogue-image"
LABEL version="0.0.0"
LABEL description="AVL catalogue generator"

ARG AVL_USER="avl"
ARG AVL_UID="1000"
ARG AVL_GID="100"

# Fix: https://github.com/hadolint/hadolint/wiki/DL4006
# Fix: https://github.com/koalaman/shellcheck/wiki/SC3014
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update --yes && \
    # - apt-get upgrade is run to patch known vulnerabilities in apt-get packages as
    #   the ubuntu base image is rebuilt too seldom sometimes (less than once a month)
    apt-get upgrade --yes && \
    apt-get install --yes --no-install-recommends \
    ca-certificates \
    curl \
    git \
    locales \
    sudo \
    # - tini is installed as a helpful container entrypoint that reaps zombie
    #   processes and such of the actual executable we want to start, see
    #   https://github.com/krallin/tini#why-tini for details.
    tini \
    wget && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

# Configure environment
ENV SHELL=/bin/bash \
    AVL_USER="${AVL_USER}" \
    AVL_UID=${AVL_UID} \
    AVL_GID=${AVL_GID} \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8
ENV PATH="${CONDA_DIR}/bin:${PATH}" \
    HOME="/home/${NB_USER}"

# Copy a script that we will use to correct permissions after running certain commands
COPY fix-permissions /usr/local/bin/fix-permissions
RUN chmod a+rx /usr/local/bin/fix-permissions

# Create user with name USER and UID=1000 and in the 'users' group
# and make sure these dirs are writable by the 'users' group.
RUN echo "auth requisite pam_deny.so" >> /etc/pam.d/su && \
    sed -i.bak -e 's/^%admin/#%admin/' /etc/sudoers && \
    sed -i.bak -e 's/^%sudo/#%sudo/' /etc/sudoers && \
    useradd -l -m -s /bin/bash -N -u "${AVL_UID}" "${AVL_USER}" && \
    chmod g+w /etc/passwd && \
    fix-permissions "${HOME}"

USER ${AVL_USER}
WORKDIR /home/${AVL_USER}

# Use fixed miniforge version to ensure Python 3.9 in base environment
RUN curl -L -O "https://github.com/conda-forge/miniforge/releases/download/4.11.0-4/Mambaforge-$(uname)-$(uname -m).sh" && \
    bash Mambaforge-$(uname)-$(uname -m).sh -b -p "${HOME}/conda" && \
    source "${HOME}/conda/etc/profile.d/conda.sh" && \
    source "${HOME}/conda/etc/profile.d/mamba.sh" && \
    mamba activate && \
    mamba install --quiet --yes \
        xcube \
        xcube-cds \
        xcube-cmems \
        xcube-sh \
        xcube-cci \
        mkdocs && \
    mamba install --yes --only-deps agriculture-vlab && \
    pip install --no-deps git+https://github.com/agriculture-vlab/agriculture-vlab@pont-9-catalogue
