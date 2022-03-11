from bottle import route, static_file
import pygitit.settings as settings
import os.path


@route("/static/<name:path>")
def static(name):
    """
    Renders static contents.
    """

    for s_root in settings.CONFIG["static_root"]:
        if os.path.exists(os.path.join(s_root, name)):
            return static_file(name, s_root)
