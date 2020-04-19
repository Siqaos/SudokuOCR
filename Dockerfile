FROM ubuntu:18.04
ENV TESS_VER="4.1.1"
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    autoconf \
    autoconf-archive \
    automake \
    build-essential\
    git \
    wget \
	libjpeg-dev \
	libjpeg8-dev \
	libleptonica-dev \
	libopencv-dev \
	libtesseract-dev \
	libtiff5-dev \
	libtool \
	pkg-config \
	python3 \
	python3-dev \
	python3-setuptools \
	python3-pip \
	nginx \
	supervisor \
	sqlite3 \
	tesseract-ocr \
	zlib1g-dev \
	curl wget locales && \
	pip3 install -U pip setuptools
RUN curl http://www.leptonica.org/source/leptonica-1.74.4.tar.gz -o leptonica-1.74.4.tar.gz && \
	tar -zxvf leptonica-1.74.4.tar.gz && \
	cd leptonica-1.74.4 && ./configure && make && make install && \
	cd .. && rm -rf leptonica*
RUN wget https://github.com/tesseract-ocr/tesseract/archive/4.1.1.tar.gz && \
    tar xvf ${TESS_VER}.tar.gz \
	cd tesseract-4.1.1 && \
	./autogen.sh && \
	./configure && \
	LDFLAGS="-L/usr/local/lib" CFLAGS="-I/usr/local/include" make && \
	make install && \
	ldconfig && \
	cd .. && rm -rf tesseract
RUN curl -LO https://github.com/tesseract-ocr/tessdata/raw/master/deu.traineddata && \
	mv deu.traineddata /usr/local/share/tessdata/
RUN pip3 install uwsgi
COPY requirements.txt /home/docker/code/
RUN pip3 --no-cache-dir install -U pip
RUN pip3 --no-cache-dir install -r /home/docker/code/requirements.txt
COPY ./app /home/docker/code/
EXPOSE 80
