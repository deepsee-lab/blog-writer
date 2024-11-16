<script lang="ts" setup>
import { reactive, ref, onMounted } from "vue"
import Kbitem from "./Kbitem.vue"
defineOptions({
  // 命名当前组件
  name: "Kblist"
})
</script>
<template>
  <div>
    <el-row :gutter="40">
      <el-col :span="6" class="kblist-item" v-for="o in 55" :key="o"><Kbitem /></el-col>
    </el-row>
  </div>
</template>
<style lang="scss" scoped>
.kblist-item{
  margin-bottom: 20px;
}</style>
