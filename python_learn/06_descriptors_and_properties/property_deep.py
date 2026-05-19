"""
描述符与 Property 深入
运行: python python_learn/06_descriptors_and_properties/property_deep.py
"""

import time


# ============================================================
# 1. 手写 @property
# ============================================================

class Property:
    """手写 property 描述符"""
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.doc = doc

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("不可读")
        return self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("不可写")
        self.fset(obj, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("不可删除")
        self.fdel(obj)

    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel)

    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel)


class Person:
    def __init__(self, name):
        self._name = name

    @Property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("name 必须是字符串")
        self._name = value


# ============================================================
# 2. 数据描述符: 类型校验
# ============================================================

class TypedField:
    """类型校验描述符"""
    def __init__(self, name, field_type):
        self.name = name
        self.field_type = field_type

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        if not isinstance(value, self.field_type):
            raise TypeError(
                f"{self.name} 期望 {self.field_type.__name__}, "
                f"得到 {type(value).__name__}"
            )
        obj.__dict__[self.name] = value

    def __delete__(self, obj):
        raise AttributeError("不允许删除")


class Employee:
    name = TypedField("name", str)
    age = TypedField("age", int)
    salary = TypedField("salary", float)

    def __init__(self, name: str, age: int, salary: float):
        self.name = name
        self.age = age
        self.salary = salary

    def __repr__(self):
        return f"Employee(name='{self.name}', age={self.age}, salary={self.salary})"


# ============================================================
# 3. 非数据描述符: @classmethod 原理
# ============================================================

class ClassMethod:
    """手写 classmethod 描述符（非数据描述符）"""
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, objtype=None):
        if objtype is None:
            objtype = type(obj)
        def wrapper(*args, **kwargs):
            return self.func(objtype, *args, **kwargs)
        return wrapper


class MyClass:
    @ClassMethod
    def hello(cls):
        return f"Hello from {cls.__name__}"


# ============================================================
# 4. 延迟计算属性 (lazy property)
# ============================================================

class LazyProperty:
    """延迟计算: 只在第一次访问时计算，之后缓存"""
    def __init__(self, func):
        self.func = func
        self.name = func.__name__

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        value = self.func(obj)
        obj.__dict__[self.name] = value  # 缓存到实例字典
        return value


class DataProcessor:
    def __init__(self, data):
        self.data = data

    @LazyProperty
    def processed(self):
        """耗时的处理: 只执行一次"""
        print("  执行耗时处理...")
        time.sleep(0.2)
        return [x * x for x in self.data]


# ============================================================
# 5. @cached_property (Python 3.8+ functools)
# ============================================================

from functools import cached_property

class Report:
    def __init__(self, data):
        self.data = data

    @cached_property
    def summary(self):
        print("  生成报表摘要...")
        return {
            "count": len(self.data),
            "sum": sum(self.data),
            "avg": sum(self.data) / len(self.data),
        }


# ============================================================
# 6. 属性访问拦截: __getattr__ vs __getattribute__
# ============================================================

class AttributeLogger:
    """记录所有属性访问"""
    def __init__(self):
        self.data = {}

    def __getattribute__(self, name):
        """拦截所有属性访问（包括已存在的）"""
        print(f"[__getattribute__] 访问: {name}")
        return super().__getattribute__(name)

    def __getattr__(self, name):
        """仅拦截不存在的属性"""
        print(f"[__getattr__] 不存在的属性: {name}")
        return f"默认值({name})"

    def __setattr__(self, name, value):
        print(f"[__setattr__] 设置: {name} = {value!r}")
        super().__setattr__(name, value)


# ============================================================
# 运行演示
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("1. 手写 @property")
    p = Person("Alice")
    print(f"  p.name = {p.name}")
    p.name = "Bob"
    print(f"  p.name = {p.name}")

    print("\n2. 类型校验描述符")
    e = Employee("张三", 28, 15000.0)
    print(f"  {e}")
    try:
        Employee("李四", "二十八", 10000.0)
    except TypeError as e:
        print(f"  类型错误: {e}")

    print("\n3. 非数据描述符 (classmethod)")
    print(f"  {MyClass.hello()}")

    print("\n4. LazyProperty")
    dp = DataProcessor([1, 2, 3, 4, 5])
    print(f"  第一次访问 processed: {dp.processed}")
    print(f"  第二次访问 processed: {dp.processed}")

    print("\n5. @cached_property")
    r = Report([1, 2, 3, 4, 5])
    print(f"  第一次: {r.summary}")
    print(f"  第二次: {r.summary}")

    print("\n6. 属性访问拦截")
    a = AttributeLogger()
    a.x = 42  # __setattr__
    print(f"  a.x = {a.x}")  # __getattribute__
    print(f"  a.y = {a.y}")  # __getattr__ (不存在)
