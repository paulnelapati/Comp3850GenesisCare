FROM python:3

RUN apt-get update && apt-get install -y python3-opencv
RUN pip install opencv-python

RUN apt install -y tesseract-ocr
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "RunDetector.py" ]
