import { request } from "@/utils/service"
import type * as WX_path from "./types/WX"

/** 获取封面的list */
export function type_list_all() {
  return request<WX_path.Wenxin_article_Type>({
    url: "Wenxin/thumb_media_data",
    method: "get"
  })
}

/** 获取开启评论的list */
export function need_open_data_list_all() {
  return request<WX_path.Wenxin_article_Type>({
    url: "Wenxin/need_open_data",
    method: "get"
  })
}

/** 获取粉丝评论的list */
export function fans_comment_list_all() {
  return request<WX_path.Wenxin_article_Type>({
    url: "Wenxin/fans_comment",
    method: "get"
  })
}

/** 提交创建WX */
export function create_WX(data:WX_path.WXData) {
  return request<WX_path.WXData>({
    url: "Wenxin/WX_submit_draft",
    method: "post",
    data
  })
}

/** 获取media ID list */
export function MEDIA_ID_data_list_all() {
  return request<WX_path.Wenxin_article_Type>({
    url: "Wenxin/MEDIA_ID_list",
    method: "get"
  })
}

/** 发布创建WX */
export function publish_WX(data:WX_path.Wenxin_Media_ID) {
  return request<WX_path.WXData>({
    url: "Wenxin/WX_publish_draft",
    method: "post",
    data
  })
}