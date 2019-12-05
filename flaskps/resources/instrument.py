from base64 import b64encode
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required

from flaskps.models.instrument import Instrument
from flaskps.models.instrument_type import InstrumentType
from flaskps.helpers.instrument import InstrumentCreateForm

SUCCESS_MSG = {
    'deactivate': 'Instrumento desactivado correctamente',
    'activate': 'Instrumento activado correctamente'
}


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


def deactivate(instrument_id):
    instrument = Instrument.query.get(instrument_id)
    instrument.deactivate()
    flash(SUCCESS_MSG['deactivate'], 'success')
    return redirect(url_for('instrument_index'))


def activate(instrument_id):
    instrument = Instrument.query.get(instrument_id)
    instrument.activate()
    flash(SUCCESS_MSG['activate'], 'success')
    return redirect(url_for('instrument_index'))


def profile(instrument_id):
    instrument = Instrument.query.get(instrument_id)
    image = b64encode(instrument.image).decode("utf-8")
    return render_template(
        'instrument/profile.html',
        instrument=instrument,
        image=image
    )
