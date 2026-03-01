import atexit
from flask import Flask
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from extensions import limiter
from handlers import scheduler_cron
from routes.api_routes import api_blueprint

app = Flask(__name__)
CORS(app, origins=["http://localhost:4200", "http://127.0.0.1:5500", "https://tinosnegocios.com.br"])

limiter.init_app(app)
app.register_blueprint(api_blueprint)

scheduler: BackgroundScheduler = BackgroundScheduler()
scheduler.add_job(
    scheduler_cron.check_expired_user,
    CronTrigger(hour=0, minute=0),
    #CronTrigger(minute="*/1"),
    #CronTrigger(second="*/5"),
)
scheduler.add_job(
   scheduler_cron.check_will_expired_user,
   CronTrigger(hour=1, minute=0),
)

scheduler.start()
atexit.register(lambda: scheduler.shutdown(wait=False))


if __name__ == "__main__":
    app.run()
