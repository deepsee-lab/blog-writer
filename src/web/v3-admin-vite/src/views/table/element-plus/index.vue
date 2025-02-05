<script lang="ts" setup>
//import { reactive, ref, watch } from "vue"
//import { createTableDataApi, deleteTableDataApi, updateTableDataApi, getTableDataApi } from "@/api/table"
//import { type CreateOrUpdateTableRequestData, type TableData } from "@/api/table/types/table"
import { type FormInstance, type FormRules, ElMessage, ElMessageBox } from "element-plus"
import { Search, Refresh, CirclePlus, Delete, Download, RefreshRight } from "@element-plus/icons-vue"
//import { usePagination } from "@/hooks/usePagination"
//import { cloneDeep } from "lodash-es"

import {reactive,ref,onMounted} from "vue";
import { kb_list_all,result_list_all,type_list_all,model_list_all } from "./index"
import type * as KB_path from "./types/KB"
defineOptions({
  // 命名当前组件
  name: "ElementPlus"
})

/** 登录表单校验规则 */
const KBFormRules: FormRules = {
  Query_content: [{ required: true, message: "请输入提问", trigger: "blur" }]
}
/** 登录表单元素的引用 */
const kbFormRef = ref<FormInstance | null>(null)
//const { paginationData, handleCurrentChange, handleSizeChange } = usePagination()
/** 知识库对话数据 */
const kbFormData: KB_path.KBRequestData = reactive({
  Type_item: "ollama",
  Model_item: "qwen2:1.5b-instruct-fp16",
  KB_item: "kb_id_kba5a008b69c4d1eb9e75fa915c9de2d",
  Top_K:"5",
  Temprature:"50",
  Query_content:"",
  KB_result:"",
  answer_content:"",
  code:""
})



/** 提交信息 */
const handleKB = () => {
  kbFormRef.value?.validate((valid: boolean, fields) => {
    if (valid) {
      console.log('heelo')
      try {
        result_list_all(kbFormData).then((res) => {
          console.log(res.data)
          kbFormData.KB_result=res.data.KB_result
          kbFormData.answer_content=res.data.answer_content
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
const KB_Data =ref([])
onMounted(async () =>{
  try {
    kb_list_all().then((res) => {
      console.log(res.data)
      KB_Data.value = res.data.kb_list
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
        <el-form ref="kbFormRef" :model="kbFormData" :rules="KBFormRules" @keyup.enter="handleKB">
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
          <el-form-item prop="KB_item">
            <el-select
            v-model.trim="kbFormData.KB_item"
            placeholder="选择知识库"
            tabindex="3"
            size="large">
            <el-option
                v-for="item in KB_Data"
                :key="item.kb_id"
                :label="item.kb_name"
                :value="item.kb_id"></el-option>
          </el-select>
          </el-form-item>
          <el-form-item prop="Top_K">
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
            <el-input
              v-model.trim="kbFormData.Temprature"
              placeholder="temprature: 1~100"
              type="text"
              tabindex="5"
              :prefix-icon="RefreshRight"
              size="large"
            />
          </el-form-item>
          <el-form-item prop="Query_content">
            <el-input
              v-model.trim="kbFormData.Query_content"
              placeholder="Query_content"
              type="text"
              tabindex="6"
              :prefix-icon="RefreshRight"
              size="large"
            />
          </el-form-item>
          <el-form-item prop="KB_result">
            <el-input
              v-model.trim="kbFormData.KB_result"
              placeholder="KB_result"
              type="textarea"
              tabindex="7"
              :prefix-icon="RefreshRight"
              size="large"
              :rows="3"
            />
          </el-form-item>
          <el-form-item prop="answer_content">
            <el-input
              v-model.trim="kbFormData.answer_content"
              placeholder="answer_content"
              type="textarea"
              tabindex="8"
              :prefix-icon="RefreshRight"
              size="large"
              :rows="5"
            />
          </el-form-item>
          <el-button :loading="loading" type="primary" size="large" @click.prevent="handleKB">提交</el-button>
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
