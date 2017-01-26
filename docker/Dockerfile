FROM tensorflow/tensorflow:0.11.0

MAINTAINER Akshay Bhat <akshayubhat@gmail.com>
RUN apt-get update && apt-get install -y wget
WORKDIR "/bin/"
RUN wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-64bit-static.tar.xz
RUN tar xvfJ ffmpeg-release-64bit-static.tar.xz
RUN mv ffmpeg-3.2.2-64bit-static/* .
WORKDIR "/root/
RUN apt-get update && apt-get install -y \
		bc \
		build-essential \
		curl \
		git \
		libffi-dev \
		libssl-dev \
		libtiff5-dev \
		libzmq3-dev \
		nano \
		pkg-config \
		python-pip \
		python-dev \
		software-properties-common \
		unzip \
		vim \
		wget \
		zlib1g-dev \
		libboost-all-dev \
		libgflags-dev \
		libgoogle-glog-dev \
		&& \
	apt-get clean && \
	apt-get autoremove && \
	rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y libpq-dev && \
	apt-get clean && \
	apt-get autoremove && \
	rm -rf /var/lib/apt/lists/*
RUN pip install https://s3.amazonaws.com/pytorch/whl/cu75/torch-0.1.6.post22-cp27-none-linux_x86_64.whl
RUN pip install scipy
RUN pip install torchvision
RUN pip install --upgrade pip \
                          fabric \
                          django \
                          jinja \
                          jinja2 \
                          djangorestframework \
                          markdown \
                          django-filter \
                          "celery==3.1.23" \
                          "django-celery==3.1.17" \
                          "dj-database-url==0.4.0" \
                          "whitenoise==2.0.6" \
                          raven \
                          psycopg2 \
                          requests \
                          pandas \
                          boto3 \
                          protobuf \
                          humanize
RUN  git clone https://github.com/akshayubhat/DeepVideoAnalytics /root/DVA
WORKDIR "/root/DVA"