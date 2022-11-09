FROM python:alpine

WORKDIR /app

COPY . .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD ["python" , "Datastore_main.py"]