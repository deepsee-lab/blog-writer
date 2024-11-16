<script lang="ts" setup>
import { reactive, ref, onMounted } from "vue"

defineOptions({
  // 命名当前组件
  name: "Kbitem"
})
</script>
<template>
  <el-card style="max-width: 480px">
    <h2>我是一张卡片</h2>
    <template #footer>Footer content</template>
  </el-card>
</template>
<style lang="scss" scoped></style>
