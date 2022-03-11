# A wrapper for multiple repository types

from datetime import datetime


class __Git_Repo:
    def __init__(self, root):
        from git import Repo, InvalidGitRepositoryError

        try:
            self.repo = Repo(root)
        except InvalidGitRepositoryError:
            self.repo = Repo.init(root)
        except:
            raise Exception(f"Unable to open or create git repository at {root}")

    def file_rev(self, fname, rev):
        # Get the contents of the rev version of the file fname

        commit = self.repo.commit(rev)
        target = commit.tree / fname
        return target.data_stream.read().decode()

    def commit(self, commit_msg, *fnames):
        for fname in fnames:
            self.repo.index.add(fname)
        self.repo.index.commit(commit_msg)

    def versions(self, fname):
        return [
            {
                "date": commit.committed_datetime.date().isoformat(),
                "time": commit.committed_datetime.time().isoformat(),
                "author": commit.author.name,
                "hex": commit.hexsha,
                "message": commit.message,
            }
            for commit in self.repo.iter_commits(paths=fname)
        ]


class __Hg_Repo:
    def __init__(self, root):
        from mercurial import ui, hg

        try:
            self.repo = hg.repository(ui.ui(), str.encode(root), create=True)
        except:
            raise Exception(f"Unable to open or create mercurial repository at {root}")

    def file_rev(self, fname, rev):
        fc = self.repo.filectx(str.encode(fname), rev)
        return fc.rawdata().decode()

    def versions(self, fname):
        results = []
        log = self.repo.file(str.encode(fname))
        for i in log.revs():
            fc = self.repo.filectx(str.encode(fname), log.linkrev(i))
            dt = datetime.utcfromtimestamp(int(fc.date()[0]))
            results.append(
                {
                    "date": dt.date().isoformat(),
                    "time": dt.time().isoformat() + " (UTC)",
                    "author": fc.user().decode(),
                    "hex": fc.hex().decode(),
                    "message": fc.changectx().description().decode(),
                }
            )
        results.reverse()
        return results

    def commit(self, commit_msg, *fnames):
        from mercurial import commands, ui

        commands.commit(
            ui.ui(),
            self.repo,
            *[self.repo.pathto(str.encode(fname)) for fname in fnames],
            message=str.encode(commit_msg),
            user=b"Anonymous",
        )


def Repo_Wrapper(root, system):
    if system == "git":
        return __Git_Repo(root)
    elif system == "hg":
        return __Hg_Repo(root)
