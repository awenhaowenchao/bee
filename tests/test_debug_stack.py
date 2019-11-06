from bee.util.debug.stack import *


def foo():
    stack()


def bar():
    foo()


def main():
    bar()


if __name__ == "__main__":
    main()
