"""
Expected value -> 7
"""

def main():
    for i in [1, 2, 3, 4, 5]:
        if i == 1 or i == 3 or i == 5:
            print("Yes it's odd")
        elif i == 2 or i == 4:
            print("Great it's even")
        else:
            print("WHAT HAVE YOU DONE")


if __name__ == '__main__':
    main()
