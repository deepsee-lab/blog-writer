<script lang="ts" setup>
import { reactive, ref, onMounted } from "vue"
defineOptions({
  // 命名当前组件
  name: "Kbitem"
})

const url =
  'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg'
</script>
<template>
  <el-card style="max-width: 480px" shadow="hover"  >
    <div style="display: flex;">
      <div><el-image style="width: 48px; height: 48px" :src="url" fit="fill" /></div>
      <div style="margin-left: 16px;">
        <div>title</div>
        <div>tag</div>
      </div>
    </div>
    <template #footer>Footer content</template>
  </el-card>
</template>
<style lang="scss" scoped></style>
