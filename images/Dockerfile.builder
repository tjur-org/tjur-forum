# syntax=docker/dockerfile:labs

################################################################################
# Builder target
################################################################################
FROM python as builder

RUN python -m venv venv

COPY reqs reqs
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --require-hashes --pre \
        -r reqs/requirements.txt && \
    pip check


################################################################################
# Test builder target
################################################################################
FROM builder as builder-test

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --require-hashes --pre \
        -c reqs/requirements.txt \
        -r reqs/dev-requirements.txt && \
    pip check
