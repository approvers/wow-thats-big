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

    if len(sys.argv) > 1:
        root_dir = root_dir + os.sep + sys.argv[1]

    root_dir += os.sep
    root_dir = re.sub(f"\\{os.sep}+", os.sep, root_dir)

    if not os.path.isdir(root_dir):
        raise RuntimeError(f"The provided root directory is not found or directory: {root_dir}")

    argument_table = {k.lower(): os.environ[k] for k in os.environ if not k.lower().startswith("github")}
    result = measure.measure(root_dir, argument_table)
    print()
    print("Result")
    print("------")

    for file in result:
        print(file.path)
        max_len = max([len(x.caption) for x in file.info_list])
        for info in file.info_list:
            print(f"   {info.caption}{' ' * (max_len - len(info.caption))} | {info.info}")


if __name__ == '__main__':
    main()
