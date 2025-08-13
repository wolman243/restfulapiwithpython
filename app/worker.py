from celery import Celery

from db import session_local
from models import JobResult

celery_app = Celery(

    "worker",
    broker="amqp://guest:guest@rabbitmq//",
    backend="redis://redis:6379/0",

)

@celery_app.task(bind=True)

def run_job(self, job_name, data):

    if job_name == "os_command":
        from jobs.os_command_job import run_os_command
        
        result = run_os_command(data)

    elif job_name == "katana_crawl":
        from jobs.katana_crawl_job import run_katana_crawl

        url = data.get("url", "")
        result = run_katana_crawl(url)

    else:
        result = {"status": "error", "message": "Job not found!"}

    with session_local() as session:

        job_result = JobResult(

            job_name=job_name,
            status=result.get("status", "error"),
            result=str(result)

        )

        session.add(job_result)

        session.commit()
        
        session.refresh(job_result)

    return {"job_result_id": job_result.id, "result": result}