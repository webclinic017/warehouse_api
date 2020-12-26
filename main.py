"""
Entry point to the app:
In production, run using gunicorn using `gunicorn -c python:web_config 'main:create_app()'`
"""
from dotenv import load_dotenv

# load environment variables
load_dotenv()


from web_config import web_service_config  # noqa
from app.abstract.config import is_production  # noqa
from app.web_servers.http_server import run, create_app  # noqa

if __name__ == '__main__':

    if not is_production():
        # Run the rest_api http server using uvicorn when not in production
        run(app=create_app(), web_service_config=web_service_config)
