"""
类型注解与泛型
运行: python python_learn/10_type_hints/basic_generics.py
"""

from typing import (
    List, Dict, Tuple, Set, Optional, Union, Any,
    TypeVar, Generic, Callable, Iterable, Sequence,
    Mapping, NewType,
)


# ============================================================
# 1. 基础注解
# ============================================================

def greet(name: str, age: int = 18) -> str:
    return f"你好，{name}，你{age}岁了"


# ============================================================
# 2. 集合类型
# ============================================================

def process_items(
    names: List[str],
    scores: Dict[str, int],
    unique_ids: Set[int],
    coordinates: Tuple[float, float],
) -> None:
    pass


# ============================================================
# 3. Optional 和 Union
# ============================================================

def find_user(user_id: int) -> Optional[str]:
    """返回 None 表示未找到"""
    users = {1: "Alice", 2: "Bob"}
    return users.get(user_id)


def parse_value(value: Union[int, str, float]) -> str:
    """接受多种类型"""
    return str(value)


# ============================================================
# 4. TypeVar — 泛型
# ============================================================

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


def first(items: List[T]) -> Optional[T]:
    """泛型函数: 返回列表第一个元素"""
    return items[0] if items else None


def reverse_pair(pair: Tuple[T, V]) -> Tuple[V, T]:
    """反转二元组"""
    return (pair[1], pair[0])


# ============================================================
# 5. TypeVar 加约束
# ============================================================

Number = TypeVar("Number", int, float)


def double(value: Number) -> Number:
    return value * 2


# ============================================================
# 6. Generic — 泛型类
# ============================================================

class Stack(Generic[T]):
    """泛型栈"""
    def __init__(self) -> None:
        self._items: List[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __repr__(self) -> str:
        return f"Stack({self._items})"


# 多类型参数
class MultiKeyDict(Generic[K, V]):
    def __init__(self) -> None:
        self._data: Dict[K, V] = {}

    def set(self, key: K, value: V) -> None:
        self._data[key] = value

    def get(self, key: K) -> Optional[V]:
        return self._data.get(key)


# ============================================================
# 7. Callable
# ============================================================

# Callable[[参数类型...], 返回类型]
Transformer = Callable[[str], str]


def apply_transform(text: str, transform: Transformer) -> str:
    return transform(text)


# ============================================================
# 8. NewType — 新类型
# ============================================================

UserId = NewType("UserId", int)
ProductId = NewType("ProductId", int)


def get_user(user_id: UserId) -> str:
    return f"User({user_id})"


# ============================================================
# 9. 运行验证
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("类型注解是静态检查，运行时不影响。以下只是演示语法正确性。\n")

    # 泛型函数
    print(f"  first([10, 20, 30]) = {first([10, 20, 30])}")
    print(f"  first([]) = {first([])}")

    # 泛型类
    stack = Stack[int]()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    print(f"  Stack[int]: {stack}")
    print(f"  pop(): {stack.pop()}")

    # 多类型参数
    d = MultiKeyDict[str, int]()
    d.set("age", 30)
    print(f"  MultiKeyDict: {d.get('age')}")

    # Callable
    upper: Transformer = lambda s: s.upper()
    print(f"  apply_transform: {apply_transform('hello', upper)}")

    # NewType
    uid: UserId = UserId(42)
    print(f"  get_user: {get_user(uid)}")
