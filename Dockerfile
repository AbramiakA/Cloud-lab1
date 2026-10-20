FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py ./
COPY init.sql ./
COPY my_project ./my_project

RUN useradd --create-home appuser
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]