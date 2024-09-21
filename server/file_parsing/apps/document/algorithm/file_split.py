import re
import jieba
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')


def to_keywords(input_string):
    """将句子转成检索关键词序列"""
    # 按搜索引擎模式分词
    word_tokens = jieba.cut_for_search(input_string)
    # 加载停用词表
    stop_words = set(stopwords.words('chinese'))
    # 去除停用词
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    return ' '.join(filtered_sentence)


def sent_tokenize(input_string):
    """按标点断句"""
    # 按标点切分
    sentences = re.split(r'(?<=[。！？；?!])', input_string)
    # 去掉空字符串
    return [sentence for sentence in sentences if sentence.strip()]


def split_text(paragraphs, chunk_size=128, overlap_size=32):
    '''按指定 chunk_size 和 overlap_size 交叠割文本'''
    sentences = [s.strip() for p in paragraphs for s in sent_tokenize(p)]
    chunks = []
    i = 0
    while i < len(sentences):
        chunk = sentences[i]
        overlap = ''
        prev_len = 0
        prev = i - 1
        # 向前计算重叠部分
        while prev >= 0 and len(sentences[prev]) + len(overlap) <= overlap_size:
            overlap = sentences[prev] + ' ' + overlap
            prev -= 1
        chunk = overlap + chunk
        next = i + 1
        # 向后计算当前chunk
        while next < len(sentences) and len(sentences[next]) + len(chunk) <= chunk_size:
            chunk = chunk + ' ' + sentences[next]
            next += 1
        chunks.append(chunk)
        i = next
    return chunks


if "__main__" == __name__:
    # 测试关键词提取
    # print(to_keywords("小明硕士毕业于中国科学院计算所，后在日本京都大学深造"))
    # 测试断句
    # print(sent_tokenize("这是，第一句。这是第二句吗？是的！啊"))
    paragraphs = input('paragraphs: ')
    chunks = split_text(paragraphs, 128, 32)
    print(chunks)
    print('lll', len(chunks), chunks[1])
