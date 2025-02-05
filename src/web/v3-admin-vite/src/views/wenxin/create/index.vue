<script lang="ts" setup>
//import { reactive, ref, watch } from "vue"
//import { createTableDataApi, deleteTableDataApi, updateTableDataApi, getTableDataApi } from "@/api/table"
//import { type CreateOrUpdateTableRequestData, type TableData } from "@/api/table/types/table"
import { type FormInstance, type FormRules, ElMessage, ElMessageBox } from "element-plus"
import { Search, Refresh, CirclePlus, Delete, Download, RefreshRight } from "@element-plus/icons-vue"
import axios from 'axios';
//import { usePagination } from "@/hooks/usePagination"
//import { cloneDeep } from "lodash-es"
import type * as WX_path from "./types/WX"
import {type_list_all,style_list_all,create_WX,Word_number_list_all,Word_style_list_all,WX_content_prompt } from "./index"
import {reactive,ref,onMounted} from "vue";
defineOptions({
  // 命名当前组件
  name: "create"
})
/** 登录表单校验规则 */
const WXFormRules: FormRules = {
  Query_content: [{ required: true, message: "请输入提问", trigger: "blur" }]
}
/** 登录表单元素的引用 */
const wxFormRef = ref<FormInstance | null>(null)
const WXFormData: WX_path.WXData = reactive({
  Type_item: "旅游攻略",
  Title_item: "",
  Content_item: "",
  Style_item:"",
  Word_number:"",
  Word_style:"",
  Result_item:"",
  code:""
})

const Type_Data =ref([])
onMounted(async () =>{
  try {
    type_list_all().then((res) => {
      Type_Data.value = res.data
  })
  }catch (error){
    console.error(
        '错误',error
    )
  }
})
const Style_Data =ref([])
onMounted(async () =>{
  try {
    style_list_all().then((res) => {
      Style_Data.value = res.data
  })
  }catch (error){
    console.error(
        '错误',error
    )
  }
})
const Word_Data =ref([])
onMounted(async () =>{
  try {
    Word_number_list_all().then((res) => {
      Word_Data.value = res.data
  })
  }catch (error){
    console.error(
        '错误',error
    )
  }
})

const Word_style_Data =ref([])
onMounted(async () =>{
  try {
    Word_style_list_all().then((res) => {
      Word_style_Data.value = res.data
  })
  }catch (error){
    console.error(
        '错误',error
    )
  }
})
/** 提交信息 */
const handleWX = () => {

  try {
    create_WX(WXFormData).then((res) => {
    WXFormData.Result_item = res.data.Result_item
    alert("创建成功")

  })
  }catch (error){
    console.error(
        '错误',error
    )
  }

}
/** 提交信息 */
const content_prompt = () => {

  try {
    WX_content_prompt(WXFormData).then((res) => {
    WXFormData.value = res.data
    alert("优化成功")
  })
  }catch (error){
    console.error(
        '错误',error
    )
  }

}
</script>


<template>
  <el-form ref="wxFormRef" :model="WXFormData" :rules="WXFormRules" @keyup.enter="handleWX">
          <el-form-item prop="Type_item">
            <p>文章类型：</p>
            <el-select
            v-model.trim="WXFormData.Type_item"
            placeholder="选择类型"
            tabindex="1"
            size="large">
            <el-option
                v-for="item in Type_Data"
                :key="item.name"
                :label="item.name"
                :value="item.name"></el-option>
          </el-select>
          </el-form-item>
          <el-form-item prop="Title_item">
            <p>文章题目：</p>
            <el-input
              v-model.trim="WXFormData.Title_item"
              placeholder="题目"
              type="text"
              tabindex="4"
              :prefix-icon="RefreshRight"
              size="large"
            />
          </el-form-item>
          <el-form-item prop="Content_item">
            <p>内容设定：</p>
            <el-input
              v-model.trim="WXFormData.Content_item"
              placeholder="内容"
              type="textarea"
              tabindex="4"
              :prefix-icon="RefreshRight"
              size="large"
            />
            <el-button  type="primary" size="large" @click.prevent="content_prompt">优化</el-button>
          </el-form-item>
          <el-form-item prop="Style_item">
            <p>选择风格：</p>
            <el-select
            v-model.trim="WXFormData.Style_item"
            placeholder="选择风格："
            tabindex="1"
            size="large">
            <el-option
                v-for="item in Style_Data"
                :key="item.name"
                :label="item.name"
                :value="item.name"></el-option>
          </el-select>
          </el-form-item>
          <el-form-item prop="Word_number">
            <p>选择字数：</p>
            <el-select
            v-model.trim="WXFormData.Word_number"
            placeholder="选择字数："
            tabindex="1"
            size="large">
            <el-option
                v-for="item in Word_Data"
                :key="item.name"
                :label="item.name"
                :value="item.name"></el-option>
          </el-select>
          </el-form-item>
          <el-form-item prop="word_style">
            <p>语言风格：</p>
            <el-select
            v-model.trim="WXFormData.Word_style"
            placeholder="选择风格："
            tabindex="1"
            size="large">
            <el-option
                v-for="item in Word_style_Data"
                :key="item.name"
                :label="item.name"
                :value="item.name"></el-option>
          </el-select>
          </el-form-item>
          <el-form-item prop="Result_item">
            <p>生成结果：</p>
            <el-input
              v-model.trim="WXFormData.Result_item"
              placeholder="结果"
              type="textarea"
              tabindex="4"
              :prefix-icon="RefreshRight"
              size="large"
            />
          </el-form-item>
          <el-button :loading="loading" type="primary" size="large" @click.prevent="handleWX">提交</el-button>
        </el-form>
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
