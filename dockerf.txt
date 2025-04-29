FROM python:3.12-slim

WORKDIR /app

COPY . /app

or 

COPY ..

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000


CMD ["python", "app.py"]
