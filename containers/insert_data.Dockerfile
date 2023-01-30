FROM python:3.10.1

RUN pip install pandas

WORKDIR /app
COPY src/insert_data.py insert_data.py

ENTRYPOINT ["python", "insert_data.py"]