FROM python:3

RUN apt install tesseract
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "RunDetector.py" ]
