FROM python:3.7.12
COPY . /app
WORKDIR /app
COPY requirements.txt .
RUN python -m pip install -U -r requirements.txt
CMD ["python", "main.py"]
