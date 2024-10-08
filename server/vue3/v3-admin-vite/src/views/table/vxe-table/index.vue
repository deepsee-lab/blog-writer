<script lang="ts" setup>
import { reactive, ref ,onMounted} from "vue"
import axios from 'axios';
import type * as KB_path from "./types/KB"
import { vector_list_all,embedding_list_all ,create_KB} from "./index"
defineOptions({
  // 命名当前组件
  name: "VxeTable"
})

/** 知识库新建 */
const kb_Data: KB_path.New_KB = reactive({
  KB_name: "请输入知识库名字",
  desc: "请输入知识库描述",
  vector_name: "",
  embedding_model_name:"",
  code:""
})

const Vector_Data =ref([])
onMounted(async () =>{
  try {
    vector_list_all().then((res) => {
      Vector_Data.value = res.data
  })
  }catch (error){
    console.error(
        '错误',error
    )
  }
})

const Embedding_Data =ref([])
onMounted(async () =>{
  try {
    embedding_list_all().then((res) => {
      Embedding_Data.value = res.data
  })
  }catch (error){
    console.error(
        '错误',error
    )
  }
})

/** 提交信息 */
const create_new_KB = () => {
  
      try {
        create_KB(kb_Data).then(() => {
        alert("创建成功")
      })
      }catch (error){
        console.error(
            '错误',error
        )
      }
  
}


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
        const response = await axios.post('http://127.0.0.1:9020/weibo_UI/api/v1/KB/upload', formData, {
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

</script>

<template>
  <div class="app-container">
    <p>新建KB</p>
    <el-form-item prop="KB_name">
            <el-input
              v-model.trim="kb_Data.KB_name"
              placeholder="请输入知识库描述"
              type="text"
              tabindex="6"
              size="large"
            />
    </el-form-item>
    <el-form-item prop="desc">
            <el-input
              v-model.trim="kb_Data.desc"
              placeholder="请输入知识库名字"
              type="textarea"
              tabindex="6"
              size="large"
              :rows="2"
            />
    </el-form-item>
    <el-form-item prop="vector_name">
            <el-select 
            v-model.trim="kb_Data.vector_name"
            placeholder="vector name" 
            tabindex="3"
            size="large">
            <el-option
                v-for="item in Vector_Data"
                :key="item.name"
                :label="item.name"
                :value="item.name"></el-option>
          </el-select>
          </el-form-item>
    <el-form-item prop="embedding_model_name">
            <el-select 
            v-model.trim="kb_Data.embedding_model_name"
            placeholder="embedding name" 
            tabindex="3"
            size="large">
            <el-option
                v-for="item in Embedding_Data"
                :key="item.name"
                :label="item.name"
                :value="item.name"></el-option>
          </el-select>
          </el-form-item>
      <el-button :loading="loading" type="primary" size="large" @click.prevent="create_new_KB">提交</el-button>
      <p>   </p>
      <p>---- 分割线 ---</p>
      <p>   </p>
    <form @submit.prevent="uploadFile">
      <input type="file" ref="fileInput" />
      <button type="submit">上传文件</button>
    </form>
  </div>
</template>
