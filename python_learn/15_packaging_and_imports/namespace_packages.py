"""
Python 导入系统深入
运行: python python_learn/15_packaging_and_imports/namespace_packages.py
"""

import sys
import importlib
import importlib.util
from pathlib import Path
import tempfile
import os
import shutil


# ============================================================
# 1. sys.path 与模块搜索
# ============================================================

def demo_sys_path():
    print("--- sys.path ---")
    print(f"  Python 搜索路径:")
    for i, p in enumerate(sys.path, 1):
        print(f"    {i}. {p}")


# ============================================================
# 2. __all__ 的作用
# ============================================================

def demo_all():
    print("\n--- __all__ ---")
    # from module import * 只导入 __all__ 中列出的名称
    all_module_code = """
__all__ = ["public_func", "PublicClass"]

def public_func():
    return "这是公开函数"

def _private_func():
    return "这是私有函数"

class PublicClass:
    pass

class _PrivateClass:
    pass
    """
    print(f"  __all__ 控制 from module import * 的行为")
    print(f"  public_func ✅  被导出")
    print(f"  _private_func ❌ 不被导出（_开头）")


# ============================================================
# 3. importlib 动态导入
# ============================================================

def demo_importlib():
    print("\n--- importlib 动态导入 ---")

    # 方式1: import_module
    math_module = importlib.import_module("math")
    print(f"  import_module('math'): {math_module.sqrt(16)}")

    # 方式2: spec_from_loader
    spec = importlib.util.spec_from_loader("math", None)
    print(f"  模块 spec: {spec}")

    # 方式3: 从文件路径加载
    temp_dir = tempfile.mkdtemp()
    module_path = Path(temp_dir) / "dynamic_module.py"
    module_path.write_text("""
def hello():
    return "我是动态加载的模块！"
value = 42
""")

    spec = importlib.util.spec_from_file_location("dynamic", module_path)
    dynamic = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dynamic)

    print(f"  动态加载模块: {dynamic.hello()}")
    print(f"  模块内变量: {dynamic.value}")
    shutil.rmtree(temp_dir, ignore_errors=True)


# ============================================================
# 4. 重新加载模块
# ============================================================

def demo_reload():
    print("\n--- 重新加载模块 ---")

    temp_dir = tempfile.mkdtemp()
    module_path = Path(temp_dir) / "reloadable.py"
    module_path.write_text("value = 1")

    sys.path.insert(0, temp_dir)
    import reloadable
    print(f"  初始 value = {reloadable.value}")

    module_path.write_text("value = 2")
    import importlib
    importlib.reload(reloadable)
    print(f"  重载后 value = {reloadable.value}")

    sys.path.remove(temp_dir)
    shutil.rmtree(temp_dir, ignore_errors=True)
    del sys.modules["reloadable"]


# ============================================================
# 5. __init__.py 的作用
# ============================================================

def demo_init_py():
    print("\n--- __init__.py 的作用 ---")
    print(f"  1. 标记目录为 Python 包")
    print(f"  2. 可以在 __init__.py 中控制 from package import *")
    print(f"  3. 可以在 __init__.py 中执行包初始化代码")
    print(f"  4. Python 3.3+ 可以不写 __init__.py (命名空间包)")


# ============================================================
# 6. sys.modules 缓存
# ============================================================

def demo_sys_modules():
    print("\n--- sys.modules ---")
    print(f"  当前已加载模块数: {len(sys.modules)}")
    print(f"  'math' 是否已加载: {'math' in sys.modules}")

    # 模拟第一次导入
    if "collections" not in sys.modules:
        import collections
        print(f"  首次导入 collections")

    print(f"  第二次访问 (从缓存): {sys.modules['collections'].__name__}")


# ============================================================
# 7. _ 前缀 — 私有 vs 公开
# ============================================================

def demo_private():
    print("\n--- 命名约定 ---")
    print(f"  _name     — 内部使用 (from module import * 不导入)")
    print(f"  __name    — 名称修饰 (Name Mangling)")
    print(f"  __name__  — 魔术方法/属性")

    class Demo:
        def __init__(self):
            self.public = "公开"
            self._protected = "保护"
            self.__private = "私有"

        def get_private(self):
            return self.__private

    d = Demo()
    print(f"  d.public: {d.public}")
    print(f"  d._protected: {d._protected}")
    # print(d.__private)  # AttributeError
    print(f"  d._Demo__private: {d._Demo__private}")  # 名称修饰
    print(f"  get_private: {d.get_private()}")


# ============================================================
# 8. if __name__ == '__main__'
# ============================================================

def demo_name_main():
    print("\n--- __name__ == '__main__' ---")
    print(f"  当前模块 __name__: {__name__}")  # 直接运行时是 __main__
    print(f"  作用: 让模块既可以作为脚本运行，也可以被导入")


# ============================================================
# 运行演示
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    demo_sys_path()
    demo_all()
    demo_importlib()
    demo_reload()
    demo_init_py()
    demo_sys_modules()
    demo_private()
    demo_name_main()
