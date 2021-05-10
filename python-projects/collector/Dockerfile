FROM python:3.7-alpine

WORKDIR /collector

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD ["nohup", "python3", "iccrawlerd.py", "&"]
