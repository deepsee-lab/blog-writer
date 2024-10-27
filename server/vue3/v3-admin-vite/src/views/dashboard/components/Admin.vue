<script lang="ts" setup>
//import { reactive, ref, watch } from "vue"
//import { createTableDataApi, deleteTableDataApi, updateTableDataApi, getTableDataApi } from "@/api/table"
//import { type CreateOrUpdateTableRequestData, type TableData } from "@/api/table/types/table"
import { type FormInstance, type FormRules, ElMessage, ElMessageBox } from "element-plus"
import { Search, Refresh, CirclePlus, Delete, Download, RefreshRight } from "@element-plus/icons-vue"
import axios from 'axios';
//import { usePagination } from "@/hooks/usePagination"
//import { cloneDeep } from "lodash-es"
import type * as Fight_path from "./types/Fight"
import {Dashboard_chat } from "./index"
import {reactive,ref,onMounted} from "vue";
import { fi } from "element-plus/lib/locale/index.js";
defineOptions({
  // 命名当前组件
  name: "admin"
})
/** 登录表单校验规则 */
const FormRules: FormRules = {
  Query_content: [{ required: true, message: "请输入提问", trigger: "blur" }]
}
/** 登录表单元素的引用 */
const FormRef = ref<FormInstance | null>(null)
const FormData: Fight_path.F_Data = reactive({
  Content_item: "",
  Result:"",
  code:""
})
/** 提交信息 */
const handleDB = () => {
  
  try {
    Dashboard_chat(FormData).then((res) => {
      FormData.value = res.data
    alert(FormData.value.Result)
  })
  }catch (error){
    console.error(
        '错误',error
    )
  }

}
</script>


<template>
  <div class="dashboard-container">
    <el-card shadow="never">
      <el-col :span="18" :xs="24">
          <div class="flex h-full items-center">
            
            <div>
              <h2>智能公众号写手</h2>
            </div>
          </div>
        </el-col>
        <el-col :span="26" :xs="24">
          <div class="flex h-full items-center justify-around">
            <p class="text-sm text-gray">
                智能生成  一键发布，开启轻松愉快的创作旅途
              </p>
          </div>
        </el-col>
    </el-card>
    <!-- 数据卡片 -->
    <el-row :gutter="10" class="mt-5">
      <el-col :xs="24" :sm="12" :lg="6">
        <el-card shadow="never">
          <router-link to="/wenxin/material">上传素材  </router-link>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :lg="6">
        <el-card shadow="never">
          <router-link to="/wenxin/create">新建草稿  </router-link>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :lg="6">
        <el-card shadow="never">
          <router-link to="/wenxin/publish">发布文章  </router-link>
        </el-card>
      </el-col>

    </el-row>

    <el-row :gutter="10" class="mt-5">  
      <el-col :xs="24" :sm="12" :lg="26">
        <el-card shadow="never">
          <el-form ref="wxFormRef" :model="FormData" :rules="FormRules" @keyup.enter="handleDB" >
          <el-form-item prop="Content_item">
            <p>输入内容提示：</p>
            <el-input
              v-model.trim="FormData.Content_item"
              placeholder="请输入"
              type="textarea"
              tabindex="4"
              :prefix-icon="RefreshRight"
              size="large"
            />
            <el-button  type="primary" size="large" @click.prevent="handleDB">生成</el-button>
          </el-form-item>
          
        </el-form>
        </el-card>
      </el-col>
    </el-row>

  </div>
</template>

<style lang="scss" scoped>
.search-wrapper {
  margin-bottom: 20px;
  :deep(.el-card__body) {
    padding-bottom: 2px;
  }
}

.toolbar-wrapper {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.table-wrapper {
  margin-bottom: 20px;
}

.pager-wrapper {
  display: flex;
  justify-content: flex-end;
}
</style>
