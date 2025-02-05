<template>
  <div class="max-w-4xl mx-auto">
    <!-- 表单 -->
    <el-form ref="formRef" :model="formData" :rules="rules" label-width="170px" class="w-full" label-position="top">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-x-4 gap-y-0 overflow-auto">
        <!-- 框架选择 -->
        <el-form-item label="框架选择" prop="type_name" required>
          <el-select v-model="formData.type_name" placeholder="请选择框架" @change="handleFrameworkChange">
            <el-option v-for="option in frameworkOptions" :key="option" :label="option" :value="option" />
          </el-select>
        </el-form-item>

        <!-- 模型输入 -->
        <el-form-item label="模型" prop="model_select" required>
          <el-select v-model="formData.model_select" placeholder="请选择模型">
            <el-option v-for="option in ModelOptions" :key="option" :label="option" :value="option" />
          </el-select>
        </el-form-item>

        <!-- 主题 -->
        <el-form-item label="主题" prop="theme" required>
          <el-input v-model="formData.theme" placeholder="请输入主题，如‘武汉游记’" />
        </el-form-item>

        <el-form-item label="摘要" prop="travel_descriptions" required>
          <el-input v-model="formData.travel_descriptions" placeholder="请输入摘要，如‘今日去武汉夜游，很开心’" />
        </el-form-item>

        <!-- 风格输入 -->
        <el-form-item label="风格" prop="style">
          <el-input v-model="formData.style" placeholder="请输入风格，如‘自然流畅’" />
        </el-form-item>

        <!-- Temperature 输入 -->
        <el-form-item label="Temperature" prop="temperature">
          <el-input-number v-model="formData.temperature" :min="0" :max="1" :step="0.1" />
        </el-form-item>

        <!-- 长度输入 -->
        <el-form-item label="长度" prop="length">
          <el-input-number v-model="formData.length" :min="1" placeholder="请输入长度" :step="20" />
        </el-form-item>

        <!-- 摘要长度输入 -->
        <el-form-item label="摘要长度" prop="summary_length">
          <el-input-number v-model="formData.summary_length" :min="1" placeholder="请输入摘要长度" :step="50" />
        </el-form-item>
      </div>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, watch, onMounted } from 'vue';
import { ElMessage } from 'element-plus';

import { getModelsByFramework } from '../index'

const emit = defineEmits<{
  (event: 'updateFormData', data: any): void;
}>();

// 表单数据
const formData = reactive({
  type_name: '',
  theme: '',
  travel_descriptions: '',
  model_select: '',
  temperature: 0.5,
  style: '',
  length: 200,
  summary_length: 400,
});

// 表单校验规则
const rules = {
  type_name: [{ required: true, message: '请选择框架', trigger: 'change' }],
  model_select: [{ required: true, message: '请选择模型', trigger: 'change' }],
  theme: [{ required: true, message: '请输入主题', trigger: 'blur' }],
  travel_descriptions: [{ required: true, message: '请输入摘要', trigger: 'blur' }],
};

const frameworkOptions = reactive(['xinference', 'openai', 'oneapi', 'ollama']);
const ModelOptions = reactive(['MiniCPM-V-2.6-8B']);

const formRef = ref();

// 从 localStorage 加载数据
onMounted(async () => {
  // await handleFrameworkChange(frameworkOptions[0])
  const savedData = localStorage.getItem('formData');
  if (savedData) {
    Object.assign(formData, JSON.parse(savedData));
  }
});

// 监听表单变化并保存到 localStorage
watch(
  formData,
  (newValue) => {
    if (formRef.value) {
      formRef.value.validate((valid: boolean) => {
        if (valid) {
          localStorage.setItem('formData', JSON.stringify(newValue));
          emit('updateFormData', newValue);
          ElMessage({
            message: '配置已保存',
            type: 'success',
          });
        }
      });
    }
  },
  { deep: true }
);

// methods:

const handleFrameworkChange = async (value: string) => {
  console.log('Selected Value:', value);
  try {
    // const res: any = await getModelsByFramework(value)
    const res: any = await getModelsByFramework({ inference_service: value })
    console.log("handleFrameworkChange res", res);
    ModelOptions.splice(0, ModelOptions.length, ...(res?.data?.all_model_list || []));
    formData.model_select = ModelOptions[0]
    if (value === 'openai') {
      ModelOptions.splice(0, ModelOptions.length, 'gpt-4o');
      formData.model_select = ModelOptions[0]
      console.log("ModelOptions", ModelOptions);
    }
  } catch (error) {
    ElMessage.warning('该框架暂无可选模型列表');
    return;
  }
}
</script>

<style scoped>
/* 可根据实际需要添加自定义样式 */
</style>
