from bottle import run, TEMPLATE_PATH, debug
import pygitit.settings as settings
from pygitit.core_views import edit, revert, history, diff, wiki, wiki_post, wiki_root
from pygitit.util_views import static
import argparse
import json

debug(True)


def main():
    """
    Main wiki loop.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--settings",
        "-s",
        type=argparse.FileType("r"),
        help="setting json file",
    )
    arguments = parser.parse_args()
    if arguments.settings:
        settings.init(json.load(arguments.settings))
    else:
        settings.init()
    
    for t_root in settings.CONFIG["template_root"][::-1]:
        TEMPLATE_PATH.insert(0, t_root)
    run(host=settings.CONFIG["host"], port=settings.CONFIG["port"])


if __name__ == "__main__":
    main()
