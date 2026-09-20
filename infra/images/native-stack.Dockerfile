FROM docker.io/mambaorg/micromamba@sha256:e583f8e151fd1ebbc78b05cf4feb37ddbb518892dbabf6c0c03ea8ad613bc519

ARG SOURCE_LOCK_DIGEST
ARG BUILD_COMMIT_SHA

LABEL org.opencontainers.image.source="https://github.com/raphaelperrut/DSGeorref" \
      org.opencontainers.image.revision="${BUILD_COMMIT_SHA}" \
      io.dsgeorref.source-lock-digest="${SOURCE_LOCK_DIGEST}" \
      io.dsgeorref.runtime-platform="linux/amd64"

ENV PROJ_NETWORK=OFF \
    PROJ_DATA=/opt/conda/share/proj \
    GDAL_DATA=/opt/conda/share/gdal \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY --chown=$MAMBA_USER:$MAMBA_USER infra/images/native-stack.conda-lock.txt /tmp/native-stack.conda-lock.txt

RUN micromamba install --yes --name base --file /tmp/native-stack.conda-lock.txt \
    && micromamba clean --all --yes \
    && rm /tmp/native-stack.conda-lock.txt

ADD --chown=$MAMBA_USER:$MAMBA_USER --chmod=0444 \
    --checksum=sha256:944336ef298148dfd97478638567b223d929aba8717ad8be73ae962a62ecd61d \
    https://files.pythonhosted.org/packages/74/ed/15196be41f2bf84e358d899e62daf5666ba4f6dbab4cbad87d16cc16df6d/fastapi-0.140.2-py3-none-any.whl \
    /tmp/fastapi-0.140.2-py3-none-any.whl

RUN /opt/conda/bin/python -m pip install --no-deps /tmp/fastapi-0.140.2-py3-none-any.whl \
    && rm /tmp/fastapi-0.140.2-py3-none-any.whl \
    && /opt/conda/bin/python -m pip check

CMD ["/opt/conda/bin/python", "--version"]
