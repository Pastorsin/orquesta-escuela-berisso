from flask import render_template
from flask_login import current_user, login_required
from flaskps.helpers.webconfig import get_web_config

from flaskps.models.user import Student


@login_required
def index():
    students = Student.query.all()
    return render_template(
        'student/index.html',
        students=students,
        config=get_web_config(),
        current_user=current_user
    )
