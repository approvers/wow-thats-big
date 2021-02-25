import os


def main():
    environment_keys = os.environ.keys()
    max_length = max([len(x) for x in environment_keys])

    print("--- Provided Environment Variables List ---")
    for env in os.environ.keys():
        print(f"  {env}{max_length - len(env)} : {os.environ[env]}")


if __name__ == '__main__':
    main()
