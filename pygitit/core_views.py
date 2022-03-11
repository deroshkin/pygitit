from typing import Any
from bottle import redirect, route, request, Jinja2Template, template, post
from os.path import isfile, join, relpath
import pygitit.settings as settings
from pygitit.util import save, fetch, render
import difflib


@route("/edit/<name:path>")
def edit(name: str) -> Any:
    """
    Wiki edit view.
    """

    if isfile(
        join(settings.CONFIG["wiki_root"], name + "." + settings.CONFIG["suffix"])
    ):
        fname = join(
            settings.CONFIG["wiki_root"], name + "." + settings.CONFIG["suffix"]
        )
        with open(fname, "r") as f:
            data = f.read()
    else:
        data = ""
    return template(
        "edit.html",
        name=name,
        raw_data=data,
        logo=settings.CONFIG["logo"],
        template_adapter=Jinja2Template,
    )


@route("/revert/<name:path>")
def revert(name):
    """
    Revert the wiki page to an earlier revision, which is passed as the query "revision" parameter. Returns `None` if no revision is passed.
    """

    if "revision" not in request.query or not request.query["revision"]:
        return None
    else:
        rev = request.query["revision"]
        fname = join(
            settings.CONFIG["wiki_root"], name + "." + settings.CONFIG["suffix"]
        )
        rel_fname = relpath(fname, settings.CONFIG["git_root"])
        data = settings.REPO.file_rev(rel_fname, rev)
        save(fname, data, f"Reverting {name} to revision {rev[:7]}")
        redirect(f"/wiki/{name}")


@route("/history/<name:path>")
def history(name):
    """
    History view for a wiki page.
    """

    if isfile(
        join(settings.CONFIG["wiki_root"], name + "." + settings.CONFIG["suffix"])
    ):
        fname = join(
            settings.CONFIG["wiki_root"], name + "." + settings.CONFIG["suffix"]
        )
        rel_fname = relpath(fname, settings.CONFIG["git_root"])
    else:
        return template(
            "dne.html",
            name=name,
            logo=settings.CONFIG["logo"],
            template_adapter=Jinja2Template,
        )
    rev_data = settings.REPO.versions(rel_fname)
    return template(
        "history.html",
        name=name,
        revisions=rev_data,
        logo=settings.CONFIG["logo"],
        template_adapter=Jinja2Template,
        diff_page=f"/diff/{name}",
    )


@route("/diff/<name:path>")
def diff(name):
    """
    Compare two versions of the wiki page.
    """

    if "to" not in request.query or "from" not in request.query:
        return None
    fname = join(settings.CONFIG["wiki_root"], name + "." + settings.CONFIG["suffix"])
    differ = difflib.HtmlDiff()
    new_rev = request.query["to"]
    old_rev = request.query["from"]
    new_md = fetch(fname, new_rev)
    old_md = fetch(fname, old_rev)
    new_lines = new_md.split("\n")
    old_lines = old_md.split("\n")
    diff_table = differ.make_table(old_lines, new_lines)
    return template(
        "diff.html",
        name=name,
        new_rev=new_rev[:7],
        old_rev=old_rev[:7],
        diff_table=diff_table,
        logo=settings.CONFIG["logo"],
        template_adapter=Jinja2Template,
    )


@post("/diff/<name:path>")
def diff_post(name):
    """
    POST version of the diff page, used to request diff from within history
    """

    if isfile(
        join(settings.CONFIG["wiki_root"], name + "." + settings.CONFIG["suffix"])
    ):
        fname = join(
            settings.CONFIG["wiki_root"], name + "." + settings.CONFIG["suffix"]
        )
        rel_fname = relpath(fname, settings.CONFIG["git_root"])
    else:
        return template(
            "dne.html",
            name=name,
            logo=settings.CONFIG["logo"],
            template_adapter=Jinja2Template,
        )
    rev_data = settings.REPO.versions(rel_fname)
    revs = [rev["hex"] for rev in rev_data if rev["hex"] in request.forms]

    request.query["from"] = revs[0]
    request.query["to"] = revs[1]
    return diff(name)


@post("/wiki/<name:path>")
def wiki_post(name):
    """
    POST version of the wiki page, used to submit revisions.
    """

    commit_msg = request.forms.get("commit_msg")
    data = request.forms.get("data")
    fname = join(settings.CONFIG["wiki_root"], name + "." + settings.CONFIG["suffix"])
    save(fname, data, commit_msg)

    return wiki(name)


@route("/wiki/<name:path>")
def wiki(name):
    """
    Primary wiki page view. If "revision" parameter is passed, it will render that revision of the page
    """

    if isfile(
        join(settings.CONFIG["wiki_root"], name + "." + settings.CONFIG["suffix"])
    ):
        fname = join(
            settings.CONFIG["wiki_root"], name + "." + settings.CONFIG["suffix"]
        )
    else:
        return template(
            "dne.html",
            name=name,
            logo=settings.CONFIG["logo"],
            template_adapter=Jinja2Template,
        )

    if "revision" not in request.query or not request.query["revision"]:
        return template(
            "wiki.html",
            name=name,
            fname=fname,
            data=render(fname),
            logo=settings.CONFIG["logo"],
            template_adapter=Jinja2Template,
        )
    else:
        rev = request.query["revision"]
        return template(
            "wiki.html",
            name=name,
            fname=fname,
            data=render(fname, rev=rev),
            logo=settings.CONFIG["logo"],
            rev=rev[:7],
            template_adapter=Jinja2Template,
        )


@route("/wiki")
@route("/wiki/")
@route("/")
def wiki_root():
    """
    Home page view.
    """
    return wiki(settings.CONFIG["home"])
