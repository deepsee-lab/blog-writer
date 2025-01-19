<script lang="ts" setup>
import { reactive, ref ,onMounted} from "vue"
import axios from 'axios';
import type * as KB_path from "./types/KB"
import {kb_list_all} from "../element-plus/index"
import { vector_list_all,embedding_list_all ,create_KB,kb_file_list_all,file_doc_base_list_all,create_KB_doc} from "./index"
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

/** 知识库文件新建 */
const kb_Data_file: KB_path.New_KB_doc = reactive({
  kb_id: "请选择知识库",
  doc_id: "",
  doc_name: "",
  doc_path:"",
  doc_content:"",
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

const KB_file_Data =ref([])
onMounted(async () =>{
  try {
    kb_file_list_all().then((res) => {
      KB_file_Data.value = res.data
  })
  }catch (error){
    console.error(
        '错误',error
    )
  }
})
const doc_base_Data =ref([])
onMounted(async () =>{
  try {
    file_doc_base_list_all().then((res) => {
      doc_base_Data.value = res.data
  })
  }catch (error){
    console.error(
        '错误',error
    )
  }
})

/** 提交信息 */
const create_new_KB_doc = () => {
  
  try {
    create_KB_doc(kb_Data_file).then(() => {
    alert("添加成功")
  })
  }catch (error){
    console.error(
        '错误',error
    )
  }

}


</script>

<template>
  <div class="app-container">
    <p>新建KB</p>
    <el-form-item prop="KB_name">
            <el-input
              v-model.trim="kb_Data.KB_name"
              placeholder="请输入知识库名字"
              type="text"
              tabindex="6"
              size="large"
            />
    </el-form-item>
    <el-form-item prop="desc">
            <el-input
              v-model.trim="kb_Data.desc"
              placeholder="请输入知识库描述"
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
      <p>上传文件</p>
    <form @submit.prevent="uploadFile">
      <input type="file" ref="fileInput" />
      <button type="submit">上传文件</button>
    </form>
    <p>   </p>
      <p>---- 分割线 ---</p>
      <p>   </p>
      <p>给知识库添加文件</p>
      <el-form-item prop="kb_id">
            <el-select 
            v-model.trim="kb_Data_file.kb_id"
            placeholder="选择知识库" 
            tabindex="1"
            size="large">
            <el-option
                v-for="item in KB_Data"
                :key="item.kb_id"
                :label="item.kb_name"
                :value="item.kb_id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item prop="doc_id">
            <el-input
              v-model.trim="kb_Data_file.doc_id"
              placeholder="请输入文件ID"
              type="text"
              tabindex="6"
              size="large"
            />
    </el-form-item>
    <el-form-item prop="doc_name">
            <el-input
              v-model.trim="kb_Data_file.doc_name"
              placeholder="请定义文件名称"
              type="text"
              tabindex="6"
              size="large"
            />
    </el-form-item>
    <el-form-item prop="doc_path">
            <el-select 
            v-model.trim="kb_Data_file.doc_path"
            placeholder="选择文件" 
            tabindex="1"
            size="large">
            <el-option
                v-for="item in KB_file_Data"
                :key="item.name"
                :label="item.name"
                :value="item.name"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item prop="doc_content">
            <el-select 
            v-model.trim="kb_Data_file.doc_content"
            placeholder="选择doc base" 
            tabindex="1"
            size="large">
            <el-option
                v-for="item in doc_base_Data"
                :key="item.name"
                :label="item.name"
                :value="item.name"></el-option>
          </el-select>
        </el-form-item>
        <el-button :loading="loading" type="primary" size="large" @click.prevent="create_new_KB_doc">提交</el-button>
  </div>
</template>
