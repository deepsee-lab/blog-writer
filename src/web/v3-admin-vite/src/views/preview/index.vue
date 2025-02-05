<template>
  <div class="allWrap flex p-4 items-center flex-col">
    <div
      class="mb-4 text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-green-600 drop-shadow-md animate-fade-in">
      智能生成您的游记文章
    </div>

    <!-- 主体内容区域：左右布局 -->
    <div class="flex-1 min-h-0 flex gap-4 w-full">
      <!-- 左侧 UploadImage 组件 -->
      <UploadImage class="w-2/5" :currentStep="currentStep" :ParentLoading="contentLoading" :content="content"
        @update-imageRes="handleUpdateImageConent" @update-loading="updateLoading" @update-content="updateContent"
        @update-frameRes="handleUpdateFrameConent" @update-FinalRes="handleUpdateFinalConent" />

      <!-- 右侧显示内容 -->
      <div
        class="flex flex-col bg-gray-50 justify-between w-3/5 font-bold p-6 text-center rounded-xl shadow-md h-full overflow-hiddenrelative"
        ref="ref1">
        <!-- 这里是你现有的内容组件 -->
        <StepOne v-if="currentStep === 0 && Object.keys(imageDescContent).length > 0" :ParentLoading="contentLoading"
          :title="title" :introduction="introduction" :content="imageDescContent" class="flex-grow overflow-y-auto" />
        <StepTwo v-else-if="currentStep === 1 && Object.keys(FrameContent).length > 0" :content="FrameContent"
          :ParentLoading="contentLoading" class="flex-grow overflow-y-auto" />
        <StepThree v-else-if="currentStep === 2 && Object.keys(FinalContent).length > 0" :content="FinalContent"
          :ParentLoading="contentLoading" class="flex-grow overflow-y-auto" />
        <div v-else class="flex-grow" v-loading="contentLoading" element-loading-text="生成中...">
          <el-empty description="暂无内容" style="height: 100%;" />
        </div>
        <div class="right-4 w-full max-w-xs flex justify-between items-center self-end mt-6">
          <!-- 上一步按钮 -->
          <el-button @click="prevStep" :disabled="currentStep <= 0 || contentLoading"
            class="custom-button flex items-center justify-center whitespace-nowrap">
            上一步
          </el-button>

          <!-- 进度条 -->
          <el-progress :percentage="((currentStep + 1) / totalSteps) * 100" class="w-full mx-4" :format="formatProgress"
            :stroke-width="16" :color="['#4caf50', '#43a047']" :status="currentStep === totalSteps - 1 ? 'success' : ''"
            :text-inside="true" />

          <!-- 下一步按钮 -->
          <el-button @click="nextStep" :disabled="currentStep >= totalSteps - 1 || contentLoading"
            class="custom-button flex items-center justify-center whitespace-nowrap">
            下一步
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
// import { content } from './mockData'
import UploadImage from './components/UploadImage.vue'
import StepOne from './components/StepOne.vue';
import StepTwo from './components/StepTwo.vue';
import StepThree from './components/StepThree.vue';

import { parseJSON } from '@/utils/tools'
// 模拟后端返回的数据，使用 `as const` 使得键名和数组内容成为字面量类型
// `as const` 确保键名和数组内容变成字面量类型
const ref1 = ref()
const open = ref(true)
// 页面标题和简介
const title = ref('游记');
const introduction = ref('游记简介');

// 当前步骤
const currentStep = ref<number>(0); // 当前步骤
const totalSteps = ref<number>(3); // 总步骤数
type ImageDescType = Record<string, string[]>;
type ContentResponse = Record<string, string[]>;
const content = reactive<ContentResponse>({})
const imageDescContent = reactive<ImageDescType>({})
const FrameContent = ref<any>({})
const FinalContent = ref<any>({})


const contentLoading = ref(false)
const updateLoading = (newLoading: boolean) => {
  contentLoading.value = newLoading;
  console.log("updateLoading", contentLoading.value);
}

const handleUpdateFrameConent = (FrameConent: any) => {
  console.log("FrameConent", FrameConent);
  FrameContent.value = FrameConent
  FrameContent.value.content = parseJSON(FrameContent.value.content)
}

const handleUpdateFinalConent = (FinalConent: any) => {
  console.log("FinalConent", FinalConent);
  FinalContent.value = FinalConent
}

const handleUpdateImageConent = (ImageConent: any) => {
  console.log("ImageConent", ImageConent);
  const TransContent = Object.fromEntries(
    Object.entries(ImageConent.descriptions.descriptions).map(([key, value]) => [key, [value]])
  );
  Object.keys(imageDescContent).forEach(key => {
    delete content[key];
  });
  Object.assign(imageDescContent, TransContent);
  console.log("handleUpdateImageConent", imageDescContent);
}

const transformToMockData = (finalResult: any): Record<string, string[]> => {
  const tempcotnent: Record<string, string[]> = {};  // 显式指定类型

  // 遍历 descriptions，将 path 作为 key，description 转化为数组
  if (finalResult.data.descriptions && Array.isArray(finalResult.data.descriptions)) {
    finalResult.data.descriptions.forEach((item: any) => {
      const { path, is_url, description } = item;
      if (!tempcotnent[path]) {
        tempcotnent[path] = [];
      }
      // 将描述添加到数组
      if (is_url) {
        tempcotnent[path].push(description);
      }
    });
  }

  return tempcotnent;
};

const updateContent = (res: any) => {
  const showContent = transformToMockData(res)
  title.value = res?.data?.title
  // 先清空原内容
  Object.keys(content).forEach(key => {
    delete content[key];
  });
  // 将新内容添加到内容对象中
  Object.assign(content, showContent);
  console.log("updateContent", content);
}
const prevStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--;
  }
};

const nextStep = () => {
  if (currentStep.value < totalSteps.value - 1) {
    currentStep.value++;
  }
};
// 用于格式化显示步骤进度的函数
const formatProgress = (percentage: number) => {
  const step = currentStep.value + 1;
  return `${step}/${totalSteps.value}`;  // 例如 "1/3", "2/3"
};







onMounted(() => {

});
</script>


<style scoped lang="scss">
/* 样式可以根据需求进行调整 */
img {
  max-width: 100%;
  height: auto;
}

.custom-button {
  width: 100px;
  /* 缩小宽度 */
  height: 32px;
  /* 缩小高度 */
  font-size: 12px;
  /* 调整字体大小 */
  padding: 0 10px;
  border-radius: 8px;
  background-color: #4caf50;
  color: white;
  transition: background-color 0.3s ease;
}

.custom-button:hover {
  background-color: #45a049;
}

.custom-button:disabled {
  background-color: #b0bec5;
  cursor: not-allowed;
}
</style>
<style lang="scss">
/* 适用于整个页面 */

.allwrap {
  height: calc(100vh - var(--v3-header-height) - 50px);
}

.el-popper.is-customized {
  padding: 6px 12px;
  background: linear-gradient(90deg, rgb(159, 229, 151), rgb(204, 229, 129));
  /* 自定义渐变背景 */
}

.el-popper.is-customized .el-popper__arrow::before {
  background: linear-gradient(45deg, #b2e68d, #bce689);
  /* 自定义箭头渐变背景 */
  right: 0;
}
</style>
