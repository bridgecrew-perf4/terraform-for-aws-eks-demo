from flask import Flask
import os
import requests
app = Flask(__name__)

backend_service_base_url = os.environ['BACKEND_URL']
backend_service_health_url = os.environ['BACKEND_HEALTH_URL']

@app.route('/backend/health')
def call_backend_health():
    response = requests.get(backend_service_health_url)
    return response.text

@app.route('/backend')
def call_backend():
    response = requests.get(backend_service_base_url)
    return response.text

@app.route('/health')
def health_check():
    return 'API-Server Service Health is Ok!'

@app.route('/')
def home():
    return 'Hello from API-Server Service!'