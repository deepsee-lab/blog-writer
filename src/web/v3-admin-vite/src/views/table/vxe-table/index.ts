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

/** 选择文件 */
export function kb_file_list_all() {
  return request<KB_path.file_list_RequestData>({
    url: "Embedding/doc_list",
    method: "get"
  })
}

/** 选择文件base */
export function file_doc_base_list_all() {
  return request<KB_path.file_base_list_RequestData>({
    url: "Embedding/doc_base",
    method: "get"
  })
}

/** 提交创建KB doc */
export function create_KB_doc(data:KB_path.New_KB_doc) {
  return request<KB_path.New_KB_doc>({
    url: "Embedding/create_doc",
    method: "post",
    data
  })
}
