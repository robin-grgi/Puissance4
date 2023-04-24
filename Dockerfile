
FROM python:3.8-slim

WORKDIR /usr/src

COPY requirements.txt .

RUN pip install --quiet --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn","API:app", "--host", "0.0.0.0",  "--port", "8000"]

