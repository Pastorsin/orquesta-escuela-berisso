from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from flaskps.helpers.webconfig import get_web_config
from flaskps.helpers.constraints import permissions_enabled
from datetime import datetime

from flaskps.models.school_year import SchoolYear
from flaskps.models.student_workshop import StudentWorkshop
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
        workshops=current_schoolyear.get_remaining_workshops()
    )

@login_required
@permissions_enabled('assistance_register', current_user)
def register_assistance(schoolyear_id, workshop_id):
    if request.method == 'GET':
        students_ids = StudentWorkshop.get_students_doing_workshop(schoolyear_id,workshop_id)
        students = []
        for student_id in students_ids:
            students.append(Student.query.get(student_id))
        
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
                'date':datetime.now().date(),
                'assistance':assistance
            })
        return redirect(url_for('assistance_list'))