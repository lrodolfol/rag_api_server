from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta


def enviar_mensagem(phone_number: str):
    print(f"[{datetime.now()}] finalizando chat do numero: {phone_number}")


class SchedulerChats:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SchedulerChats, cls).__new__(cls)
            cls._instance._init_scheduler()
        return cls._instance

    def _init_scheduler(self):
        self.logger = SchedulerChats(SchedulerChats, "INFO")
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

    def finish_chat(self, phone_number: str):
        job_id = f"job_{phone_number}"
        time = datetime.now() + timedelta(minutes=30)

        try:
            self.scheduler.reschedule_job(job_id, trigger="date", run_date=time)
        except Exception:
            try:
                self.scheduler.add_job(
                    enviar_mensagem,
                    "date",
                    run_date=time,
                    id=job_id,
                    args=[phone_number],
                )
            except Exception as e:
                print(f"Error adding job: {e}")
