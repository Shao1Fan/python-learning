# 15 | 打包与导入

## 面试常见问题

- `__init__.py` 的作用？
- 相对导入和绝对导入的区别？
- `__all__` 的作用？
- `if __name__ == '__main__'` 的原理？
- 命名空间包 (namespace package) 是什么？
- `.pth` 文件和 `sys.path` 的修改？

## 导入机制

```python
import foo.bar
# 1. 在 sys.modules 中查找
# 2. 在 sys.path 中搜索 finder
# 3. finder 找到 loader
# 4. loader 执行模块代码
# 5. 模块加入 sys.modules
# 6. 当前命名空间绑定变量
```
