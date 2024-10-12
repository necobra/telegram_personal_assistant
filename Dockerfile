FROM python:3.11-alpine
LABEL authors="NeCobra"

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["sh", "-c", "python3 main.py"]