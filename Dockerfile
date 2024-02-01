FROM python:3.9-slim

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 80

RUN useradd appuser && chown -R appuser /usr/src/app
USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
