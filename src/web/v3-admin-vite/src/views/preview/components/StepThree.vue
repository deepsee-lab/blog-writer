<template>
  <div v-loading="ParentLoading" element-loading-text="生成中...">
    <div class="text-4xl font-bold text-gray-800 mb-6 border-b-2 border-gray-200 pb-2">{{ content.title }}</div>
    <div style="text-indent: 2em;"
      class="bg-gray-100 border-l-2 border-gray-500 text-left text-sm max-w-[900px] mx-auto px-4 py-3 italic text-gray-600 rounded-md mb-6">
      {{
        content.文章.摘要 }}</div>
    <!-- <p class="text-gray-500 text-base leading-relaxed mt-2 font-light">{{ introduction }}</p> -->
    <div class="overflow-y-auto mt-4 pr-4">
      <div v-for="(items, index) in content.文章.正文" :key="index" class="mt-8">
        <img v-if='items.img' :src="items.img" alt="Image"
          class="w-auto max-h-[600px] rounded-lg mb-4 mx-auto shadow-md" />
        <div class="flex flex-col items-center space-y-4">
          <!-- 当前文字显示 -->
          <p style="text-indent: 2em;" class="max-w-[900px] text-base text-left text-gray-600 leading-relaxed">
            {{ items.text }}
          </p>
        </div>

        <div v-if="items.img && index < content.文章.正文.length - 1" class="flex items-center justify-center">
          <div class="h-px w-12 bg-gray-200"></div>
          <span class="mx-2 text-gray-300 text-[10px]">❈</span>
          <div class="h-px w-12 bg-gray-200"></div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, watch } from 'vue';
const props = defineProps({
  ParentLoading: {
    type: Boolean,
    required: true,
  },
  title: {
    type: String,
    required: true,
  },
  introduction: {
    type: String,
    default: 'default introduction',
  },
  content: {
    type: Object as () => Record<string, string[]>,
    required: true,
  },
});
// 手动初始化 `currentTexts`，确保每个键都具有初始值
const currentTexts = reactive<Record<string, string>>({});
// 用来记录每个 imageUrl 是否已经是最后一条
const isLastText = reactive<Record<string, boolean>>({});
// 用来存储通知信息
const notification = ref<string>('');

type ContentKeys = keyof typeof props.content;

// 判断是否禁用下一条按钮
function isNextDisabled(imageUrl: ContentKeys) {
  const texts = props.content[imageUrl] || [];
  const currentIndex = texts.indexOf(currentTexts[imageUrl]);
  return currentIndex === texts.length - 1;
}

// 判断是否禁用上一条按钮
function isPreviousDisabled(imageUrl: ContentKeys) {
  const texts = props.content[imageUrl] || [];
  const currentIndex = texts.indexOf(currentTexts[imageUrl]);
  return currentIndex === 0;
}

const initializeIsLastText = () => {
  Object.keys(props.content).forEach((imageUrl) => {
    isLastText[imageUrl] = props.content[imageUrl].length <= 1; // 如果文字只有一条，则默认是最后一条
  });
}

// methods:
function switchText(imageUrl: ContentKeys, direction: 'next' | 'previous') {
  const texts = props.content[imageUrl];
  const currentIndex = texts.indexOf(currentTexts[imageUrl]);

  if (direction === 'next') {
    if (currentIndex < texts.length - 1) {
      currentTexts[imageUrl] = texts[currentIndex + 1];
    } else {
      notification.value = '已经是最后一条了!';
    }
  } else if (direction === 'previous') {
    if (currentIndex > 0) {
      currentTexts[imageUrl] = texts[currentIndex - 1];
    } else {
      notification.value = '已经是第一条了!';
    }
  }
}

// 动态生成 Tooltip 内容
function getToolTipContent(imageUrl: string, direction: 'next' | 'previous') {
  if (direction === 'next') {
    return isNextDisabled(imageUrl) ? '已经是最后一条了!' : '下一条';
  } else {
    return isPreviousDisabled(imageUrl) ? '已经是第一条了!' : '上一条';
  }
}
const ininitFirstText = () => {
  Object.keys(props.content).forEach((imageUrl) => {
    currentTexts[imageUrl] = props.content[imageUrl][0]; // 初始化为第一条
  });
}

const toolTipContent = reactive<Record<string, string>>({});
const previousToolTipContent = reactive<Record<string, string>>({});

// 初始化 ToolTip 内容
const initializeToolTipContent = () => {
  Object.keys(props.content).forEach((imageUrl) => {
    toolTipContent[imageUrl] = '下一条';
    previousToolTipContent[imageUrl] = '上一条';
  });
}

onMounted(() => {
  try {
    // 如果 content 是空对象，则直接返回
    if (Object.keys(props.content).length === 0) {
      console.log('Content is empty, skipping initialization.');
      return;
    }

    // 初始化 content 和 currentTexts
    Object.keys(props.content).forEach((imageUrl) => {
      currentTexts[imageUrl] = props.content[imageUrl][0]; // 初始化为第一条
    });

    initializeToolTipContent();
    initializeIsLastText();
  } catch (error) {
    console.error('Error initializing data:', error);
  }

});

watch(
  () => props.content, // 监听 content
  () => {
    ininitFirstText();
    initializeToolTipContent();
    initializeIsLastText();
  },
  { immediate: true, deep: true } // deep: true 会监听内容的深层变化
);
watch(
  () => props.ParentLoading,
  (newParentLoading, oldParentLoading) => {
    console.log("ParentLoading changed:", newParentLoading);
    // 处理 ParentLoading 变化的逻辑
  },
  { immediate: true }
);

</script>

<style scoped></style>
