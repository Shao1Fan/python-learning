"""
结构模式匹配 (Python 3.10+)
运行: python python_learn/12_dataclasses_and_patterns/structural_pattern.py
"""

from dataclasses import dataclass
from typing import Union


# ============================================================
# 1. 基础 match/case
# ============================================================

def match_number(value):
    match value:
        case 0:
            return "零"
        case 1:
            return "一"
        case n if n < 0:
            return f"负数: {n}"
        case n:
            return f"正数: {n}"


# ============================================================
# 2. 匹配序列
# ============================================================

def match_sequence(data):
    match data:
        case []:
            return "空列表"
        case [x]:
            return f"单元素: {x}"
        case [x, y]:
            return f"两个元素: {x}, {y}"
        case [first, *rest]:
            return f"首个: {first}, 其余: {rest}"
        case _:
            return "未知格式"


# ============================================================
# 3. 匹配字典
# ============================================================

def match_dict(data):
    match data:
        case {"type": "user", "name": name, "age": age}:
            return f"用户: {name}, {age}岁"
        case {"type": "product", "name": name, "price": price}:
            return f"商品: {name}, ¥{price}"
        case {"type": msg}:
            return f"未知类型: {msg}"
        case _:
            return "无效数据"


# ============================================================
# 4. 匹配 dataclass
# ============================================================

@dataclass
class User:
    name: str
    role: str
    age: int = 0

@dataclass
class Admin:
    name: str
    level: int

def match_user(obj):
    match obj:
        case User(name=name, role="admin"):
            return f"管理员 {name}"
        case User(name=name, role=role):
            return f"普通用户 {name} (角色={role})"
        case Admin(name=name, level=level) if level >= 5:
            return f"高级管理员 {name}"
        case Admin(name=name):
            return f"管理员 {name}"
        case _:
            return "未知身份"


# ============================================================
# 5. 匹配类型 + 守卫
# ============================================================

def match_type(value):
    match value:
        case int() | float() as n:
            return f"数字: {n}"
        case str() as s:
            return f"字符串: {s}"
        case bytes() as b:
            return f"字节: {b.hex()}"
        case _:
            return f"其他类型: {type(value).__name__}"


# ============================================================
# 6. 匹配枚举
# ============================================================

from enum import Enum

class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"

def match_color(color):
    match color:
        case Color.RED:
            return "红色"
        case Color.GREEN:
            return "绿色"
        case Color.BLUE:
            return "蓝色"
        case _:
            return "未知颜色"


# ============================================================
# 7. OR 模式
# ============================================================

def match_or(value):
    match value:
        case 0 | 1 | 2:
            return "小数字 (0-2)"
        case 3 | 4 | 5:
            return "中等数字 (3-5)"
        case _ as n:
            return f"其他: {n}"


# ============================================================
# 运行演示
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("1. 基础匹配")
    print(f"  match_number(0) = {match_number(0)}")
    print(f"  match_number(-5) = {match_number(-5)}")
    print(f"  match_number(42) = {match_number(42)}")

    print("\n2. 序列匹配")
    print(f"  match_sequence([]) = {match_sequence([])}")
    print(f"  match_sequence([1]) = {match_sequence([1])}")
    print(f"  match_sequence([1, 2]) = {match_sequence([1, 2])}")
    print(f"  match_sequence([1, 2, 3, 4]) = {match_sequence([1, 2, 3, 4])}")

    print("\n3. 字典匹配")
    print(f"  match_dict({{'type': 'user', 'name': 'Alice', 'age': 30}}) = {match_dict({'type': 'user', 'name': 'Alice', 'age': 30})}")
    print(f"  match_dict({{'type': 'product', 'name': '手机', 'price': 3999}}) = {match_dict({'type': 'product', 'name': '手机', 'price': 3999})}")

    print("\n4. dataclass 匹配")
    print(f"  match_user(User('Alice', 'admin')) = {match_user(User('Alice', 'admin'))}")
    print(f"  match_user(User('Bob', 'user')) = {match_user(User('Bob', 'user'))}")
    print(f"  match_user(Admin('Charlie', 5)) = {match_user(Admin('Charlie', 5))}")

    print("\n5. 类型匹配")
    print(f"  match_type(42) = {match_type(42)}")
    print(f"  match_type('hello') = {match_type('hello')}")
    print(f"  match_type(b'data') = {match_type(b'data')}")

    print("\n6. 枚举匹配")
    print(f"  match_color(Color.RED) = {match_color(Color.RED)}")

    print("\n7. OR 模式")
    print(f"  match_or(1) = {match_or(1)}")
    print(f"  match_or(4) = {match_or(4)}")
    print(f"  match_or(9) = {match_or(9)}")
