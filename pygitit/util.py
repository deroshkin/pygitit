from os.path import relpath
from markdown import markdown
from sys import stderr, stdout
import pygitit.settings as settings


def render(fname, rev=None):
    """
    Markdown renders the desired revision (defaults to the most recent) of the given file.
    """

    data = fetch(fname, rev)

    if data:
        return markdown(data, extensions=settings.CONFIG["extensions"])
    else:
        return "Invalid commit for this file"


def fetch(fname, rev=None):
    """
    Fetch the desired revision (defaults to the most recent) of the given file.
    """

    if rev:
        try:
            rel_fname = relpath(fname, settings.CONFIG["git_root"])
            data = settings.REPO.file_rev(rel_fname, rev)
            return data
        except:
            return None
    else:
        with open(fname, "r") as f:
            data = f.read()
        return data


def save(fname, data, commit_msg):
    """
    Saves and commits a new revision of a file with the given contents and commit message.
    """

    with open(fname, "w") as f:
        f.write(data)

    rel_fname = relpath(fname, settings.CONFIG["git_root"])

    settings.REPO.commit(commit_msg, rel_fname)

    log(**{"op": "commit", "file": fname, "message": commit_msg})


def log(**kwargs):
    """
    Logs the operations to the configured log file (can also be stderr/stdout or None to not log anything).
    """

    log_fname = settings.CONFIG["log_file"]
    if log_fname == stderr or stdout:
        log_fname.write(str(kwargs))
    elif log_fname:
        with open(log_fname, "a") as f:
            f.write(str(kwargs))
