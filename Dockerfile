FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

ENV PYTHONUNBAFFERED=1

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
