import sys
import getopt
import datetime
from typing import List, Dict, Any
from ghapi.all import GhApi
from decouple import config

USAGE = f"Usage: python {sys.argv[0]} " \
        f"[--help] | [-o <owner>] [-r <repositories,as,csv>] [-s <start YYYY/MM/DD>] [-e <end YYYY/MM/DD>]"
GH_TOKEN = config("GITHUB_TOKEN")


def parse(args: List[str]) -> Dict[str, Any]:
    options, _ = getopt.getopt(
        args,
        "ho:r:s:e",
        ["help", "owner=", "repositories=", "start=", "end"]
    )
    args = dict()
    for o, v in options:
        if o in ("-h", "--help"):
            print(USAGE)
            sys.exit()
        if o in ("-o", "--owner"):
            args["owner"] = v
        if o in ("-r", "--repositories"):
            repos = v.split(",")
            args["repositories"] = []
            for repo in repos:
                args["repositories"].append(repo)
        if o in ("-s", "--start"):
            date = datetime.datetime.strptime(v, "%Y/%m/%d")
            args["start"] = date
        if o in ("-e", "--end"):
            date = datetime.datetime.strptime(v, "%Y/%m/%d")
            args["end"] = date
    if "end" not in args.keys():
        args["end"] = datetime.datetime.now()
    return args


def get_releases(args: Dict[str, Any]):
    owner = args["owner"]
    release_notes = dict()
    for repo in args["repositories"]:
        release_notes[repo] = []
        api = GhApi(owner=owner, repo=repo, token=GH_TOKEN)
        resp = api.repos.list_releases()
        #  published_at: 2021-11-17T21:30:45Z
        for release in resp:
            published_at = datetime.datetime.strptime(release.published_at, "%Y-%m-%dT%H:%M:%SZ")
            if args["end"] > published_at > args["start"]:
                release_notes[repo].append(release.body)
    with open("RELEASE-NOTES.md", "r+") as f:
        for repo in release_notes.keys():
            f.write(f"# {repo}\n\n")
            for release in release_notes[repo]:
                f.write(f"{release}\n\n")
            f.flush()
            # "reset" fd to the beginning of the file
            f.seek(0)
        data = f.read()
    start = args['start'].strftime('%Y-%m-%d')
    end = args['end'].strftime('%Y-%m-%d')
    description = f"Release notes for {start} - {end}"
    api = GhApi(token=GH_TOKEN)
    api.gists.create(description=description, files={f'RELEASE_NOTES_{end}.md': dict(content=data)}, public=False)


def main():
    args = sys.argv[1:]
    if not args:
        raise SystemExit(USAGE)
    args = parse(args)
    get_releases(args)


if __name__ == '__main__':
    main()
