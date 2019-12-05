from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required

from flaskps.models.instrument import Instrument
from flaskps.models.instrument_type import InstrumentType
from flaskps.helpers.instrument import InstrumentCreateForm


def new():
    if request.method == 'POST':
        form = InstrumentCreateForm(request)

        if form.is_valid():
            form.save()
            flash(form.success_message(), 'success')
            return redirect(form.success_url())
        else:
            for error in form.error_messages():
                flash(error, 'danger')
            return render_template(
                'instrument/new.html',
                instrument=form.values(),
                instrument_types=InstrumentType.query.all()
            )

    else:
        return render_template(
            'instrument/new.html',
            instrument=None,
            instrument_types=InstrumentType.query.all()
        )


def index():
    return render_template(
        'instrument/index.html',
        instruments=Instrument.query.order_by(Instrument.inventory_number)
    )
