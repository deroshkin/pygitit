from markdown.extensions.wikilinks import WikiLinkExtension
from sys import stderr, stdout
from pygitit.repo import Repo_Wrapper
from importlib.resources import files


def parse_config(config=None):
    """
    Parse the provided config file, for any missing values, use the ones provided in DEFAULTS
    """
    DEFAULTS = {
        "host": "localhost",
        "port": 7600,
        "root": "wiki",
        "suffix": "wiki",
        "home": "Home",
        "extensions": [
            "toc",
            "tables",
        ],
        "log_file": stderr,
        "logo": "/static/img/PyGitit.png",
    }
    global CONFIG
    CONFIG = {}

    # Parse the file if one is provided
    if config:
        CONFIG = config

    # Fill in missing parameters
    for key in DEFAULTS:
        if key not in CONFIG:
            CONFIG[key] = DEFAULTS[key]

    # stdout/stderr handling
    if CONFIG["log_file"] == "stderr":
        CONFIG["log_file"] = stderr
    if CONFIG["log_file"] == "stdout":
        CONFIG["log_file"] = stdout

    # git_root and wiki_root default to root if not provided
    if "git_root" not in CONFIG:
        CONFIG["git_root"] = CONFIG["root"]
    if "wiki_root" not in CONFIG:
        CONFIG["wiki_root"] = CONFIG["root"]

    # append default static and template paths
    # so that the provided static and template files serve as fallback
    # also if only a single path is given, convert to list first

    if "static_root" not in CONFIG:
        CONFIG["static_root"] = []
    elif type(CONFIG["static_root"]) == str:
        CONFIG["static_root"] = [CONFIG["static_root"]]
    CONFIG["static_root"].append(files("pygitit.static"))

    if "template_root" not in CONFIG:
        CONFIG["template_root"] = []
    elif type(CONFIG["template_root"]) == str:
        CONFIG["template_root"] = [CONFIG["template_root"]]
    CONFIG["template_root"].append(files("pygitit.templates"))

    # Add the wikilink extensions of markdown

    CONFIG["extensions"].append(WikiLinkExtension(base_url="/wiki/", end_url=""))


def init(config=None):
    """
    Initialize settings (CONFIG) from provided file and
    initiate connection to the repository (REPO)
    """
    parse_config(config)
    global REPO
    REPO = Repo_Wrapper(CONFIG["git_root"], "git")
