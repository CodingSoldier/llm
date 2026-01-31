# 安装UV
pip install uv

或者

(Linux环境) curl -LsSf https://astral.sh/uv/install.sh | sh

## 查看版本信息

uv --version

## UV初始化项目
1、创建uv01文件夹

2、cd uv01

3、执行初始化:
    
uv init

uv init命令会创建以下文件：

    .gitignore
    .python-version  # 声明python版本
    main.py
    pyproject.toml   # 声明python项目依赖
    README.md

4、使用uv创建虚拟环境：
    
uv venv 

如果需要指定虚拟环境的版本则执行：

uv venv -p 3.13.5

uv01目录下会新增.venv目录

## uv安装依赖

uv add fastapi

pyproject.toml 的 dependencies 会新增 fastapi>=0.128.0 依赖

再执行 uv add "pydantic<1.7" 测试安装有冲突的版本，uv提示无法安装

### 指定版本
    uv add pydantic==2.10.0 # 使用==
    uv add pydantic>=2.10.0
    uv add "pydantic<=2.10.0"  # <=注意添加引号，避免解析失败

### 卸载依赖

安装numpy

uv add numpy

卸载numpy

### 按树形结构显示依赖
uv tree

### 依赖说明
1. 注意：`uv add` / `uv remove` 只是针对一级依赖

   项目依赖fastapi，而fastapi依赖pydantic。此时，fastapi就是一级依赖，pydantic就是二级依赖。

   `pyproject.toml`中的`dependencies`列出的都是一级依赖

   - 在安装fastapi后，仍然执行`uv add pydantic`。最终`pydantic`会被添加到`pyproject.toml`中。
   - 然后执行`uv remove pydantic`，删除的只是`pyproject.toml`中列出的一级依赖。因为fastapi仍然需要pydantic，所以在环境中，没有删除pydantic



2. 当一个包**既是一级依赖又是二级依赖**时，其最终版本由**依赖解析器**根据以下规则确定：

   1. **一级依赖优先**
      - 如果**一级依赖明确指定了版本**（如 `pydantic>=2.0.0`），解析器会优先满足该版本要求，即使二级依赖的版本与之冲突。
      - 如果冲突无法解决（如二级依赖强制要求 `pydantic<2.0.0`），解析器会报错（`ResolutionImpossible`）。
   2. **冲突时的行为**
      - 如果一级和二级依赖的版本范围**完全不兼容**（如一级要求 `pydantic>=2.0.0`，二级要求 `pydantic<2.0.0`），解析器会失败并提示版本冲突，需要手动解决。


# 打包和同步
## 前置工作
创建好python项目

    uv01
        src
            uv01
                hello.py
                __init__.py
        tests
            test_hello.py

# 打包
1、将打包工具setuptools添加到pyproject.toml

    [build-system]
    requires = ["setuptools>=65.0.0", "wheel"]  
    build-backend = "setuptools.build_meta"

uv是python打包的前端工具。后端工具使用setuptools，也可以使用hatchling

   [build-system]
   requires = ["hatchling"]
   build-backend = "hatchling.build"

2、执行打包命令：uv build

在 src、tests的同级会生成dist目录，打包后的代码放到了dist目录

## 开发

uv没有install命令，只能通过pip使用install命令

开发时使用：uv pip install -e .

使用 `uv pip install pydantic` **不会自动修改 `pyproject.toml`**，它的行为与传统 `pip install` 一致。

建议是只对本项目才使用 uv pip install

使用 uv pip install 的包，无法通过 uv tree 查看到，只能通过 uv pip list 才能看到

执行 uv pip list  如果输出的包列表包含 

    uv01              0.1.0   项目路径

则证明本项目安装成功

### 测试
执行完 uv pip install -e . 后运行 python .\tests\test_hello.py  输出 #### hello #### 证明安装成功

# 环境同步

uv sync

uv sync命令会读取 `pyproject.toml` 中的 `[project.dependencies]`，安装pyproject.toml的所有依赖（包含间接依赖），并移除环境中未列出的包

# 4. pypi源和缓存

1. 使用清华源
    - https://docs.astral.sh/uv/concepts/configuration-files/

    - https://mirrors.tuna.tsinghua.edu.cn/help/pypi/

    Linux系统在 `~/.config/uv/uv.toml` 或者 `/etc/uv/uv.toml` 填写下面的内容：

    ```
    [[index]]
    url = "https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple/"
    default = true
    ```
2. 缓存相关
    - 查看`uv add`导致的缓存位置
      ```
      uv cache dir
      ```

    - 清理缓存
      ```
      uv cache clean
      ```
