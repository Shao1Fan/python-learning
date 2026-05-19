"""
属性访问魔术方法深入
运行: python python_learn/07_magic_methods/attribute_access.py
"""


# ============================================================
# 1. __getattr__ vs __getattribute__
# ============================================================

class AttrDemo:
    def __init__(self):
        self.name = "Alice"

    def __getattribute__(self, name):
        """拦截所有属性访问（无论存不存在）"""
        print(f"[__getattribute__] 尝试获取: {name}")
        if name == "secret":
            raise AttributeError("secret 被禁止访问")
        return super().__getattribute__(name)

    def __getattr__(self, name):
        """仅当属性不存在时调用"""
        print(f"[__getattr__] '{name}' 不存在，返回默认值")
        return f"默认值({name})"


# ============================================================
# 2. __setattr__ 拦截赋值
# ============================================================

class ReadOnly:
    """只读属性示例"""
    def __init__(self):
        self._data = {}

    def __setattr__(self, name, value):
        if name.startswith("_"):
            super().__setattr__(name, value)
        else:
            raise AttributeError(f"'{name}' 是只读属性")

    def __getattr__(self, name):
        return self._data.get(name)


# ============================================================
# 3. 代理模式
# ============================================================

class Proxy:
    """属性代理: 将属性操作转发给另一个对象"""
    def __init__(self, target):
        self._target = target

    def __getattr__(self, name):
        if name.startswith("_"):
            raise AttributeError(name)
        print(f"[Proxy] 代理获取: {name}")
        return getattr(self._target, name)

    def __setattr__(self, name, value):
        if name.startswith("_"):
            super().__setattr__(name, value)
        else:
            print(f"[Proxy] 代理设置: {name} = {value!r}")
            setattr(self._target, name, value)

    def __delattr__(self, name):
        print(f"[Proxy] 代理删除: {name}")
        delattr(self._target, name)


# ============================================================
# 4. 惰性加载属性
# ============================================================

import json

class LazyLoader:
    """延时加载属性: 只有访问时才计算"""
    def __init__(self, filepath):
        self.filepath = filepath
        self._data = None

    def __getattr__(self, name):
        if self._data is None:
            print(f"[LazyLoader] 首次访问，加载数据...")
            with open(self.filepath, 'r') as f:
                self._data = json.load(f)
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"'{name}' 不存在")

    def __setattr__(self, name, value):
        if name in ("filepath", "_data"):
            super().__setattr__(name, value)
        else:
            if self._data is None:
                self._data = {}
            self._data[name] = value


# ============================================================
# 5. __delattr__ 删除属性拦截
# ============================================================

class Protected:
    def __init__(self):
        self.name = "protected"
        self._secret = "secret value"

    def __delattr__(self, name):
        if name.startswith("_"):
            raise AttributeError(f"不允许删除私有属性: {name}")
        super().__delattr__(name)


# ============================================================
# 运行演示
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("1. __getattr__ vs __getattribute__")
    d = AttrDemo()
    print(f"  d.name = {d.name}")     # __getattribute__ 找到
    print(f"  d.xyz  = {d.xyz}")      # __getattribute__ 没找到 → __getattr__
    try:
        _ = d.secret                  # __getattribute__ 主动抛异常
    except AttributeError as e:
        print(f"  secret访问: {e}")

    print("\n2. __setattr__ 只读")
    r = ReadOnly()
    r._internal = "可以设置"
    print(f"  r._internal = {r._internal}")
    try:
        r.public_attr = "不行"
    except AttributeError as e:
        print(f"  禁止设置: {e}")

    print("\n3. Proxy 代理模式")
    class Data:
        def __init__(self):
            self.key = "value"
            self.num = 42
    original = Data()
    proxy = Proxy(original)
    print(f"  proxy.key = {proxy.key}")
    proxy.new_key = "new value"
    print(f"  original.key = {original.key}")
    print(f"  original.new_key = {original.new_key}")

    print("\n4. 惰性加载")
    # 创建一个临时 JSON 文件做演示
    import tempfile, os
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({"user": "Alice", "role": "admin"}, f)
        tmp_path = f.name
    loader = LazyLoader(tmp_path)
    print(f"  loader.user = {loader.user}")
    print(f"  loader.role = {loader.role}")
    os.unlink(tmp_path)

    print("\n5. __delattr__ 保护")
    p = Protected()
    del p.name  # OK
    try:
        del p._secret  # 失败
    except AttributeError as e:
        print(f"  删除保护: {e}")
