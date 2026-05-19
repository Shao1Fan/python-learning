"""
元类实战
运行: python python_learn/05_metaclasses/metaclass_usage.py
"""


# ============================================================
# 1. type() 动态创建类
# ============================================================

def say_hello(self):
    return f"你好，我是 {self.name}"

# 等价于:
# class Person:
#     def __init__(self, name):
#         self.name = name
#     def say_hello(self): ...
Person = type("Person", (), {
    "__init__": lambda self, name: setattr(self, "name", name),
    "say_hello": say_hello,
})


# ============================================================
# 2. 自定义元类
# ============================================================

class DebugMeta(type):
    """元类: 打印所有类创建的过程"""
    def __new__(mcs, name, bases, namespace):
        print(f"[DebugMeta] 正在创建类: {name}")
        print(f"  基类: {bases}")
        print(f"  命名空间: {[k for k in namespace if not k.startswith('__')]}")
        return super().__new__(mcs, name, bases, namespace)

    def __init__(cls, name, bases, namespace):
        print(f"[DebugMeta] 初始化类: {name}")
        super().__init__(name, bases, namespace)


class MyBase(metaclass=DebugMeta):
    pass


class MyChild(MyBase):
    def foo(self):
        pass

    def bar(self):
        pass


# ============================================================
# 3. 元类实现单例模式
# ============================================================

class SingletonMeta(type):
    """单例元类"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    def __init__(self):
        print("  Database.__init__() 被调用")
        self.connected = False

    def connect(self):
        self.connected = True


# ============================================================
# 4. 元类实现 ORM-like 字段校验
# ============================================================

class Field:
    def __init__(self, name, field_type, required=True):
        self.name = name
        self.field_type = field_type
        self.required = required


class ModelMeta(type):
    """自动校验 Model 子类的字段定义"""
    def __new__(mcs, name, bases, namespace):
        if name == "Model":
            return super().__new__(mcs, name, bases, namespace)

        fields = {}
        for key, value in list(namespace.items()):
            if isinstance(value, Field):
                fields[key] = value
                del namespace[key]

        namespace["_fields"] = fields
        cls = super().__new__(mcs, name, bases, namespace)

        print(f"[ModelMeta] 注册模型: {name}, 字段: {list(fields.keys())}")
        return cls


class Model(metaclass=ModelMeta):
    def __init__(self, **kwargs):
        for name, field in self._fields.items():
            value = kwargs.get(name)
            if value is None and field.required:
                raise ValueError(f"{name} 是必填字段")
            setattr(self, name, value)

    def validate(self):
        for name, field in self._fields.items():
            value = getattr(self, name)
            if value is None and not field.required:
                continue
            if not isinstance(value, field.field_type):
                raise TypeError(
                    f"字段 {name} 期望 {field.field_type.__name__}, "
                    f"得到 {type(value).__name__}"
                )
        return True

    def __repr__(self):
        pairs = [f"{k}={getattr(self, k, None)}" for k in self._fields]
        return f"{self.__class__.__name__}({', '.join(pairs)})"


class User(Model):
    name = Field("name", str)
    age = Field("age", int)
    email = Field("email", str, required=False)


# ============================================================
# 5. 元类实现自动注册
# ============================================================

class RegistryMeta(type):
    """自动注册所有子类"""
    registry = {}

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        if name != "BasePlugin":
            mcs.registry[name] = cls
            print(f"[Registry] 注册插件: {name}")
        return cls


class BasePlugin(metaclass=RegistryMeta):
    def process(self, data):
        raise NotImplementedError


class JsonPlugin(BasePlugin):
    def process(self, data):
        return {"type": "json", "data": data}


class XmlPlugin(BasePlugin):
    def process(self, data):
        return {"type": "xml", "data": data}


# ============================================================
# 运行演示
# ============================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("1. type() 动态创建类")
    p = Person("Alice")
    print(f"  {p.say_hello()}")

    print("\n2. 自定义元类（已在上方触发生效）")

    print("\n3. 单例元类")
    db1 = Database()
    db2 = Database()
    print(f"  db1 is db2: {db1 is db2}")

    print("\n4. ORM-like 字段校验")
    user = User(name="Alice", age=30)
    print(f"  {user}")
    print(f"  validate: {user.validate()}")
    try:
        User(name="Bob", age="二十")  # 类型错误
    except TypeError as e:
        print(f"  类型校验失败: {e}")

    print("\n5. 自动注册插件")
    print(f"  注册表: {RegistryMeta.registry}")
    for name, plugin_cls in RegistryMeta.registry.items():
        print(f"  - {name}: {plugin_cls}")
