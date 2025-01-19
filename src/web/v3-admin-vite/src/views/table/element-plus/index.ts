import { request } from "@/utils/service"
import type * as KB_path from "./types/KB"

/** 获取知识库的list */
export function kb_list_all() {
  return request<KB_path.KB_list_RequestData>({
    url: "KB/list",
    method: "get"
  })
}

/** 获取result */
export function result_list_all(data:KB_path.KBRequestData) {
  return request<KB_path.KBRequestData>({
    url: "model/result",
    method: "post",
    data
  })
}

/** 获取框架的list */
export function type_list_all() {
  return request<KB_path.Type_list_RequestData>({
    url: "model/type",
    method: "get"
  })
}

/** 获取model的list */
export function model_list_all(data:KB_path.KBRequestData) {
  return request<KB_path.Model_RequestData>({
    url: "model/list",
    method: "post",
    data
  })
}