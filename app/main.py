from flask import Flask, jsonify, request
from routes import routes
from worker import run_job
from db import session_local, Base, engine
from models import JobResult

app = Flask(__name__)

app.register_blueprint(routes)
Base.metadata.create_all(bind=engine)

@app.route('/')

def index():
    return jsonify({"message": "RESTful API is successfully running!"})


@app.route('/jobs', methods=['GET'])

def get_jobs():

    with session_local() as session:

        jobs = session.query(JobResult).all()

        jobs_data = [
            {
                "id": job.id,
                "job_name": job.job_name,
                "status": job.status,
                "result": job.result
            }

            for job in jobs
        ]
    return jsonify({"jobs": jobs_data})


@app.route('/jobs', methods=['POST'])

def create_job():

    data = request.json
    job_name = data.get("job_name")
    job_data = data.get("data", {})

    if not job_name:
        return jsonify({"error": "Job name is required!"}), 400

    task = run_job.delay(job_name, job_data)

    return jsonify({"message": "Job queued!", "task_id": task.id}), 202


@app.route('/jobs/<int:job_id>', methods=['GET'])

def job_detail(job_id):

    with session_local() as session:

        job = session.query(JobResult).filter(JobResult.id == job_id).first()

        if not job:
            return jsonify({"error": "Job not found"}), 404

        job_data = {

            "id": job.id,
            "job_name": job.job_name,
            "status": job.status,
            "result": job.result
            
        }
        
    return jsonify(job_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug = True)