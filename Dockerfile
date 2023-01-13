FROM python:3.11

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# python3 -m uvicorn api:app --port 8000 --host 0.0.0.0
CMD ["python3", "-m", "uvicorn", "api:app", "--port", "8000", "--host", "0.0.0.0"]