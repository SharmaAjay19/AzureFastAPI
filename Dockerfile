FROM python:3.9
WORKDIR /pkgs
COPY ./azurefastapi /pkgs/azurefastapi
COPY ./setup.py /pkgs/setup.py
RUN pip install .