def greeting(name: str) -> str:
    return f"Hello, {name}"

#type data structure
l: list[int] = [1,2, 3, 4, 5]
t: tuple[int, str, float] =(1, "hello", 3.14)
s: set[int] = {1,2,3,4,5}
d: dict[str, int] = {"a":2, "b":2, "c": 3}

#a list with elements of different types
li: list[int | float] = [1, 2.5, 3.14, 5]

#type alias
IntStringFloatTuple = tuple[int, str, float]
tu: IntStringFloatTuple = (1, "hello", 3.14)

#a function arguments or return types that either reutnr a value or NOne
def greet(name: str | None = None) -> str:
    return f"Hello, {name if name else 'Anonymous'}"

#type hints for classes
class Post: 
    def __init__(self, title: str) -> None:
        self.title = title

    def __str__(self) -> str:
        return self.title

posts: list[Post] = [Post("Post A"), Post("Post B")]


#type function signature with Callable
from collections.abc import Callable

ConditionFunction = Callable[[int], bool]

def filter_list(l: list[int], condition: ConditionFunction) -> list[int]:
    return [i for i in l if condition(i)]

def is_even(i:int) -> bool:
    return i % 2 == 0

filter_list([1,2,3,4,5], is_even)

#any and cast
from typing import Any, cast
def f(x: Any) -> Any:
    return x

f("a")
f(10)
f([1,2,3])

a = cast(str, f("a")) # forced type to be str


