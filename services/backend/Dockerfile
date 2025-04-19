FROM python:3.12.3

WORKDIR /app

RUN pip3 install flask boto3 jose pymongo python-keycloak requests glob2 pytest-shutil

COPY . .

EXPOSE 5000
CMD ["python", "app.py"]