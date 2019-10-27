from flaskps.models.webconfig import Webconfig


def get_web_config():
    return Webconfig.query.first()
