import { type RouteRecordRaw, createRouter } from "vue-router"
import { history, flatMultiLevelRoutes } from "./helper"
import routeSettings from "@/config/route"

const Layouts = () => import("@/layouts/index.vue")

/**
 * 常驻路由
 * 除了 redirect/403/404/login 等隐藏页面，其他页面建议设置 Name 属性
 */
export const constantRoutes: RouteRecordRaw[] = [
  {
    path: "/redirect",
    component: Layouts,
    meta: {
      hidden: true
    },
    children: [
      {
        path: ":path(.*)",
        component: () => import("@/views/redirect/index.vue")
      }
    ]
  },
  {
    path: "/403",
    component: () => import("@/views/error-page/403.vue"),
    meta: {
      hidden: true
    }
  },
  {
    path: "/404",
    component: () => import("@/views/error-page/404.vue"),
    meta: {
      hidden: true
    },
    alias: "/:pathMatch(.*)*"
  },
  {
    path: "/login",
    component: () => import("@/views/login/index.vue"),
    meta: {
      hidden: true
    }
  },
  {
    path: "/",
    component: Layouts,
    redirect: "/dashboard",
    children: [
      {
        path: "dashboard",
        component: () => import("@/views/dashboard/index.vue"),
        name: "Dashboard",
        meta: {
          title: "首页",
          svgIcon: "dashboard",
          affix: true
        }
      }
    ]
  },
  {
    path: "/link",
    meta: {
      title: "智能微博",
      svgIcon: "link"
    },
    children: [
      {
        path: "https://www.weibo.com/",
        component: () => {},
        name: "Link1",
        meta: {
          title: "新浪微博"
        }
      },
      {
        path: "https://www.zhihu.com/",
        component: () => {},
        name: "Link2",
        meta: {
          title: "知乎"
        }
      },
      {
        path: "https://www.xiaohongshu.com/",
        component: () => {},
        name: "Link2",
        meta: {
          title: "小红书"
        }
      }
    ]
  },
  {
    path: "/table",
    component: Layouts,
    redirect: "/table/element-plus",
    name: "Table",
    meta: {
      title: "知识库",
      elIcon: "Grid"
    },
    children: [
      {
        path: "element-plus",
        component: () => import("@/views/table/element-plus/index.vue"),
        name: "知识库对话",
        meta: {
          title: "知识库对话",
          keepAlive: true
        }
      },
      {
        path: "vxe-table",
        component: () => import("@/views/table/vxe-table/index.vue"),
        name: "知识库上传",
        meta: {
          title: "知识库上传",
          keepAlive: true
        }
      },
      {
        path: "setting",
        component: () => import("@/views/table/setting/index.vue"),
        name: "大模型设置",
        meta: {
          title: "大模型设置",
          keepAlive: true
        }
      },
      {
        path: "kb",
        component: () => import("@/views/table/kbase/index.vue"),
        name: "知识库",
        meta: {
          title: "知识库",
          keepAlive: true
        }
      }
    ]
  }
]

/**
 * 动态路由
 * 用来放置有权限 (Roles 属性) 的路由
 * 必须带有 Name 属性
 */
export const dynamicRoutes: RouteRecordRaw[] = [
  {
    path: "/wenxin",
    component: Layouts,
    redirect: "/wenxin/material",
    name: "wenxin",
    meta: {
      title: "微信公众号",
      svgIcon: "lock",
      roles: ["admin", "editor"], // 可以在根路由中设置角色
      alwaysShow: true // 将始终显示根菜单
    },
    children: [
      {
        path: "material",
        component: () => import("@/views/wenxin/material/index.vue"),
        name: "上传素材",
        meta: {
          title: "上传素材",
          roles: ["admin"] // 或者在子导航中设置角色
        }
      },
      {
        path: "create",
        component: () => import("@/views/wenxin/create/index.vue"),
        name: "新建草稿",
        meta: {
          title: "新建草稿",
          roles: ["admin"] // 或者在子导航中设置角色
        }
      },
      {
        path: "publish",
        component: () => import("@/views/wenxin/publish/index.vue"),
        name: "发布文章",
        meta: {
          title: "发布文章",
          roles: ["admin"] // 或者在子导航中设置角色
        }
      }
    ]
  }
]

const router = createRouter({
  history,
  routes: routeSettings.thirdLevelRouteCache ? flatMultiLevelRoutes(constantRoutes) : constantRoutes
})

/** 重置路由 */
export function resetRouter() {
  // 注意：所有动态路由路由必须带有 Name 属性，否则可能会不能完全重置干净
  try {
    router.getRoutes().forEach((route) => {
      const { name, meta } = route
      if (name && meta.roles?.length) {
        router.hasRoute(name) && router.removeRoute(name)
      }
    })
  } catch {
    // 强制刷新浏览器也行，只是交互体验不是很好
    window.location.reload()
  }
}

export default router
