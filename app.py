import atexit

from flask import Flask
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from extensions import limiter
from routes.api_routes import api_blueprint

app = Flask(__name__)
CORS(app, origins=["http://localhost:4200", "http://127.0.0.1:5500", "https://tinosnegocios.com.br"])

limiter.init_app(app)
app.register_blueprint(api_blueprint)


def print_daily_greeting() -> None:
    print("ola mundo")


scheduler: BackgroundScheduler = BackgroundScheduler()
scheduler.add_job(
    print_daily_greeting,
    CronTrigger(hour=0, minute=0),
)
scheduler.start()
atexit.register(lambda: scheduler.shutdown(wait=False))


if __name__ == "__main__":
    app.run()
