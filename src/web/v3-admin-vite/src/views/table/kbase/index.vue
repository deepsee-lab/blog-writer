<script lang="ts" setup>
import { type FormInstance, type FormRules, ElMessage, ElMessageBox } from "element-plus"
import { Search, Refresh, CirclePlus, Delete, Download, RefreshRight } from "@element-plus/icons-vue"
//import { usePagination } from "@/hooks/usePagination"
//import { cloneDeep } from "lodash-es"
import type { Kbitem } from "./types/KB"
import { reactive, ref, onMounted } from "vue"
import { kbList as mockKbList } from "./mockData"
import Kblist from "./components/Kblist.vue"
import NewKB from "./components/NewKB.vue"
defineOptions({
  // 命名当前组件
  name: "kbase"
})

const kbList = ref<Kbitem[]>(mockKbList)
onMounted(() => { })


// methods:
// 监听新增知识库事件
const handleAddKbItem = (newKbItem: Kbitem) => {
  kbList.value.push(newKbItem);
  console.log("父组件接收到新知识库：", newKbItem);
};

const isDialogVisible = ref(false); // 控制 dialog 的状态

const NewKBdialog = () => {
  isDialogVisible.value = true; // 打开 dialog
};
</script>

<template>
  <div class="common-layout">
    <el-container>
      <el-header>
        <div style="font-size: 24px; font-weight: bold">知识库</div>
        <div><el-button type="primary" @click="NewKBdialog">新建知识库</el-button></div>
      </el-header>
      <el-main>
        <Kblist :kbList="kbList" />
        <NewKB v-model:visible="isDialogVisible" @add-kb="handleAddKbItem" />
      </el-main>
    </el-container>
  </div>
</template>

<style lang="scss" scoped>
.common-layout {
  height: 100%;

  .el-container {
    height: 100%;
  }

  .el-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 24px;
  }

  .el-main {
    height: calc(100% - 60px);
    max-height: calc(100% - 60px);
    overflow-y: auto;
  }
}
</style>
