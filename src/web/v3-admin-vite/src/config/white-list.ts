import { type RouteLocationNormalized } from "vue-router"

/** 免登录白名单（匹配路由 path） */
// 先把我的知识库页面加到白名单里面方便开发"/table/kb"
const whiteListByPath: string[] = ["/login", "/table/kb"]

/** 免登录白名单（匹配路由 name） */
const whiteListByName: string[] = []

/** 判断是否在白名单 */
const isWhiteList = (to: RouteLocationNormalized) => {
  // path 和 name 任意一个匹配上即可
  return whiteListByPath.indexOf(to.path) !== -1 || whiteListByName.indexOf(to.name as any) !== -1
}

export default isWhiteList
