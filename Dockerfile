FROM python:3.6

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["streamlit", "run", "--server.port", "5000", "app.py"]