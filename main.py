import os
import sys

from src import measure
from src.report import generate_report_message

from octokit import Octokit


def comment_to_github(text):
    try:
        token = os.environ["INPUT_TOKEN"]
        event = os.environ["GITHUB_EVENT_NAME"]

        owner, repo = os.environ["GITHUB_REPOSITORY"].split("/")
        commit = "--- pull request ---"
        pr = -1
        if event == "commit":
            commit = os.environ["GITHUB_SHA"]
        elif event == "pull_request":
            pr = int(os.environ["GITHUB_REF"].split("/")[2])
    except KeyError:
        raise RuntimeError("Necessary environment variables were unavailable; is here in GitHub Actions?")

    kit = Octokit(token=token)

    if event == "commit":
        kit.repos.create_commit_comment(owner=owner, repo=repo, commit_sha=commit, body=text)
    elif event == "pull_request":
        kit.issues.create_comment(owner=owner, repo=repo, issue_number=pr, body=text)


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
