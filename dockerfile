# FROM python:3.12-bookworm

# WORKDIR /app

# COPY . /app

# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt

# EXPOSE 5000


# CMD ["python", "app.py"]

FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py . 

CMD ["python", "app.py"]