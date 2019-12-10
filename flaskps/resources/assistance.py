from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from flaskps.helpers.webconfig import get_web_config
from flaskps.helpers.constraints import permissions_enabled
from datetime import datetime

from flaskps.models.school_year import SchoolYear
from flaskps.models.student_workshop import school_year_workshop_student
from flaskps.models.assistance_student_workshop import AssistanceStudentWorkshop
from flaskps.models.student import Student

@login_required
@permissions_enabled('assistance_register', current_user)
def index():
    current_schoolyear = SchoolYear.get_current_schoolyear()
    return render_template(
        'assistance/index.html',
        current_user=current_user,
        current_schoolyear=current_schoolyear,
        workshops=current_schoolyear.workshops
    )

@login_required
@permissions_enabled('assistance_register', current_user)
def register_assistance(schoolyear_id, workshop_id):
    if request.method == 'GET':
        students = [
            {
                'id':'1',
                'first_name':'Julian',
                'last_name':'Almandos'
            },
            {
                'id':'2',
                'first_name':'Andres',
                'last_name':'Milla'
            }
        ]
        return render_template(
            'assistance/register_assistance.html',
            current_user=current_user,
            current_schoolyear=schoolyear_id,
            workshop=workshop_id,
            students=students
        )
    else:
        assistances = request.form.getlist('assistance[]')
        print(assistances)
        students = request.form.getlist('student[]')
        print(students)
        workshop = request.form.get('workshop')
        schoolyear = request.form.get('schoolyear')
        for student,assistance in zip(students,assistances):
            AssistanceStudentWorkshop.create({
                'student_id':student,
                'workshop_id':workshop,
                'schoolyear_id':schoolyear,
                'date':datetime.now()
            })
        return url_for('assistance_list')