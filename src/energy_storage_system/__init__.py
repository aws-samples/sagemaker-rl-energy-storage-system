from typing import TypeVar

T = TypeVar("T")


def hello_world(s: T) -> T:
    print("Hello world,", s)
    return s
