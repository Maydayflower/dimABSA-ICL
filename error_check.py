# 检查qwen生成的aspect与目标aspect不匹配的样本
from tqdm import tqdm


sentences = []
ids = []
aspects = []
path = "C:/Users/10780/Desktop/dimABSA_TestingSet/SIGHAN2024_dimABSA_Testing_Task1_Simplified.txt"

with open(path, 'r', encoding='UTF-8') as FA:
    for line in FA:
        line = line.split(',')
        ids.append(line[0])
        sentences.append(line[1])
        line[2] = line[2][:-1]
        line[2] = line[2][1:]
        #得到gt aspect list
        aspects.append(line[2].split('#'))

# pred_aspect 存储预测得到的aspect
pred_aspect = []
pred_file = "task1s_qwen_plus_prompt_setting4.txt"
with open(pred_file, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.split(' ')
        a = []
        pred_aspects = line[1].split(')')
        for i in pred_aspects:
            i=i[1:]
            i=i.split(',')[0]
            a.append(i)
        a = a[:-1]
        pred_aspect.append(a)

# sample =0
# print(aspects[sample], pred_aspect[sample])

for sample in range(len(aspects)):
    #如果预测得到的aspect list和gt不相等 记下来出错的样本编号
    if aspects[sample] != pred_aspect[sample]:
        with open('qwen_s4_error_list.txt', 'a', encoding='utf-8') as e:
            e.write(ids[sample])
            e.write('\n')


