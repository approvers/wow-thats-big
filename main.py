import os
import sys

from src import measure
from src.report import generate_report_message


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

    print()
    print(generate_report_message(root_dir, result, open_auto))


if __name__ == '__main__':
    main()
