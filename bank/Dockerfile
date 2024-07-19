FROM python:3.12.1-slim

WORKDIR /app

COPY bank/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bank/ .

CMD ["python", "bank/src/main.py"]