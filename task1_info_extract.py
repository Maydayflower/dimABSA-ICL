from tqdm import tqdm


# 提取数据集中每一条样本的信息 id sentence aspects
# task1 info
path = "C:/Users/10780/Desktop/task1s_info_left.txt"
sentences = []
ids = []
aspects = []
with open(path, 'r', encoding='UTF-8') as FA:
    for line in FA:
        line = line.split(',')
        ids.append(line[0])
        sentences.append(line[1])
        aspects.append(line[2])

sentences.pop(0)
ids.pop(0)
aspects.pop(0)
for i in tqdm(range(len(sentences))):     
    with open ('task1_info_left_true.txt', 'a', encoding='utf-8') as F:
        F.write(ids[i])
        F.write(' ')
        F.write(sentences[i])
        F.write(' ')
        F.write(aspects[i])

# task2 info
# path = "C:/Users/10780/Desktop/task1s_info_left.txt"
# sentences =[]
# ids = []
# with open(path, 'r', encoding='utf-8') as f:
#     for line in f:
#         line = line.split(', ')
#         ids.append(line[0])
#         sentences.append(line[1])
# for i in tqdm(range(len(sentences))):
#     with open('task1_info_left_true.txt', 'a', encoding='utf-8') as fa:
#         fa.write(ids[i])
#         fa.write(' ')
#         fa.write(sentences[i])
