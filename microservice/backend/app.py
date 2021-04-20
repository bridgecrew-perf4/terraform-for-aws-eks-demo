from flask import Flask
app = Flask(__name__)

@app.route('/health')
def health_check():
    return 'Backend Service Health is Ok!'

@app.route('/')
def home():
    return 'Hello from Backend Service!'