FROM python:3.9
WORKDIR /app
RUN apt-get update \
  && apt-get -y install tesseract-ocr \
  && apt-get install -y python3 python3-distutils python3-pip \
  && cd /usr/local/bin \
  && pip3 --no-cache-dir install --upgrade pip \
  && rm -rf /var/lib/apt/lists/*

RUN apt update \
  && apt-get install ffmpeg libsm6 libxext6 -y
RUN pip3 install pytesseract
RUN pip3 install opencv-python
RUN pip3 install pillow

ADD requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8080

COPY 試題1 /app

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]