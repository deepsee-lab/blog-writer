# 智能微博写手

## 安装
激活conda虚拟环境 （linux）

cd 到weibo-writer-agent，安装pip install -r requirements.txt

cd 到server下，安装pip install -r requirements.txt

安装ollama，, ollama pull model下载模型 / ollama serve启动

向量数据库，milvus-standalone  (milvusdb/milvus:v2.4.5)  (client = MilvusClient( uri="http://localhost:19530",  token="root:Milvus"))

embedding下的.env配置路径 （configs下的config.py 中默认MODEL_NAME = 'BAAI/bge-large-zh-v1.5'）

## 启动
```bash
# supervisor start
bash start.sh
```
Browse http://127.0.0.1:9001 to manage services. (username: admin, password: admin, config in `supervisor.conf`)

```bash
# supervisor stop
bash stop.sh
```

## 使用
http://127.0.0.1:9020   

登录webui  初始账号密码登录 account：admin  pwd：admin

知识库上传页面上传文件，创建KB，创建Doc
知识库对话，选择框架ollama， 再选择model，接着选择知识库的id，接着可以问答

选择自媒体，即可进行相关操作创作


