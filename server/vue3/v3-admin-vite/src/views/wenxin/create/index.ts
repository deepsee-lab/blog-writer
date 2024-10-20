import { request } from "@/utils/service"
import type * as WX_path from "./types/WX"

/** 获取知识库的list */
export function type_list_all() {
  return request<WX_path.Wenxin_article_Type>({
    url: "Wenxin/acticle_type",
    method: "get"
  })
}

/** 获取知识库的list */
export function style_list_all() {
  return request<WX_path.Wenxin_article_Type>({
    url: "Wenxin/acticle_style",
    method: "get"
  })
}

/** 获取知识库的list */
export function Word_number_list_all() {
  return request<WX_path.Wenxin_article_Type>({
    url: "Wenxin/word_number",
    method: "get"
  })
}

/** 获取知识库的list */
export function Word_style_list_all() {
  return request<WX_path.Wenxin_article_Type>({
    url: "Wenxin/word_style",
    method: "get"
  })
}

/** 提交创建KB */
export function create_WX(data:WX_path.WXData) {
  return request<WX_path.WXData>({
    url: "Wenxin/create_draft",
    method: "post",
    data
  })
}