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
    <el-row>
      <el-col :span="4"><Kbitem /></el-col>
    </el-row>
  </div>
</template>
<style lang="scss" scoped></style>
