from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from flaskps.helpers.webconfig import get_web_config
from flaskps.helpers.constraints import permissions_enabled
from datetime import datetime

from flaskps.models.school_year import SchoolYear
from flaskps.models.student_workshop import StudentWorkshop

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
def register_assistance(school_year, workshop):
    students = StudentWorkshop.get_students(school_year,workshop)
    return render_template(
        'assistance/register_assistance.html',
        current_user=current_user,
        current_schoolyear=current_schoolyear,
        workshop=workshop,
        students=students
    )