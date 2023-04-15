FROM python:3.9-slim-buster

WORKDIR /backend

COPY requirements.txt /backend

RUN pip install -r requirements.txt --no-cache-dir

COPY . /backend

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
