<script lang="ts" setup>
import { type FormInstance, type FormRules, ElMessage, ElMessageBox } from "element-plus"
import { Search, Refresh, CirclePlus, Delete, Download, RefreshRight } from "@element-plus/icons-vue"
import { fi } from "element-plus/lib/locale/index.js"
//import { usePagination } from "@/hooks/usePagination"
//import { cloneDeep } from "lodash-es"
import type * as KB_path from "./types/KB"
import { reactive, ref, onMounted } from "vue"

import Kblist from "./components/Kblist.vue"
defineOptions({
  // 命名当前组件
  name: "kbase"
})

const Type_Data = ref([])
onMounted(async () => {})
const Model_Data = ref([])
onMounted(() => {})
</script>

<template>
  <div class="common-layout">
    <el-container>
      <el-header>
        <div style="font-size: 24px; font-weight: bold">知识库</div>
        <div><el-button type="primary">新建知识库</el-button></div>
      </el-header>
      <el-main>
        <Kblist />
      </el-main>
    </el-container>
  </div>
</template>

<style lang="scss" scoped>
.el-container {
  height: 100%;
}
.el-header {
  display: flex;
  justify-content: space-between;
  padding: 24px;
}
.el-main {
  height: calc(100% - 60px);
  max-height: calc(100% - 60px);
  overflow-y: auto;
}
</style>
