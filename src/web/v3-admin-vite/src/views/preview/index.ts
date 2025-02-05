import { request } from "@/utils/service"
import type { UploadFileResponse, IamgeDescRequest } from "./types/KB"

/** 提交信息 */
export function uploadFile(data: any) {
  return request<UploadFileResponse>({
    url: "upload/file",
    method: "post",
    data
  })
}

export function getImageDesc(params: IamgeDescRequest) {
  return request({
    url: "get/iamge_desc",
    method: "post",
    data: params
  })
}

export function getFrame(params: any) {
  return request({
    url: "get/frame",
    method: "post",
    data: params
  })
}

export function getResult(params: any) {
  return request({
    url: "get/result",
    method: "post",
    data: params
  })
}

export function getModelsByFramework(params: any) {
  return request({
    url: "get/models",
    method: "post",
    data: params
  })
}

export function getJsonbymarkdown(params: any) {
  return request({
    url: "get/markdown2json",
    method: "post",
    data: params
  })
}
