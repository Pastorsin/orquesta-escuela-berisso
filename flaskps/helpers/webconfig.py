from ..models.webconfig import Webconfig

def web_config():
    return Webconfig.query.first()