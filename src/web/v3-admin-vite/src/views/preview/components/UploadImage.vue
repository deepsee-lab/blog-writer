<template>
  <div class="flex flex-col gap-6">
    <!-- 上传图片区域 -->
    <div class="bg-white p-4 rounded-lg shadow-md" v-loading="uploadLoading" element-loading-text="图片上传中...">
      <h2 class="text-lg font-semibold mb-4">上传图片</h2>
      <div class="flex flex-col gap-4 items-center">
        <el-upload ref="uploadRef" :file-list="fileList" :auto-upload="false" class="upload-demo w-full"
          action="/api/v1/upload/file" list-type="picture-card" :on-change="handleChange" :on-success="handleSuccess"
          :on-error="handleError" :on-remove="handleRemove" :show-file-list="true" :headers="uploadHeaders"
          :data="uploadData" :http-request="customHttpRequest" multiple accept="image/*">
          <i class="el-icon-upload"></i>
          <div class="el-upload__text">点击上传图片</div>
        </el-upload>
      </div>
    </div>

    <!-- 参数设置区域 -->
    <div class="bg-white p-4 rounded-lg shadow-md">
      <h2 class="text-lg font-semibold mb-4">参数设置</h2>
      <ParamsForm @updateFormData="handleFormData" />
    </div>

    <!-- 提交按钮 -->
    <div class="flex justify-center">
      <el-button @click="handleAction" :class="{
        'rainbow-text-button shimmer-effect': fileList.length > 0 && !props.ParentLoading,
        'disabled-button': fileList.length === 0 || props.ParentLoading,
      }" :disabled="(
        (fileList.length === 0 && Object.keys(imageRes).length === 0)
      ) || props.ParentLoading">
        <SvgIcon name="magicTool" />{{ ButtonMap[currentStep] }}
      </el-button>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, defineEmits, watch } from 'vue';
import { getImageDesc, getFrame, getResult, getJsonbymarkdown } from '../index'
import type { IamgeDescRequest } from '../types/KB'
import ParamsForm from './ParamsForm.vue';
import { ElMessage } from 'element-plus';
// 上传成功后的图片 URL
const fileList = ref<any>([])

// data:

const uploadLoading = ref(false)
const IamgeDescParamas = ref<IamgeDescRequest>({
  images: [],
  style: "自然流畅",
  language: "中文",
  length: "200",
  summary_length: "400",
  temperature: 0.3,
  type_name: 'xinference',
  model_select: 'MiniCPM-V-2.6-8B',
})


const handleRemove = (file: File, fileListRef: Array<File>) => {
  fileList.value = [...fileListRef]; // 确保 fileList 与组件内部同步
  console.log('文件被移除，当前文件列表:', fileList.value);
};


const handleChange = (file: File, fileListRef: Array<File>) => {
  fileList.value = [...fileListRef]; // 确保 fileList 及时反映最新的文件列表
  console.log('当前已选择的文件列表:', fileList.value);
};

const emit = defineEmits(['update-loading', 'update-content', 'update-imageRes', 'update-frameRes', 'update-FinalRes']);
const props = defineProps({
  ParentLoading: Boolean,
  content: Object,
  currentStep: Number
});

const uploadUrl = ref<any>(null);


const JourneyTheme = ref('游记主题')
const travel_descriptions = ref('')
const imageRes = ref<any>({})
const frameRes = ref<any>({})
const FinalRes = ref<any>({})
// 接收子组件传递的数据
const handleFormData = (data: any) => {
  JourneyTheme.value = data.theme
  travel_descriptions.value = data.travel_descriptions
  IamgeDescParamas.value.model_select = data.model_select
  IamgeDescParamas.value.temperature = data.temperature
  IamgeDescParamas.value.style = data.style
  IamgeDescParamas.value.length = data.length
  IamgeDescParamas.value.summary_length = data.summary_length
  IamgeDescParamas.value.type_name = data.type_name
};

const ButtonMap = {
  0: '图片解析',
  1: '大纲生成',
  2: '文章生成',
}

const uploadRef = ref()
const customHttpRequest = async (options: any) => {
  console.log('Custom HTTP Request Triggered:', options);
};

const handleAction = async () => {
  if (props.currentStep === 0) {
    if (!fileList.value.length) {
      ElMessage.error('请选择至少一张图片进行上传');
      return;
    }

    // 构建新的 FormData，每次清空旧内容
    const formData = new FormData();
    fileList.value.forEach((file: any) => {
      const rawFile = file.raw || file; // 确保获取文件的原始数据
      console.log('正在上传文件:', rawFile.name);
      formData.append('files', rawFile); // 修改这里，将 'file' 改为 'files'
    });

    console.log('formData type:', formData, typeof formData);

    try {
      // emit('update-loading', true);
      uploadLoading.value = true;
      const response = await fetch('/api/v1/upload/file', {
        method: 'POST',
        headers: uploadHeaders,
        body: formData,
      });
      const result = await response.json();
      if (response.ok) {
        console.log('上传成功:', result);
        handleSuccess(result, fileList.value);
        uploadLoading.value = false;
      } else {
        ElMessage.error(`上传失败：${result.message || '未知错误'}`);
        uploadLoading.value = false;
      }
    } catch (error) {
      console.error('上传失败:', error);
      ElMessage.error('上传失败，请稍后重试');
    } finally {
    }
  } else if (props.currentStep === 1) {
    try {
      emit('update-loading', true);
      await handleFrame()
    } catch (error) {
      console.error('获取大纲失败:', error);
    } finally {
      emit('update-loading', false);
    }
  } else if (props.currentStep === 2) {
    try {
      emit('update-loading', true);
      await handleFinalResult()
    } catch (error) {
      console.error('生成文章失败:', error);
    } finally {
      emit('update-loading', false);
    }
  }
};


// 错误信息

// 上传接口的 headers（可根据需要添加认证 token 等）
const uploadHeaders = {
  Authorization: `Bearer ${localStorage.getItem('token')}`, // 替换为实际获取 token 的方法
};

// 上传时附带的额外数据（如果需要）
const uploadData = {
  additionalData: 'example', // 如果需要额外的参数，可以在这里添加
};


onMounted(async () => {
  // try {
  //   const ImageSavedData = localStorage.getItem('LocalImageData');
  //   const FrameSavedData = localStorage.getItem('LocalFrameData');
  //   const FinalResultSavedData = localStorage.getItem('LocalResultData');
  //   if (ImageSavedData) {
  //     imageRes.value = JSON.parse(ImageSavedData);
  //     console.log('imageRes.value onMounted', imageRes.value);
  //   }
  //   if (FrameSavedData) {
  //     frameRes.value = JSON.parse(FrameSavedData);
  //     console.log('frameRes.value onMounted', frameRes.value);
  //   }
  //   if (FinalResultSavedData) {
  //     FinalRes.value = JSON.parse(FinalResultSavedData);
  //     console.log('FinalRes.valueonMounted ', FinalRes.value);
  //   }
  // } catch (error) {
  //   console.log(error);
  // }
});

// watch(
//   () => props.currentStep,
//   (newcurrentStep, oldcurrentStep) => {
//     console.log("ParentLoading changed:", newcurrentStep);
//     if (IamgeDescParamas.value.images.length > 0 && newcurrentStep === 0 && Object.keys(imageRes).length === 0) {
//     }
//     // 处理 ParentLoading 变化的逻辑
//   },
//   {
//     // immediate: true
//   }
// );
watch(
  () => imageRes.value,
  (newval, oldval) => {
    console.log('Object.keys(imageRes.value).length', Object.keys(imageRes.value).length);
    console.log("imageRes.value changed:", newval);
    if (Object.keys(newval).length === 0) {
      return
    }
    emit('update-imageRes', imageRes.value);
    console.log("emit imageRes.value", imageRes.value);

    // 处理 ParentLoading 变化的逻辑
  },
  {
    immediate: true
  }
);
watch(
  () => frameRes.value,
  (newval, oldval) => {
    console.log("frameRes.value changed:", newval);
    console.log('Object.keys(frameRes.value).length', Object.keys(frameRes.value).length);

    if (Object.keys(newval).length === 0) {
      return
    }
    emit('update-frameRes', frameRes.value);
    console.log("emit frameRes.value", frameRes.value);
    // 处理 ParentLoading 变化的逻辑
  },
  {
    immediate: true
  }
);
watch(
  () => FinalRes.value,
  (newval, oldval) => {
    console.log("FinalRes.value changed:", newval);
    if (Object.keys(newval).length === 0) {
      return
    }
    emit('update-FinalRes', FinalRes.value);
    console.log("emit FinalRes.value", FinalRes.value);
    // 处理 ParentLoading 变化的逻辑
  },
  {
    immediate: true
  }
);


// 上传成功的回调
const handleSuccess = async (response: any, file: File) => {
  if (response && response.data) {
    uploadUrl.value = response.data; // 假设返回的数据中有 data 字段
    IamgeDescParamas.value.images = uploadUrl.value.map((item: any) => item.url);
    ElMessage({
      message: '图片上传成功',
      type: 'success',
    })
    console.log("IamgeDescParamas.value", IamgeDescParamas.value);
    //try {
    console.log("123: any");
    try {
      emit('update-loading', true);
      await handleGetImageConent()
    } catch (error) {
      ElMessage.error('图片解析失败' + error)
    } finally {
      emit('update-loading', false);
    }

    //try {
    //} catch (error) {

    //}

  } else {
    console.error('上传失败111');
    ElMessage.error('上传失败')
  }
};


const handleGetImageConent = async () => {
  try {
    const res: any = await getImageDesc({
      ...IamgeDescParamas.value,
      type_name: "xinference",
      model_select: "MiniCPM-V-2.6-8B"
    })
    console.log("res: any", res);
    imageRes.value = res.data
    frameRes.value = {}
    FinalRes.value = {}
    localStorage.setItem('LocalImageData', JSON.stringify(imageRes.value));
    emit('update-imageRes', imageRes.value);
  } catch (error) {
    console.error('图片解析失败' + error)
  } finally {
  }
}

const handleFrame = async () => {
  const frame: any = await getFrame({
    image_desc: {
      status: true,
      data: imageRes.value.descriptions
    },
    travel_descriptions: travel_descriptions.value,
    theme: JourneyTheme.value,
    temperature: IamgeDescParamas.value.temperature,
    type_name: IamgeDescParamas.value.type_name,
    model_select: IamgeDescParamas.value.model_select,
  })
  frameRes.value = frame.data
  FinalRes.value = {}
  localStorage.setItem('LocalFrameData', JSON.stringify(frameRes.value));
  emit('update-frameRes', frameRes.value);
  console.log("frame", frame);
}

const handleFinalResult = async () => {
  const finalResult: any = await getResult({
    image_descriptions:
    {
      'status': true,
      data: imageRes.value.descriptions
    },
    theme: JourneyTheme.value,
    outline: JSON.stringify(frameRes.value.content),
    //outline: '迪士尼乐园',
    temperature: IamgeDescParamas.value.temperature,
    type_name: IamgeDescParamas.value.type_name,
    model_select: IamgeDescParamas.value.model_select,
    // outline: "### 游记大纲\n\n1. **介绍**\n   - 引言：武汉的魅力\n   - 旅游的意义和期待\n\n2. **正文**\n   - 第一章：城市建筑夜景\n     - 描述武汉的璀璨夜景\n     - 夜晚的城市活力\n     - 推荐观赏夜景的最佳地点\n   - 第二章：光谷德国风情街\n     - 描述光谷的异国风情\n     - 德国风情街的建筑和文化特色\n     - 独特的购物和美食体验\n   - 第三章：俯瞰城市公园\n     - 描述城市公园的自然美景\n     - 放松与休闲的完美去处\n     - 推荐的公园活动\n\n3. **总结**\n   - 武汉的多元魅力\n   - 此行的感悟与收获\n   - 对未来旅途的期待\n\n### 游记正文\n\n#### 介绍\n\n武汉，这座位于中国中部的城市，以其独特的地理位置和丰富的历史文化吸引着无数游客。此次旅行，我怀揣着对这座城市的无限期待，踏上了探索武汉的旅程。在这里，我希望感受到城市的现代魅力和传统韵味。\n\n#### 第一章：城市建筑夜景\n\n夜幕降临，武汉的城市建筑在璀璨灯光的映衬下显得格外迷人。站在长江大桥上，夜风轻拂，眼前的江水与城市灯火交相辉映，形成了一幅美丽的画卷。在武汉，观赏夜景的最佳地点莫过于汉口江滩，这里不仅能欣赏到两岸的灯火辉煌，还能感受到城市夜生活的活力与激情。\n\n#### 第二章：光谷德国风情街\n\n走进光谷的德国风情街，仿佛置身于异国他乡。街道两旁是富有德国特色的建筑，浓厚的文化气息扑面而来。在这里，游客不仅可以欣赏到德国的建筑风格，还能品尝到正宗的德式美食。漫步其间，各种精致的小店和咖啡馆让人目不暇接，仿佛是一次小型的环球旅行。\n\n#### 第三章：俯瞰城市公园\n\n登上高处俯瞰武汉的城市公园，绿意盎然的景色让人心旷神怡。公园内，湖水碧波荡漾，树木葱茏，是城市中难得的宁静之地。在这里，散步、骑行或简单地坐在湖边小憩，都是极好的选择。城市公园不仅提供了一个放松的场所，也为城市居民和游客提供了一个亲近自然的机会。\n\n#### 总结\n\n此次武汉之行，让我深刻感受到这座城市的多元魅力。无论是现代的城市建筑、异国风情的文化街区，还是自然宁静的城市公园，武汉都以其独特的方式吸引着每一位来访的游客。通过这次旅行，我不仅收获了美好的回忆，也对未来的旅程充满期待。武汉，这座充满活力与魅力的城市，值得每一个旅行者去探索和发现。"
  })
  console.log("finalResult 非json", finalResult);

  const JsonResult: any = await getJsonbymarkdown({
    data: {
      title: JourneyTheme.value,
      outline: JSON.stringify(frameRes.value.content) || '',
      content: finalResult.data.content || '',
      images: finalResult.data.images,
      unified_text: finalResult.data.unified_text,
      descriptions: finalResult.data.descriptions,
    },
    img_width: 600,
    temperature: IamgeDescParamas.value.temperature,
    type_name: IamgeDescParamas.value.type_name,
    model_select: IamgeDescParamas.value.model_select,
  })

  FinalRes.value = JsonResult.data
  localStorage.setItem('LocalResultData', JSON.stringify(FinalRes.value));
  emit('update-FinalRes', FinalRes.value);
  console.log("JsonResult", FinalRes);
  emit('update-content', finalResult);
}

// 上传失败的回调
const handleError = (err: Error, file: File) => {
  ElMessage.error('上传失败4' + err)
};


</script>

<style lang="scss" scoped>
.upload-demo i {
  font-size: 28px;
  color: #409EFF;
}

.el-upload__text {
  color: #409EFF;
}

.error {
  color: red;
}

.rainbow-text-button {
  position: relative;
  /* 必须设为 relative */
  padding: 4px 0px;
  font-family: PingFangSC, PingFang SC;
  font-weight: 500;
  font-size: 28px;
  background: linear-gradient(51.08966190210423deg, #FF00FA 0%, #0061FF 47%, #00C8FF 100%);
  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;
  border-radius: 5px;
  border: none;
  overflow: hidden;
  /* 确保动画不会超出边界 */
}

.disabled-button {
  font-size: 28px;
  color: #ccc;
  /* 灰色字体 */
  background: none;
  /* 无背景渐变 */
  border: none;
  /* pointer-events: none; */
  /* 禁止鼠标交互 */
  opacity: 0.6;

  /* 调整透明度 */
  &:hover {
    color: #ccc !important;
    background: unset !important;
    /* 恢复透明度 */
  }
}

.disabled-button svg {
  fill: #ccc;
  /* 灰色 */
  stroke: #ccc;
  /* 灰色 */
}

.rainbow-text-button::after {
  content: '';
  position: absolute;
  top: 0;
  left: -150%;
  /* 初始位置在按钮左侧 */
  width: 100%;
  height: 100%;
  background: linear-gradient(120deg, rgba(255, 255, 255, 0.4) 0%, rgba(255, 255, 255, 0.2) 30%, rgba(255, 255, 255, 0) 70%);
  transform: skewX(-30deg);
  transition: none;
  pointer-events: none;
  /* 确保光效不干扰点击 */
}

.shimmer-effect:active::after,
.shimmer-effect:focus::after,
.shimmer-effect:hover::after {
  animation: shimmer 1s ease-in-out;
  /* 触发动画 */
}

@keyframes shimmer {
  0% {
    left: -150%;
    /* 起点 */
  }

  50% {
    left: 50%;
    /* 光效经过按钮中间 */
  }

  100% {
    left: 150%;
    /* 光效消失在按钮右侧 */
  }
}
</style>
