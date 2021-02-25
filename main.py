import os
import pathlib
import re
import sys

from src import measure


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

    print(scanning_directory)
    argument_table = {k.lower(): os.environ[k] for k in os.environ if not k.lower().startswith("github")}
    result = measure.measure(scanning_directory, argument_table)
    print()
    print("Result")
    print("------")
    for file in result:
        file_path = file.path.replace(root_dir, "", 1).replace(os.sep, "", 1)
        file_path = re.sub(f"\\{os.sep}+", os.sep, file_path)
        print(file_path)
        max_len = max([len(x.caption) for x in file.info_list])
        for info in file.info_list:
            print(f"   {info.caption}{' ' * (max_len - len(info.caption))} | {info.info}")


if __name__ == '__main__':
    main()
