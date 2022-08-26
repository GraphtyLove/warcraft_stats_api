FROM python:3.10

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python3", "-m", "uvicorn",  "api:app"]