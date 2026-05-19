"""
高级类型注解
运行: python python_learn/10_type_hints/advanced_typing.py
"""

from typing import (
    Protocol, TypedDict, Literal, Final,
    overload, runtime_checkable,
    Any, TypeVar, ClassVar,
)
from enum import Enum, auto
from datetime import datetime


# ============================================================
# 1. Protocol — 结构子类型（鸭子类型）
# ============================================================

@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> str:
        ...


class Circle:
    def draw(self) -> str:
        return "绘制圆形"


class Square:
    def draw(self) -> str:
        return "绘制正方形"


class NotDrawable:
    pass


def render(obj: Drawable) -> None:
    print(f"  渲染: {obj.draw()}")


# ============================================================
# 2. TypedDict — 结构化字典
# ============================================================

class UserDict(TypedDict):
    name: str
    age: int
    email: str


class EmployeeDict(UserDict):
    salary: float


def process_user(user: UserDict) -> str:
    return f"{user['name']} ({user['age']}岁)"


# ============================================================
# 3. Literal — 字面量类型
# ============================================================

def set_mode(mode: Literal["read", "write", "append"]) -> str:
    return f"模式设置为: {mode}"


# ============================================================
# 4. Final — 常量
# ============================================================

MAX_RETRIES: Final = 3
DEFAULT_TIMEOUT: Final[float] = 30.0


# ============================================================
# 5. @overload — 函数重载
# ============================================================

@overload
def process(value: int) -> int:
    ...

@overload
def process(value: str) -> str:
    ...

@overload
def process(value: list) -> list:
    ...

def process(value: Any) -> Any:
    """根据输入类型返回不同结果"""
    if isinstance(value, int):
        return value * 2
    elif isinstance(value, str):
        return value.upper()
    elif isinstance(value, list):
        return [x * 2 for x in value]
    return value


# ============================================================
# 6. ClassVar — 类变量
# ============================================================

class Config:
    default_host: ClassVar[str] = "localhost"
    default_port: ClassVar[int] = 8080

    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port


# ============================================================
# 7. Enum + Literal
# ============================================================

class Status(Enum):
    PENDING = auto()
    RUNNING = auto()
    DONE = auto()
    FAILED = auto()


def get_status_text(status: Status) -> str:
    mapping = {
        Status.PENDING: "待处理",
        Status.RUNNING: "运行中",
        Status.DONE: "已完成",
        Status.FAILED: "失败",
    }
    return mapping[status]


# ============================================================
# 8. TypeAlias (Python 3.10+)
# ============================================================

from typing import TypeAlias

JSON: TypeAlias = dict[str, Any]
JSONList: TypeAlias = list[JSON]


def parse_json(data: str) -> JSON:
    import json
    return json.loads(data)


# ============================================================
# 运行验证
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("1. Protocol — 结构子类型")
    render(Circle())
    render(Square())
    # render(NotDrawable())  # 静态类型检查会报错
    print(f"  Circle 实现了 Drawable? {isinstance(Circle(), Drawable)}")

    print("\n2. TypedDict")
    user: UserDict = {"name": "Alice", "age": 30, "email": "alice@example.com"}
    print(f"  {process_user(user)}")

    print("\n3. Literal")
    print(f"  {set_mode('read')}")
    # set_mode('delete')  # 类型检查报错

    print("\n4. Final — 修改会警告")
    print(f"  MAX_RETRIES = {MAX_RETRIES}")
    # MAX_RETRIES = 5  # mypy/pyright 会报错

    print("\n5. @overload")
    print(f"  process(10)     = {process(10)}")
    print(f"  process('abc')  = {process('abc')}")
    print(f"  process([1,2])  = {process([1,2])}")

    print("\n6. ClassVar")
    print(f"  Config.default_host = {Config.default_host}")

    print("\n7. Enum")
    print(f"  Status.RUNNING = {get_status_text(Status.RUNNING)}")
