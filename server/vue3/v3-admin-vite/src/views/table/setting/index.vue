<script lang="ts" setup>
//import { reactive, ref, watch } from "vue"
//import { createTableDataApi, deleteTableDataApi, updateTableDataApi, getTableDataApi } from "@/api/table"
//import { type CreateOrUpdateTableRequestData, type TableData } from "@/api/table/types/table"
import { type FormInstance, type FormRules, ElMessage, ElMessageBox } from "element-plus"
import { Search, Refresh, CirclePlus, Delete, Download, RefreshRight } from "@element-plus/icons-vue"
//import { usePagination } from "@/hooks/usePagination"
//import { cloneDeep } from "lodash-es"
import type * as KB_path from "./types/KB"
import { type_list_all,model_list_all,submit_list_all} from "./index"
import {reactive,ref,onMounted} from "vue";
import { fi } from "element-plus/lib/locale/index.js";
defineOptions({
  // 命名当前组件
  name: "setting"
})
/** 登录表单校验规则 */
const KBFormRules: FormRules = {
  Query_content: [{ required: true, message: "请输入提问", trigger: "blur" }]
}
const kbFormRef = ref<FormInstance | null>(null)
/** 知识库对话数据 */
const kbFormData: KB_path.KBRequestData = reactive({
  Type_item: "ollama",
  Model_item: "qwen2:1.5b-instruct-fp16",
  Top_K:"5",
  Temprature:"50",
  max_time:"5000",
  code:""
})

 

/** 提交信息 */
const handle_setting = () => {
  kbFormRef.value?.validate((valid: boolean, fields) => {
    if (valid) {
      console.log('heelo')
      try {
        submit_list_all(kbFormData).then((res) => {
          console.log(res.data)
      })
      }catch (error){
        console.error(
            '错误',error
        )
      }
    } else {
      console.error("表单校验不通过", fields)
    }
  })
} 
const Type_Data =ref([])
onMounted(async () =>{
  try {
    type_list_all().then((res) => {
      Type_Data.value = res.type_list
  })
  }catch (error){
    console.error(
        '错误',error
    )
  }
})
const Model_Data =ref([])
onMounted(async () =>{
  try {
    model_list_all(kbFormData).then((res) => {
      console.log(res.data)
      Model_Data.value = res.data
  })
  }catch (error){
    console.error(
        '错误',error
    )
  }
})

 
</script>

<template>
    <div class="content">
        <el-form ref="kbFormRef" :model="kbFormData" :rules="KBFormRules" @keyup.enter="handle_setting">
          <el-form-item prop="Type_item">
            <el-select 
            v-model.trim="kbFormData.Type_item"
            placeholder="选择框架" 
            tabindex="1"
            size="large">
            <el-option
                v-for="item in Type_Data"
                :key="item.type"
                :label="item.type"
                :value="item.type"></el-option>
          </el-select>
          </el-form-item>
          <el-form-item prop="Model_item">
            <el-select 
            v-model.trim="kbFormData.Model_item"
            placeholder="选择模型" 
            tabindex="2"
            size="large">
            <el-option
                v-for="item in Model_Data"
                :key="item.name"
                :label="item.name"
                :value="item.name"></el-option>
          </el-select>
          </el-form-item>
          <el-form-item prop="Top_K">
            <p>Top_K</p>
            <el-input
              v-model.trim="kbFormData.Top_K"
              placeholder="Top_K"
              type="text"
              tabindex="4"
              :prefix-icon="RefreshRight"
              size="large"
            />
          </el-form-item>
          <el-form-item prop="Temprature">
            <p>Temprature</p>
            <el-input
              v-model.trim="kbFormData.Temprature"
              placeholder="temprature: 1~100"
              type="text"
              tabindex="5"
              :prefix-icon="RefreshRight"
              size="large"
            />
          </el-form-item>
          <el-form-item prop="max_time">
            <p>max_time</p>
            <el-input
              v-model.trim="kbFormData.max_time"
              placeholder="max_time: 5000"
              type="text"
              tabindex="5"
              :prefix-icon="RefreshRight"
              size="large"
            />
          </el-form-item>
          <el-button :loading="loading" type="primary" size="large" @click.prevent="handle_setting">提交</el-button>
        </el-form>
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
