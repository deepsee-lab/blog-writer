<template>
  <el-dialog v-model="dialogVisible" title="新建知识库" width="500">
    <el-form ref="ruleFormRef" :model="FormData" :rules="rules" :size="formSize" label-position="top"
      require-asterisk-position="right">
      <el-form-item label="名称" :label-width="formLabelWidth" prop="KBname">
        <el-input v-model="FormData.KBname" autocomplete="off" placeholder="请输入知识库名称" clearable maxlength="50"
          show-word-limit />
      </el-form-item>
      <el-form-item label="描述" prop="desc">
        <el-input v-model="FormData.desc" type="textarea" maxlength="200" placeholder="请输入知识库描述" show-word-limit
          :autosize="{ minRows: 4, maxRows: 4 }" />
      </el-form-item>
      <el-form-item label="Embedding模型" :label-width="formLabelWidth" prop="Embedding">
        <el-select v-model="FormData.Embedding" placeholder="Please select a zone">
          <el-option label="text-embedding-ada-002" value="Embedding-id1" />
          <el-option label="multilingual-e5-small" value="Embedding-id2" />
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="closeDialog">取消</el-button>
        <el-button type="primary" @click="ConfirmNewKB">
          完成
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import { ref, computed, reactive } from 'vue'
import type { ComponentSize, FormInstance, FormRules } from 'element-plus'
import { nanoid } from "nanoid";
import { kbList } from "../mockData"
defineOptions({
  // 命名当前组件
  name: "NewKB"
})
const props = defineProps({
  visible: {
    type: Boolean,
    required: true,
  },
});
// 定义 emits
const emit = defineEmits(["update:visible", "add-kb"]);

interface RuleForm {
  KBname: string
  Embedding: string
  desc: string
}

const formSize = ref<ComponentSize>('default')
const ruleFormRef = ref<FormInstance>()

const FormData = reactive<RuleForm>({
  KBname: '知识库',
  Embedding: 'Embedding-id1',
  desc: '',
})


const rules = reactive<FormRules<RuleForm>>({
  KBname: [
    { required: true, message: '请填写知识库名称', trigger: 'blur' },
    { min: 1, max: 50, message: '请填写1到50个字符 1 to 50', trigger: 'blur' },
  ],
  Embedding: [
    {
      required: true,
      message: '请选择一个Embedding模型',
      trigger: 'change',
    },
  ],
})


const submitForm = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate((valid, fields) => {
    if (valid) {
      console.log('submit!')
    } else {
      console.log('error submit!', fields)
    }
  })
}


const dialogVisible = computed({
  get: () => props.visible, // 读取父组件传递的值
  set: (value) => emit("update:visible", value), // 通知父组件更新值
});

const dialogFormVisible = ref(false)
const formLabelWidth = '70px'



const closeDialog = () => {
  dialogVisible.value = false; // 关闭 dialog
};

// 添加新知识库逻辑
const ConfirmNewKB = () => {
  const newKbItem = {
    id: nanoid(), // 使用 nanoid 生成唯一 ID
    name: FormData.KBname,
    description: FormData.desc,
    Embedding: FormData.Embedding,
    tags: "",
  };

  console.log("新增知识库：", newKbItem);

  // 可通过 emit 通知父组件数据已更新
  emit("add-kb", newKbItem);

  // 关闭 dialog
  closeDialog();
};
</script>
