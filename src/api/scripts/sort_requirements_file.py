import datetime


# 读取文件内容，排序并保存到新文件
def read_sort_and_save_packages(filename, output_filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    # 提取注释
    comments = [line.strip() for line in lines if line.strip().startswith('#')]

    # 去除注释和空行，只留下需要排序的包名
    package_lines = [line.strip() for line in lines if line.strip() and not line.startswith('#')]

    # 对包名进行排序
    package_lines.sort()

    # 将注释和排序后的包名合并
    sorted_content = comments + package_lines

    # 将排序后的内容写入新文件，注意文件结尾不多加'\n'
    with open(output_filename, 'w') as outfile:
        for i, line in enumerate(sorted_content):
            # 为每行末尾添加换行符，除了最后一行
            if i < len(sorted_content) - 1:
                outfile.write(line + '\n')
            else:
                outfile.write(line)


# 使用函数，指定你的源文件路径和输出文件路径
file = '../requirements.txt'
read_sort_and_save_packages(file, file)

print(f"Sorted packages have been saved to {file}")
print(datetime.datetime.now())
