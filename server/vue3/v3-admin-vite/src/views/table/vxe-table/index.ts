import { request } from "@/utils/service"
import type * as KB_path from "./types/KB"


/** 获取vector的list */
export function vector_list_all() {
  return request<KB_path.vector_list_RequestData>({
    url: "Vector/list",
    method: "get"
  })
}

/** 获取embedding的list */
export function embedding_list_all() {
  return request<KB_path.embedding_list_RequestData>({
    url: "Embedding/list",
    method: "get"
  })
}

/** 提交创建KB */
export function create_KB(data:KB_path.New_KB) {
  return request<KB_path.New_KB>({
    url: "Embedding/create",
    method: "post",
    data
  })
}