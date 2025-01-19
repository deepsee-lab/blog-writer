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
import {WX_txt_to_pic,WX_update_token } from "./index"
import {reactive,ref,onMounted} from "vue";
import { fi } from "element-plus/lib/locale/index.js";
defineOptions({
  // 命名当前组件
  name: "material"
})

/** 提交文件 */
const fileInput = ref(null);
const uploadFile = async () => {
  if (!fileInput.value.files[0]) {
        alert('请选择一个文件');
        return;
      }
  const formData = new FormData();
  formData.append('file', fileInput.value.files[0]);
  console.log(formData)
  try {
        const response = await axios.post('http://127.0.0.1:9020/weibo_UI/api/v1/Wenxin/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        console.log(response)
        console.log(response.status)
        if (response.status === 200) {
          alert('文件上传成功');
        } else {
          alert('文件上传失败');
        }
      } catch (error) {
        console.error('上传文件出错：', error);
        alert('文件上传失败');
      }
} 

const Wenxin_Pic: WX_path.Wenxin_pic = reactive({
  Name: "描述你所想象的画面 角色 情绪 风格 内容。。。",
  code:""
})

/** 提交信息 */
const txt_to_pic = () => {
  
  try {
    WX_txt_to_pic(Wenxin_Pic).then(() => {
    alert("添加成功")
  })
  }catch (error){
    console.error(
        '错误',error
    )
  }

}
/** 更新token */
const update_token = () => {
  
  try {
    WX_update_token().then(() => {
    alert("更新成功")
  })
  }catch (error){
    console.error(
        '错误',error
    )
  }

}
</script>

<template>
  <p>matrial</p>
  <el-button :loading="loading" type="primary" size="large" @click.prevent="update_token">更新token</el-button>
  <form @submit.prevent="uploadFile">
      <input type="file" ref="fileInput" />
      <button type="submit">上传文件</button>
    </form>
    <el-form-item prop="Text">
            <p>输入描述</p>
            <el-input
              v-model.trim="Wenxin_Pic.Data"
              placeholder=""
              type="text"
              tabindex="4"
              :prefix-icon="RefreshRight"
              size="large"
            />
          </el-form-item>
          <el-button :loading="loading" type="primary" size="large" @click.prevent="txt_to_pic">提交</el-button>
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
