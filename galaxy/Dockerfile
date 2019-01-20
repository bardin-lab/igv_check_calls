FROM continuumio/miniconda3:4.5.11

RUN apt-get update && apt-get install -y xvfb libxrender1 libxtst6 && apt-get clean
RUN conda create -p /usr/local --copy -y -c conda-forge -c bioconda xvfbwrapper samtools igv openjdk=8 freetype font-ttf-dejavu-sans-mono fontconfig coreutils && rm -Rf /opt
