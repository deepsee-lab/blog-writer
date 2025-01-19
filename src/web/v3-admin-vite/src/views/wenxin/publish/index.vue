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
import {type_list_all,need_open_data_list_all,create_WX,fans_comment_list_all,MEDIA_ID_data_list_all,publish_WX } from "./index"
import {reactive,ref,onMounted} from "vue";
import { fi } from "element-plus/lib/locale/index.js";
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
  author: "作者",
  Title_item: "",
  digest: "",
  content:"",
  content_source_url:"",
  thumb_media_id:"",
  need_open_comment:"",
  only_fans_can_comment:"",
  code:""
})

const thumb_media_data =ref([])
onMounted(async () =>{
  try {
    type_list_all().then((res) => {
      thumb_media_data.value = res.data
  })
  }catch (error){
    console.error(
        '错误',error
    )
  }
})
const need_open_data =ref([])
onMounted(async () =>{
  try {
    need_open_data_list_all().then((res) => {
      need_open_data.value = res.data
  })
  }catch (error){
    console.error(
        '错误',error
    )
  }
})
const fans_comment_data =ref([])
onMounted(async () =>{
  try {
    fans_comment_list_all().then((res) => {
      fans_comment_data.value = res.data
  })
  }catch (error){
    console.error(
        '错误',error
    )
  }
})
const imagePath =ref()
onMounted(async () =>{
      imagePath.value = WXFormData.thumb_media_id.url
  
})
/** 提交信息 */
const handleWX = () => {
  
  try {
    create_WX(WXFormData).then((res) => {
    if (res.success){
      alert("创建成功")
    }else{
      alert("创建失败")
    }
  })
  }catch (error){
    console.error(
        '错误',error
    )
  }

}
const WXFormData_final: WX_path.Wenxin_Media_ID = reactive({
  MEDIA_ID: "请选择ID",
  code:""
})
const MEDIA_ID_data =ref([])
onMounted(async () =>{
  try {
    MEDIA_ID_data_list_all().then((res) => {
      MEDIA_ID_data.value = res.data
  })
  }catch (error){
    console.error(
        '错误',error
    )
  }
})
/** 发布信息 */
const submitWX = () => {
  
  try {
    publish_WX(WXFormData_final).then((res) => {
    if (res.success){
      alert("发布成功")
    }else{
      alert("发布失败")
    }
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
          <el-form-item prop="author">
            <p>作者：</p>
            <el-input
              v-model.trim="WXFormData.author"
              placeholder="作者"
              type="text"
              tabindex="4"
              :prefix-icon="RefreshRight"
              size="large"
            />
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
          <el-form-item prop="digest">
            <p>摘要</p>
            <el-input
              v-model.trim="WXFormData.digest"
              placeholder="摘要"
              type="textarea"
              tabindex="4"
              :prefix-icon="RefreshRight"
              size="large"
            />
          </el-form-item>
          <el-form-item prop="content">
            <p>内容：</p>
            <el-input
              v-model.trim="WXFormData.content"
              placeholder="内容"
              type="textarea"
              tabindex="4"
              :prefix-icon="RefreshRight"
              size="large"
            />
          </el-form-item>
          <el-form-item prop="content_source_url">
            <p>阅读原文地址：</p>
            <el-input
              v-model.trim="WXFormData.content_source_url"
              placeholder="原文地址url"
              type="text"
              tabindex="4"
              :prefix-icon="RefreshRight"
              size="large"
            />
          </el-form-item>
          <el-form-item prop="thumb_media_id">
            <p>封面</p>
            <el-select 
            v-model.trim="WXFormData.thumb_media_id"
            placeholder="选择：" 
            tabindex="1"
            size="large">
            <el-option
                v-for="item in thumb_media_data"
                :key="item.url"
                :label="item.name"
                :value="item.thumb_media_id"></el-option>
          </el-select>
          </el-form-item>
          <el-form-item prop="need_open_comment">
            <p>开启评论</p>
            <el-select 
            v-model.trim="WXFormData.need_open_comment"
            placeholder="选择：" 
            tabindex="1"
            size="large">
            <el-option
                v-for="item in need_open_data"
                :key="item.name"
                :label="item.name"
                :value="item.name"></el-option>
          </el-select>
          </el-form-item>
          <el-form-item prop="only_fans_can_comment">
            <p>仅粉丝评论</p>
            <el-select 
            v-model.trim="WXFormData.only_fans_can_comment"
            placeholder="选择：" 
            tabindex="1"
            size="large">
            <el-option
                v-for="item in fans_comment_data"
                :key="item.name"
                :label="item.name"
                :value="item.name"></el-option>
          </el-select>
          </el-form-item>
          <el-button :loading="loading" type="primary" size="large" @click.prevent="handleWX">提交草稿</el-button>
        </el-form>
        <el-form ref="wxFormRef" :model="WXFormData_final" :rules="WXFormRules" @keyup.enter="submitWX">
          <el-form-item prop="MEDIA_ID">
            <p>MEDIA_ID</p>
            <el-select 
            v-model.trim="WXFormData_final.MEDIA_ID"
            placeholder="选择：" 
            tabindex="1"
            size="large">
            <el-option
                v-for="item in MEDIA_ID_data"
                :key="item.value"
                :label="item.name"
                :value="item.value"></el-option>
          </el-select>
          </el-form-item>
          <el-button :loading="loading" type="primary" size="large" @click.prevent="submitWX">发布草稿</el-button>
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
