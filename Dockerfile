FROM continuumio/miniconda3

#RUN conda update -n base -c defaults conda
RUN conda install -y conda-build anaconda-client conda-verify

# prepare app directory
COPY . /home/app/
WORKDIR /home/app/