<script lang="ts" setup>
import { reactive, ref, onMounted } from "vue"
import { useRouter } from 'vue-router';
import { Delete, Document, ElementPlus } from '@element-plus/icons-vue'
import type { Kbitem } from "../types/KB"

defineOptions({
  // 命名当前组件
  name: "Kbitem"
})
const props = defineProps<{
  ItemData: Kbitem;
}>();
const emit = defineEmits(["del-item"]);
const router = useRouter();
const url = ref('https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg')
const handleClick = () => {
  router.push(`/table/kb/${props.ItemData.id}`);// 跳转到动态路由页面
}



</script>
<template>
  <el-card style="max-width: 480px" shadow="hover" @click="handleClick">
    <div style="display: flex;">
      <div><el-image style="width: 48px; height: 48px" :src="url" fit="fill" /></div>
      <div style="margin-left: 16px;">
        <div class="title">{{ ItemData.name }}</div>
        <div v-if="ItemData.tags"><el-tag>{{ ItemData.tags }}</el-tag></div>
        <!-- <div v-else></div> -->
      </div>
    </div>
    <template #footer>
      <div class="footer">
        <div>
          <el-button :icon="Document" link>
            n个文档
          </el-button>
          <el-button :icon="ElementPlus" link>
          </el-button>
        </div>
        <div>
          <el-dropdown>
            <span class="el-dropdown-link">
              <el-icon>
                <More />
              </el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item>
                  <span style="color: red;">删除</span>
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </template>
  </el-card>
</template>
<style lang="scss" scoped>
.el-card {

  &:hover {
    cursor: pointer;
  }
}

.title {
  font-size: 16px;
  font-weight: 500;
}

.el-tag {
  padding: 0px 2px;
  height: 18px;
}

.footer {
  display: flex;
  justify-content: space-between;
  align-items: center;

  .el-button {
    font-size: 12px;
  }
}
</style>
