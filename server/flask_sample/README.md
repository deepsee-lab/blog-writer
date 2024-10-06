# flask_demo

## 环境配置

###### Anaconda

官方下载: https://www.anaconda.com/download
官方文档：https://docs.anaconda.com/

```bash
# open terminal
conda create -n WWA python=3.10.14
conda activate WWA
cd server && pip install -r requirements.txt
```

注：conda 使用及相关环境问题，可以多问问GPT-4/Google等

## 启动服务

```bash
# open terminal
# cd server
python api.py
```

## 测试服务

打开浏览器（建议 Chrome、Edge），访问`http://127.0.0.1:5000/demo/heartbeat`

看到页面显示 heartbeat 则调用成功

注：此处 IP 和 Port 以实际配置的为准，注意类似 `Please visit http://IP:Port/demo/heartbeat to verify.` 的日志输出

## 新增Flask蓝图说明（代码合并说明）

请大家在 `apps` 目录下，新建和 `demo` 同级的蓝图文件夹，完整路径为 `apps/my_bp_name`，`my_bp_name` 替换为具体的英文名称

其中`apps/my_bp_name/views.py`和`apps/my_bp_name/__init__.py`必须有（参考 `apps/demo`），其他文件可以灵活

并在 `api.py` 中增加类似如下代码

```text
# add
from apps.my_bp_name import bp as xxx_bp

def create_app():
    # add
    app.register_blueprint(xxx_bp)
```

注：关注自定义导包，建议都从 server 为根目录开始导包

###### 文件介绍

1. `views.py`: 路由函数的定义在此处完成，并确保存在类似如下代码

```python
# -*- coding: utf-8 -*-
from flask import Blueprint

bp = Blueprint("my_bp_name", __name__, url_prefix='/my_bp_name')


@bp.route('/heartbeat')
def heartbeat():
    return 'heartbeat'

```

2. `__init__.py`: 确保存在类似如下代码

```text
# -*- coding: utf-8 -*-
from apps.my_bp_name.views import bp
```

3. `models.py`: 表结构相关的放这里，实现请参考 apps/demo/models.py

4. 类似`hook.py`,`forms.py`,`decorators.py` 等 Flask/Python 常用文件，后续也可以统一格式

## 注意事项

1. 在 PyCharm 等 IDE 里面，可以设置 server 目录为 "Sources Root"
2. 日志在 `logs` 查看
3. 注意 `.gitignore` 的更新和新增管理（已忽略了`logs`和`db.sqlite3`），超过 10M 的文件如非必要不建议上传
