from fastapi.staticfiles import StaticFiles
import os

backend_url = "/graggle-backend"
frontend_url = "/graggle-frontend"

class Static():

    def configureStatic(app):
        static_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../public')
        app.mount(backend_url + frontend_url, StaticFiles(directory=static_directory), name="public")
        app.mount(frontend_url, StaticFiles(directory=static_directory), name="public")
        app.mount(backend_url, StaticFiles(directory=static_directory), name="public")


