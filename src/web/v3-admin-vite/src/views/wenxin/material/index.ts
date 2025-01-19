import { request } from "@/utils/service"
import type * as WX_path from "./types/WX"



/** 获取result */
export function WX_txt_to_pic(data:WX_path.Wenxin_pic) {
  return request<WX_path.Wenxin_pic>({
    url: "Wenxin/txt_to_pic",
    method: "post",
    data
  })
}

/** 获取result */
export function WX_update_token(data:WX_path.Wenxin_pic) {
  return request<WX_path.Wenxin_pic>({
    url: "Wenxin/update_token",
    method: "post",
    data
  })
}