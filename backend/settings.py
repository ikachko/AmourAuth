import os

API_HOST = os.environ['API_HOST'] if 'API_HOST' in os.environ else '127.0.0.1'
API_PORT = os.environ['API_PORT'] if 'API_PORT' in os.environ else '5000'
