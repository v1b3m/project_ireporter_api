
from project.server import app
import os

app_settings = os.getenv(
    'APP_SETTINGS',
    'project.server.config.DevelopmentConfig'
)

app.config.from_object(app_settings)

if __name__ == '__main__':
    app.run(debug=True)
