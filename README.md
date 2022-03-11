![PyGitit Log](pygitit/static/img/PyGitit.png)

# PyGitit: a simple wiki

## What is it?

**PyGitit** is a port of the [Gitit](https://github.com/jgm/gitit) project to a python base, implemented from scratch.

This project runs a wiki with the revision backend provided by either [git](https://git-scm.com/) or [mercurial](https://www.mercurial-scm.org/).

## Installation

You can install PyGitit simply by running `pip install .` or `python setup.py install` after downloading

## Running your wiki

The simplest way to run PyGitit is by running the command `pygitit` in your command line after installation. To do this you must first create a `wiki` subfolder of wherever you are running the command, Pygitit will store all your wiki pages in that folder, and will create a git repository there.

Alternatively, you may run `pygitit -s [config_file]`, where the config file must be a json file. You may specify as many or as few of the following options in that file. Options you do not specify will use default values, which are listed in parentheses.

* host ("localhost") - If you want to run the wiki over the network/internet, this should be the ip/url. To run it locally, use "localhost".
* port (7600) - Port on which the wiki should run.
* suffix ("wiki") - Suffix for the stored wiki files.
* extensions (\["toc", "tables"\]) - Python markdown extensions. PyGitit will also automatically add the WikiLinkExtension to enable cross-linking the wiki pages.
* log_file ("stderr") - File for logging PyGitit operations. Can use "stderr" or "stdout" for standard output destinations.
* logo("/static/img/PyGitit.png") - URL of the logo to be used on the wiki.
* root("wiki") - Root folder for the wiki. This is used for both git_root and wiki_root by default.
* git_root(root) - Root folder of the git repository, may be any parent folder of the wiki root.
* wiki_root(root) - Root folder for where to store wiki pages.
* template_root("pygitit.templates") - Root folder(s) for templates. Can be provided as a single folder name or a list of folders. If a list is given, the preference is to the folders earlier in the list. The built-in templates are always included as the last location to look.
* static_root("pygitit.static") - Root folder(s) for static files. Can be provided as a single folder name or a list of folders. If a list is given, the preference is to the folders earlier in the list. The built-in static folder is always included as the last location to look.

## Features

* Standard markdown formatting for wiki pages
* History of page revisions
* Comparison of page revisions
* Ability to view old versions of a page and to revert to them

# Future Planned Features

* Allowing file uploads.
* Add views for a listing of all files, random page, recent changes.
* Improve UI.
* Improve revision comparison page.
* Add categories.
* Add wiki page template support.
* Add page export.