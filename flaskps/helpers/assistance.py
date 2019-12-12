from datetime import datetime

from flaskps.models.school_year import SchoolYear


def valid_assistance_date(**kwargs):
    current_schoolyear = SchoolYear.query.get(
        kwargs.get('schoolyear_id')
    )
    assistance_datetime = datetime.strptime(
        kwargs.get('assistance_date'),
        '%d-%m-%Y'
    )
    return current_schoolyear.is_valid_assistance_date(
        assistance_datetime.date(),
        kwargs.get('workshop_id'),
        kwargs.get('schoolyear_id')
    )
