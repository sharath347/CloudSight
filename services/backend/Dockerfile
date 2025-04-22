FROM python:3.10.12

WORKDIR /app

RUN pip3 install flask flask-cors boto3 pymongo python-keycloak python-jose

COPY . .

EXPOSE 5000
CMD ["python", "app.py"]