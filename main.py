"""
Entry point to the app
"""
from fastapi import FastAPI
from dotenv import load_dotenv

# load environment variables

load_dotenv()

from app.web_servers.http_server import run as run_http_server  # noqa

if __name__ == '__main__':
    # Run the rest_api http server basing
    app = FastAPI()

    run_http_server(app=app)
