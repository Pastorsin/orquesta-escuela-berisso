from flaskps.models.webconfig import Webconfig
from .form import Form


def get_web_config():
    return Webconfig.query.first()


class WebconfigForm(Form):

    def __init__(self, form):
        super(WebconfigForm, self).__init__(form)
        self.frontend_enabled = 'frontend_enabled' in form

    def success_message(self):
        return 'Configuración establecida con éxito'

    @property
    def values(self):
        self.fields['frontend_enabled'] = self.frontend_enabled
        return self.fields
