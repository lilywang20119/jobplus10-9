from flask import Blueprint
from flask import render_template
from jobplus.models import Job

from flask_login import login_required


job = Blueprint('job', __name__, url_prefix='/jobs')

@job.route('/<int:job_id>')
def index(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('job.html', job=job)



