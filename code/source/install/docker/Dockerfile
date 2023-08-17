FROM python:3.10 AS compile-image
RUN python -m venv /opt/mdpu-kit
# Make sure we use the virtualenv
ENV PATH="/opt/mdpu-kit/bin:$PATH"
# Install package
COPY dist /dist
RUN pip install "$(ls /dist/mdpu_kit-*manylinux*_x86_64.whl)[gpu,cu11,lmp]" \
    && dp -h \
    && lmp -h \
    && python -m mdpu -h

FROM python:3.10 AS build-image
COPY --from=compile-image /opt/mdpu-kit /opt/mdpu-kit
ENV PATH="/opt/mdpu-kit/bin:$PATH"
CMD ["/bin/bash"]
