import router from "@/router"
import { useUserStoreHook } from "@/store/modules/user"
import { usePermissionStoreHook } from "@/store/modules/permission"
import { ElMessage } from "element-plus"
import { setRouteChange } from "@/hooks/useRouteListener"
import { useTitle } from "@/hooks/useTitle"
import { getToken } from "@/utils/cache/cookies"
import routeSettings from "@/config/route"
import isWhiteList from "@/config/white-list"
import NProgress from "nprogress"
import "nprogress/nprogress.css"

const { setTitle } = useTitle()
NProgress.configure({ showSpinner: false })

router.beforeEach(async (to, _from, next) => {
  NProgress.start()
  const userStore = useUserStoreHook()
  const permissionStore = usePermissionStoreHook()
  const token = getToken()
  permissionStore.setAllRoutes()
  return next()

  // 先注释掉下方的权限验证，这一块逻辑比较复杂，先注释掉方便开发

  // // debugger
  // // 如果没有登陆
  // if (!token) {
  //   // 如果在免登录的白名单中，则直接进入
  //   if (isWhiteList(to)) return next()
  //   // 其他没有访问权限的页面将被重定向到登录页面
  //   console.log("跳转到login了吗")

  //   return next("/login")
  // }

  // // 如果已经登录，并准备进入 Login 页面，则重定向到主页
  // if (to.path === "/login") {
  //   return next({ path: "/" })
  // }

  // // 如果用户已经获得其权限角色
  // if (userStore.roles.length !== 0) return next()

  // // 否则要重新获取权限角色
  // try {
  //   await userStore.getInfo()
  //   // 注意：角色必须是一个数组！ 例如: ["admin"] 或 ["developer", "editor"]
  //   // 例如: const roles = ["admin"]
  //   console.log("userStore.roles:", userStore.roles, "token:", token)

  //   const roles = userStore.roles
  //   // 生成可访问的 Routes
  //   routeSettings.dynamic ? permissionStore.setRoutes(roles) : permissionStore.setAllRoutes()
  //   // 将 "有访问权限的动态路由" 添加到 Router 中
  //   permissionStore.addRoutes.forEach((route) => router.addRoute(route))
  //   // 确保添加路由已完成
  //   // 设置 replace: true, 因此导航将不会留下历史记录
  //   next({ ...to, replace: true })
  // } catch (err: any) {
  //   // 过程中发生任何错误，都直接重置 Token，并重定向到登录页面
  //   userStore.resetToken()
  //   ElMessage.error(err.message || "路由守卫过程发生错误")
  //   next("/login")
  // }
})

router.afterEach((to) => {
  setRouteChange(to)
  setTitle(to.meta.title)
  NProgress.done()
})
