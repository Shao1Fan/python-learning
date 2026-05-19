"""
dataclass 进阶用法
运行: python python_learn/12_dataclasses_and_patterns/dataclass_adv.py
"""

from dataclasses import dataclass, field, InitVar, asdict, astuple, replace
from typing import List, Optional, ClassVar
from enum import Enum


# ============================================================
# 1. 基础 dataclass
# ============================================================

@dataclass
class Person:
    name: str
    age: int
    email: str = ""
    tags: List[str] = field(default_factory=list)


# ============================================================
# 2. field() 高级配置
# ============================================================

@dataclass
class Product:
    name: str
    price: float
    _id: int = field(init=False, repr=False)  # 不传入 init，不显示在 repr 中
    discount: float = field(default=0.0, compare=False)  # 比较时忽略
    metadata: dict = field(default_factory=dict, hash=False)  # hash 时忽略
    _counter: ClassVar[int] = 0  # 类变量，不是字段

    def __post_init__(self):
        """初始化后的处理"""
        Product._counter += 1
        self._id = Product._counter
        if self.price < 0:
            raise ValueError("价格不能为负")


# ============================================================
# 3. frozen=True — 不可变 dataclass
# ============================================================

@dataclass(frozen=True)
class Point:
    x: float
    y: float

    def __post_init__(self):
        # frozen 模式下，__post_init__ 中也不能直接赋值
        pass

    # 需要通过 __setattr__ 绕过（不推荐）
    def move(self, dx, dy):
        return Point(self.x + dx, self.y + dy)


# ============================================================
# 4. InitVar — 初始化参数但不作为字段
# ============================================================

@dataclass
class DatabaseConfig:
    host: str
    port: int = 5432
    db_url: InitVar[str] = None  # 传给 __post_init__，不作为字段

    def __post_init__(self, db_url: Optional[str] = None):
        if db_url:
            parts = db_url.split(":")
            self.host = parts[0]
            self.port = int(parts[1]) if len(parts) > 1 else 5432


# ============================================================
# 5. @dataclass(slots=True) — Python 3.10+
# ============================================================

@dataclass(slots=True)
class SlottedProduct:
    name: str
    price: float
    quantity: int = 0


# ============================================================
# 6. 继承
# ============================================================

@dataclass
class Base:
    created_at: str = ""
    id: int = 0

    def __post_init__(self):
        if not self.created_at:
            from datetime import datetime
            self.created_at = datetime.now().isoformat()

@dataclass
class User(Base):
    name: str = ""
    email: str = ""


# ============================================================
# 7. 嵌套 dataclass & 转换
# ============================================================

@dataclass
class Address:
    city: str
    street: str
    zipcode: str

@dataclass
class Employee:
    name: str
    address: Address
    salary: float


# ============================================================
# 运行演示
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("1. 基础 dataclass")
    p = Person("Alice", 30, tags=["admin", "user"])
    print(f"  {p}")

    print("\n2. field() 高级配置")
    prod = Product("笔记本电脑", 7999.0)
    print(f"  {prod}")
    print(f"  _id = {prod._id}")

    print("\n3. frozen=True")
    pt = Point(1.0, 2.0)
    print(f"  {pt}")
    # pt.x = 3.0  # 报错
    pt2 = pt.move(3, 4)
    print(f"  移动后: {pt2}")

    print("\n4. InitVar")
    cfg = DatabaseConfig(host="", db_url="localhost:3306")
    print(f"  host={cfg.host}, port={cfg.port}")

    print("\n5. slots=True")
    sp = SlottedProduct("手机", 3999, 10)
    # sp.extra = "test"  # 报错

    print("\n6. 继承")
    user = User(id=1, name="Alice", email="alice@example.com")
    print(f"  {user}")

    print("\n7. 嵌套 dataclass & 转换")
    emp = Employee("Bob", Address("北京", "长安街", "100000"), 15000.0)
    print(f"  asdict: {asdict(emp)}")
    print(f"  astuple: {astuple(emp)}")

    # replace — 创建修改后的副本
    emp2 = replace(emp, salary=20000.0)
    print(f"  修改工资: {emp2.salary}")
