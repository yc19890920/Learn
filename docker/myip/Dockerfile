FROM ubuntu:18.04
RUN buildDeps='curl' \
    && apt-get update \
    && apt-get install -y $buildDeps \
    && rm -rf /var/lib/apt/lists/*
    # && apt-get purge -y --auto-remove $buildDeps
CMD [ "curl", "-s", "https://ip.cn" ]