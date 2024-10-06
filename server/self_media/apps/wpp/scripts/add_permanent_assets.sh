if [ -f .env ]; then
  # 读取 .env 文件并导出变量
  export $(cat .env | grep -v '#' | awk '/=/ {print $1}')
fi

echo "access_token: $access_token"


# 上传图文消息内的图片获取URL
# curl -F media=@logo.png "https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token=${access_token}"


# 新增其他类型永久素材
curl -F media=@logo.png "https://api.weixin.qq.com/cgi-bin/material/add_material?type=image&access_token=${access_token}"


# 新增永久视频素材的调用示例
# curl -F media=@demo.mp4 "https://api.weixin.qq.com/cgi-bin/material/add_material?type=TYPE&access_token=${access_token}" -F description='{"title":"demo", "introduction":"introduction"}'
