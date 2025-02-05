<script lang="ts" setup>

import { reactive, ref, onMounted } from "vue"
import { useRoute } from "vue-router";
// 手动引入图标
import { Document, Edit, Folder, Loading } from "@element-plus/icons-vue";
import type { Kbitem } from "../types/KB"
import { kbList as mockKbList } from "../mockData"
const route = useRoute();
const id = route.params.id; // 获取路由中的动态参数 :id

const ItemData = ref<null | Kbitem>(null); // 存储知识库详情数据

const kbList = ref<Kbitem[]>(mockKbList)

// 模拟文件数据
interface FileItem {
  id: string;
  name: string;
  size: string; // 文件大小
  paragraphs: number; // 段落数
  characters: number; // 字符数
  updatedAt: string; // 更新时间
  status: boolean; // 是否可用
}

const fileList = reactive<FileItem[]>([
  {
    id: "1",
    name: "文档1.pdf",
    size: "2.3 MB",
    paragraphs: 10,
    characters: 5000,
    updatedAt: "2023-11-16 14:23:00",
    status: true,
  },
  {
    id: "2",
    name: "图纸2.dwg",
    size: "5.7 MB",
    paragraphs: 1,
    characters: 1200,
    updatedAt: "2023-11-15 11:02:45",
    status: false,
  },
  {
    id: "3",
    name: "笔记.txt",
    size: "512 KB",
    paragraphs: 20,
    characters: 8000,
    updatedAt: "2023-11-14 09:30:20",
    status: true,
  },
]);

// 根据 ID 加载知识库详情
const loadData = () => {
  ItemData.value = kbList.value.find((item) => item.id === id) || null;
};

defineOptions({
  // 命名当前组件
  name: "KbDetail"
})
// 切换文件状态
const onStatusChange = (file: FileItem) => {
  console.log(`文件 ${file.name} 的状态已切换为: ${file.status ? "启用" : "禁用"}`);
};



const addfile = () => {
  console.log('添加文档')
}
onMounted(() => {
  loadData();
})

</script>

<template>
  <div class="common-layout">
    <el-container>
      <el-header>
        <div style="font-size: 24px; font-weight: bold">{{ ItemData?.name }}</div>
        <div><el-button type="primary" @click="addfile">添加文档</el-button></div>
      </el-header>
      <el-main>
        <el-table :data="fileList" border stripe style="width: 100%">
          <!-- 文件名列 -->
          <el-table-column label="文件名" min-width="200">
            <template #default="{ row }">
              <div style="display: flex; align-items: center;">
                <el-icon v-if="row.name.endsWith('.pdf')">
                  <Document />
                </el-icon>
                <el-icon v-else-if="row.name.endsWith('.txt')">
                  <Edit />
                </el-icon>
                <el-icon v-else-if="row.name.endsWith('.dwg')">
                  <Folder />
                </el-icon>
                <el-icon v-else>
                  <Loading />
                </el-icon>
                <span style="margin-left: 8px;">{{ row.name }}</span>
              </div>
            </template>
          </el-table-column>

          <!-- 文件大小列 -->
          <el-table-column prop="size" label="文件大小" min-width="100" />

          <!-- 段落数列 -->
          <el-table-column prop="paragraphs" label="段落数" min-width="80" />

          <!-- 字符数列 -->
          <el-table-column prop="characters" label="字符数" min-width="100" />

          <!-- 更新时间列 -->
          <el-table-column prop="updatedAt" label="更新时间" min-width="150" />

          <!-- 状态列 -->
          <el-table-column label="状态" width="120">
            <template #default="{ row }">
              <el-tag :type="row.status ? 'success' : 'danger'">
                {{ row.status ? "可用" : "不可用" }}
              </el-tag>
            </template>
          </el-table-column>

          <!-- 操作列 -->
          <el-table-column label="操作" min-width="150">
            <template #default="{ row }">
              <el-switch v-model="row.status" @change="onStatusChange(row)" />
            </template>
          </el-table-column>
        </el-table>
      </el-main>
    </el-container>
  </div>
</template>

<style lang="scss" scoped>
.common-layout {
  height: 100%;
  background-color: #f7f7fa;

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
