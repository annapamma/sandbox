# ----------------------------------------------------------------------------
FROM docker:19.03.11 as static-docker-source

# ----------------------------------------------------------------------------
FROM alpine:3.11 as bin-base
RUN apk add --update --no-cache curl perl-utils unzip wget

# kubectl
# ----------------------------------------------------------------------------
FROM bin-base as bin-kubectl
ARG KUBECTL_VERSION=1.15.7
RUN \
  curl -L https://storage.googleapis.com/kubernetes-release/release/v${KUBECTL_VERSION}/bin/linux/amd64/kubectl -o /usr/local/bin/kubectl && \
  chmod +x /usr/local/bin/kubectl

# terraform
# ----------------------------------------------------------------------------
FROM bin-base as bin-terraform
# https://www.terraform.io/downloads.html
ARG TF_VERSION=0.12.21
ARG TF_SHA256=ca0d0796c79d14ee73a3d45649dab5e531f0768ee98da71b31e423e3278e9aa9
RUN \
  wget -nv https://releases.hashicorp.com/terraform/${TF_VERSION}/terraform_${TF_VERSION}_linux_amd64.zip &&\
  test $(shasum -a 256 terraform_${TF_VERSION}_linux_amd64.zip | awk '{print $1}') = ${TF_SHA256} &&\
  unzip terraform_${TF_VERSION}_linux_amd64.zip &&\
  rm terraform_${TF_VERSION}_linux_amd64.zip &&\
  mv terraform /usr/local/bin

# kapp
# ----------------------------------------------------------------------------
FROM bin-base as bin-kapp
# https://github.com/k14s/kapp/releases
ARG KAPP_VERSION=0.19.0
ARG KAPP_SHA256=99a2597d29ab9cf75d636a8220cb7e5ee315ac85b7adeb48b6c1ccb56a5cf477
RUN \
  wget -nv https://github.com/k14s/kapp/releases/download/v${KAPP_VERSION}/kapp-linux-amd64 &&\
  test $(shasum -a 256 kapp-linux-amd64 | awk '{print $1}') = ${KAPP_SHA256} &&\
  mv kapp-linux-amd64 /usr/local/bin/kapp &&\
  chmod +x /usr/local/bin/kapp

# kbld
# ----------------------------------------------------------------------------
FROM bin-base as bin-kbld
# https://github.com/k14s/kbld/releases
ARG KBLD_VERSION=0.13.0
ARG KBLD_SHA256=c5dc9a5e2fc1795f64f674cbc528a28c269432ce9485ee4dc74d8d18890dd4be
RUN \
  wget -nv https://github.com/k14s/kbld/releases/download/v${KBLD_VERSION}/kbld-linux-amd64 &&\
  test $(shasum -a 256 kbld-linux-amd64 | awk '{print $1}') = ${KBLD_SHA256} &&\
  mv kbld-linux-amd64 /usr/local/bin/kbld &&\
  chmod +x /usr/local/bin/kbld

# sops
# ----------------------------------------------------------------------------
FROM bin-base as bin-sops
# https://github.com/mozilla/sops/releases
ARG SOPS_VERSION=3.5.0
ARG SOPS_SHA256=610fca9687d1326ef2e1a66699a740f5dbd5ac8130190275959da737ec52f096
RUN \
  wget -nv https://github.com/mozilla/sops/releases/download/v${SOPS_VERSION}/sops-v${SOPS_VERSION}.linux &&\
  test $(shasum -a 256 sops-v${SOPS_VERSION}.linux | awk '{print $1}') = ${SOPS_SHA256} &&\
  mv sops-v${SOPS_VERSION}.linux /usr/local/bin/sops &&\
  chmod +x /usr/local/bin/sops

# dotenv-exec
# ----------------------------------------------------------------------------
FROM bin-base as bin-dotenv-exec
ARG DOTENV_EXEC_VERSION=0.1.1
ARG DOTENV_EXEC_SHA256=52e82aa8b8e6e63fa14139d0f8ee16b3a0259fa63d21159362ce80b1d2e5eb85
RUN \
  wget -nv https://github.com/lirsacc/dotenv-exec/releases/download/v${DOTENV_EXEC_VERSION}/dotenv-exec-x86_64-unknown-linux-musl &&\
  test $(shasum -a 256 dotenv-exec-x86_64-unknown-linux-musl | awk '{print $1}') = ${DOTENV_EXEC_SHA256} &&\
  mv dotenv-exec-x86_64-unknown-linux-musl /usr/local/bin/dotenv-exec &&\
  chmod +x /usr/local/bin/dotenv-exec

# kustomize
# ----------------------------------------------------------------------------
FROM bin-base as bin-kustomize
# https://github.com/kubernetes-sigs/kustomize/releases
ARG KUSTOMIZE_VERSION=3.4.0
ARG KUSTOMIZE_SHA256=eabfa641685b1a168c021191e6029f66125be94449b60eb12843da8df3b092ba
RUN \
  wget -nv https://github.com/kubernetes-sigs/kustomize/releases/download/kustomize%2Fv${KUSTOMIZE_VERSION}/kustomize_v${KUSTOMIZE_VERSION}_linux_amd64.tar.gz &&\
  test $(shasum -a 256 kustomize_v${KUSTOMIZE_VERSION}_linux_amd64.tar.gz | awk '{print $1}') = ${KUSTOMIZE_SHA256} &&\
  tar -xvzf kustomize_v${KUSTOMIZE_VERSION}_linux_amd64.tar.gz &&\
  rm kustomize_v${KUSTOMIZE_VERSION}_linux_amd64.tar.gz &&\
  mv kustomize /usr/local/bin/kustomize

# ----------------------------------------------------------------------------
FROM alpine:3.11

LABEL \
    maintainer="engineering@thread.com" \
    description="Docker image with some preinstalled infrastructure and devops tooling. \
This is aimed for use in CI context."

RUN \
  apk add --update --no-cache \
    git \
    bash \
    openssh \
    python3 \
    curl \
    make \
    libressl \
    py-crcmod \
    libc6-compat \
    openssh-client \
    ca-certificates &&\
  rm -rf /var/cache/apk/*

ARG CLOUD_SDK_VERSION=296.0.1

ENV PATH /google-cloud-sdk/bin:$PATH

 RUN \
    curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz && \
    tar xzf google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz && \
    rm google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz && \
    gcloud config set core/disable_usage_reporting true && \
    gcloud config set component_manager/disable_update_check true && \
    gcloud config set metrics/environment github_docker_image && \
    gcloud components install beta cloud_sql_proxy docker-credential-gcr &&\
    rm -rf /google-cloud-sdk/install/.backup google-cloud-sdk/.install/.backup

COPY --from=static-docker-source /usr/local/bin/docker /usr/local/bin/docker

COPY --from=bin-kubectl /usr/local/bin/* /usr/local/bin
COPY --from=bin-terraform /usr/local/bin/* /usr/local/bin
COPY --from=bin-kapp /usr/local/bin/* /usr/local/bin
COPY --from=bin-kbld /usr/local/bin/* /usr/local/bin
COPY --from=bin-sops /usr/local/bin/* /usr/local/bin
COPY --from=bin-dotenv-exec /usr/local/bin/* /usr/local/bin
COPY --from=bin-kustomize /usr/local/bin/* /usr/local/bin

# Override this with a volume when workin on local files.
RUN mkdir workspace
WORKDIR workspace

ENTRYPOINT ["/bin/sh", "-c"]
CMD ["bash"]

