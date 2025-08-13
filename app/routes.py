from flask import Blueprint, request, jsonify
from worker import run_job
from db import session_local
from models import JobResult

routes = Blueprint('routes', __name__)

@routes.route('/jobs', methods=['POST'])

def create_job():

    data = request.json
    job_name = data.get("job_name")
    job_data = data.get("data", {})

    if not job_name:
        return jsonify({"error": "Job name is required!"}), 400

    task = run_job.delay(job_name, job_data)

    return jsonify({"message": "Job queued!", "task_id": task.id}), 202

@routes.route('/jobs/results', methods=['GET'])

def get_all_results():

    with session_local() as session:

        results = session.query(JobResult).order_by(JobResult.created_at.desc()).all()

        return jsonify([
            {

                "id": r.id,
                "job_name": r.job_name,
                "status": r.status,
                "created_at": r.created_at.isoformat()

            }

            for r in results
        ])

@routes.route('/jobs/results/<int:id>', methods=['GET'])

def get_result(id):

    with session_local() as session:

        job_result = session.query(JobResult).filter(JobResult.id == id).first()

        if not job_result:
            return jsonify({"error": "Job result not found"}), 404
        
        return jsonify({

            "id": job_result.id,
            "job_name": job_result.job_name,
            "status": job_result.status,
            "result": job_result.result,
            "created_at": job_result.created_at.isoformat()
            
        })
