<script lang="ts" setup>
import { reactive, ref, onMounted } from "vue"
import type { Kbitem as KbitemType } from "../types/KB"
import Kbitem from "./Kbitem.vue"
defineOptions({
  // 命名当前组件
  name: "Kblist"
})


const props = defineProps<{
  kbList: KbitemType[];
}>();

// 用于存储知识库数据
</script>
<template>
  <div>
    <el-row :gutter="40">
      <el-col :span="6" class="kblist-item" v-for="item in kbList" :key="item.id" :xs="24" :sm="12" :md="8" :lg="6">
        <Kbitem :ItemData="item" />
      </el-col>
    </el-row>
  </div>
</template>
<style lang="scss" scoped>
.kblist-item {
  margin-bottom: 20px;
}
</style>
