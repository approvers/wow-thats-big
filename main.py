import os
import sys

from src import measure
from src.report import generate_report_message


def main():

    environment_keys = os.environ.keys()
    max_length = max([len(x) for x in environment_keys])

    print("--- Provided Environment Variables List ---")
    for env in os.environ.keys():
        print(f"  {env}{' ' * (max_length - len(env))} : {os.environ[env]}")

    return

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
