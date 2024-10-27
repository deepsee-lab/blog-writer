import { request } from "@/utils/service"
import type * as FT_path from "./types/Fight"


/** 问答prompt */
export function Dashboard_chat(data:FT_path.F_Data) {
  return request<FT_path.F_Data>({
    url: "Dashboard/chat",
    method: "post",
    data
  })
}
