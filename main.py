import json
import os
import sys

import requests

from src import measure
from src.report import generate_report_message


def comment_to_github(text):
    try:
        token = os.environ["INPUT_TOKEN"]
        event = os.environ["GITHUB_EVENT_NAME"]
        api_root = os.environ["GITHUB_API_URL"]

        owner, repo = os.environ["GITHUB_REPOSITORY"].split("/")
        commit = "--- pull request ---"
        pr = -1
        if event == "commit":
            commit = os.environ["GITHUB_SHA"]
        elif event == "pull_request":
            pr = int(os.environ["GITHUB_REF"].split("/")[2])
    except KeyError:
        raise RuntimeError("Necessary environment variables were unavailable; is here in GitHub Actions?")

    header = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    if event == "push":
        res = requests.post(
            f"{api_root}/repos/{owner}/{repo}/commits/{commit}/comments",
            json.dumps({"body": text}),
            headers=header
        )
    elif event == "pull_request":
        res = requests.post(
            f"{api_root}/repos/{owner}/{repo}/issues/{pr}/comments",
            json.dumps({"body": text}),
            headers=header
        )
    else:
        res = None
        print("Unknown event; skipping request.")

    if res is not None and not str(res.status_code).startswith("2"):
        print(f"Failed to post request: {res.status_code}")
        print(res.text)
    else:
        print("Posted request successfully!")


def main():

    if "GITHUB_WORKSPACE" in os.environ:
        root_dir = os.environ["GITHUB_WORKSPACE"]
    else:
        root_dir = os.curdir

    scanning_directory = root_dir
    if len(sys.argv) > 1:
        scanning_directory += os.sep + sys.argv[1]

    scanning_directory += os.sep

    if not os.path.isdir(scanning_directory):
        raise RuntimeError(f"The provided root directory is not found or directory: {scanning_directory}")

    argument_table = {k.lower(): os.environ[k] for k in os.environ if not k.lower().startswith("github")}
    result = measure.measure(scanning_directory, argument_table)

    open_auto = True
    if len(sys.argv) > 2 and sys.argv[2].lower() in ["true", "false"]:
        open_auto = (sys.argv[2].lower() == "true")

    text = generate_report_message(root_dir, result, open_auto)
    if "CI" in os.environ and os.environ["CI"] == "true":
        comment_to_github(text)
    else:
        print()
        print(text)


if __name__ == '__main__':
    main()
