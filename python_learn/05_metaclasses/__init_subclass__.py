"""
元类的现代替代方案: __init_subclass__ 与 __set_name__
运行: python python_learn/05_metaclasses/__init_subclass__.py
"""


# ============================================================
# 1. __init_subclass__ — 替代元类的常见场景
# ============================================================

class PluginBase:
    """__init_subclass__ 实现自动注册"""
    registry = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if hasattr(cls, "name"):
            PluginBase.registry[cls.name] = cls
            print(f"[__init_subclass__] 注册插件: {cls.name}")


class PluginA(PluginBase):
    name = "json_format"


class PluginB(PluginBase):
    name = "xml_format"


# ============================================================
# 2. __init_subclass__ 接收关键字参数
# ============================================================

class ValidatedModel:
    """验证器基类"""
    def __init_subclass__(cls, abstract=False, **kwargs):
        super().__init_subclass__(**kwargs)
        if abstract:
            cls._abstract = True
        else:
            cls._abstract = False
            # 检查是否实现了所有必需方法
            for method in getattr(cls, "__required_methods__", []):
                if not hasattr(cls, method) or not callable(getattr(cls, method)):
                    raise TypeError(
                        f"{cls.__name__} 没有实现必需方法: {method}"
                    )
            print(f"[ValidatedModel] {cls.__name__} 验证通过")


class Shape(ValidatedModel, abstract=True):
    __required_methods__ = ["area", "perimeter"]


class Rectangle(Shape):
    def __init__(self, w, h):
        self.w, self.h = w, h

    def area(self):
        return self.w * self.h

    def perimeter(self):
        return 2 * (self.w + self.h)


# ============================================================
# 3. __set_name__ — 描述符自动获取属性名
# ============================================================

class ValidatedField:
    """验证字段描述符 + __set_name__ 自动获取名字"""
    def __set_name__(self, owner, name):
        # 自动获取属性名，无需手动传入
        self.name = name
        print(f"[__set_name__] {owner.__name__}.{name}")

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        self.validate(value)
        obj.__dict__[self.name] = value

    def validate(self, value):
        raise NotImplementedError


class PositiveInt(ValidatedField):
    def validate(self, value):
        if not isinstance(value, int):
            raise TypeError(f"{self.name} 必须是 int")
        if value <= 0:
            raise ValueError(f"{self.name} 必须是正数")


class CharField(ValidatedField):
    def __init__(self, max_length=255):
        self.max_length = max_length

    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError(f"{self.name} 必须是 str")
        if len(value) > self.max_length:
            raise ValueError(f"{self.name} 长度不能超过 {self.max_length}")


class Product:
    """使用 __set_name__ 描述符"""
    price = PositiveInt()
    name = CharField(max_length=50)

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Product(name='{self.name}', price={self.price})"


# ============================================================
# 运行演示
# ============================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("1. __init_subclass__ 自动注册")
    print(f"   注册表: {PluginBase.registry}")

    print("\n2. __init_subclass__ 验证必需方法")
    r = Rectangle(10, 20)
    print(f"   矩形面积: {r.area()}, 周长: {r.perimeter()}")

    print("\n3. __set_name__ 自动获取属性名")
    p = Product("笔记本电脑", 7999)
    print(f"   {p}")
    try:
        Product("手机", -100)
    except ValueError as e:
        print(f"   校验失败: {e}")
