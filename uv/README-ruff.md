# ruff介绍
Ruff 是一个用 Rust 编写的、速度极快的 Python Linter 和 Formatter。

它的核心使命是用一个工具**替代**过去 Python 开发中需要安装和配置的**一大堆**零散的工具。它将代码检查（Linting）、代码格式化（Formatting）、导入排序、语法升级等功能全部整合到了一个快如闪电的二进制文件中。

# 安装ruff
使用pip安装ruff，pip会自动配置环境变量

pip install ruff

vs code 也可以安装 ruff 插件

# ruff命令
格式化我的代码	        ruff format .
检查代码问题并自动修复	 ruff check . --fix
在 CI/CD 中验证格式	    ruff format . --check
在 CI/CD 中检查代码质量	ruff check .
开发时实时检查	        ruff check . --watch
搞不清某条规则是什么意思 ruff rule <RULE_CODE>
清理缓存	            ruff cache clean
终极清理	            ruff format . && ruff check . --fix



