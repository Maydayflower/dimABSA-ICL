from cal_sim import sample_selector
from http import HTTPStatus
import dashscope
from tqdm import tqdm
dashscope.api_key='replace_this_str_with_your_own_api'
# from tqdm import tqdm
import argparse


# Some casual prompt here.
# prompt = "给你一个句子\
# 你需要提取里面所有的aspect及句子中针对该方面的Valence值和Arousal值，\
# Valence和Arousal维度上的值1分别表示极高的负面情绪和低Arousal。\
# 相反，9表示极高的正面情绪和高Arousal，5表示中性和中等唤醒情绪。\
# Valence和Arousal值由一个标记标签（符号“#”）分隔。\
# 请注意，aspect可能是主体或者具有一定意义的名词。\
# 如果给出的句子是：柠檬酱也不会太油，塔皮对我而言稍软。则输出： (柠檬酱,5.67#5.5)(塔皮,4.83#5.0)\
# 返回结果为输出列表。\
# 下面是更多例子供你参考，你需要从中学习到如何尽量给出准确的Valence和Arousal值：\
# 输入：肉粿没有很焦脆。\
# 输出：(肉粿,4.0#5.0)\
# 输入：口感有点微妙\
# 输出：(口感,4.75#4.75)\
# 输入：很够味起司也很香\
# 输出：(起司,6.67#6.5)(起司,6.5#6.33)\
# 输入：他们家的泡菜很好吃\
# 输出：(泡菜,6.62#6.62)\
# 输入：口味偏甜\
# 输出：(口味,5.12#4.75)\
# 输入：服务还蛮好的\
# 输出：(服务,6.12#5.38)\
# 接下来，我会给你一些句子，请识别出我给你的句子中的所有aspect及其对应的Valence和Arousal，\
# 并以前面我给你的例子中的的输出格式返回结果\
# 请不要输出给定输出格式以外的文字。"
# prompt += "Respond using markdown."


# prompt = '给你一个句子：\
# 你需要提取里面所有的方面及句子中针对该方面的Valence值和Arousal值，\
# 比如，输入：柠檬酱也不会太油，塔皮对我而言稍软。\
# 输出： (柠檬酱,5.67#5.5)(塔皮,4.83#5.0)\
# 接下来，我会给你一些句子，请识别出我给你的句子中的所有方面及其对应的Valence和Arousal，\
# 并以前面我给你的例子中的的输出格式返回结果\
# 注意，如果对一个方面存在多个评价，则会针对该方面给出多个输出。严禁输出答案以外的文字，必须只输出结果。'
# prompt setting 3 random select
# prompt = '你是情感分析方面的专家，非常擅长根据用户给出的评论来判断他们对某一个物品的情感偏向（Valence）和情感强度（Arousal）\
# 现在，给你一个句子：\
# 你需要提取里面所有的方面及句子中针对该方面的Valence值和Arousal值，\
# 比如，输入：柠檬酱也不会太油，塔皮对我而言稍软。\
# 输出： (柠檬酱,5.67#5.5)(塔皮,4.83#5.0)\
# 下面是更多例子供你参考，你需要从中学习到如何尽量给出准确的Valence和Arousal值：\
'



prompt = '
现在，给你一个句子：\
你需要提取里面所有的方面及句子中针对该方面的Valence值和Arousal值，\
比如，输入：柠檬酱也不会太油，塔皮对我而言稍软。\
输出： (柠檬酱,5.67#5.5)(塔皮,4.83#5.0)\
下面是更多例子供你参考，你需要从中学习到如何尽量给出准确的Valence和Arousal值：\
'




# category :'食物#品质', '食物#份量与款式', '服务#概括', '食物#价格', '地点#概括', '氛围#概括', '餐厅#杂项', 
#           '餐厅#价格', '饮料#品质', '餐厅#概括', '饮料#价格', '饮料#份量与款式'
task2_prompt = "给你一个句子，请你提取出句子中的每一个实体，并提取出句子中对他们的描述，然后给出实体的valence值和arousal值，\
                Valence和Arousal为1时分别表示极高的负面情绪和低强度。\
                相反，9表示极高的正面情绪和高强度，5表示中性情绪和中等强度。\
                Valence和Arousal值由一个标记标签（符号“#”）分隔。\
                接下来我会给你一个例子：\
                输入：不仅餐点美味上菜速度也是飞快耶!! 输出：(餐点, 美味, 6.63#4.63) (上菜速度, 飞快, 7.25#6.00)\
                其中“餐点”是aspect，“美味”是对“餐点”的描述，“6.63#4.63”是餐点对应的valence和arousal值\
                下面是更多例子供你参考，你需要从中学习到如何提取出对实体的描述，并且尽量给出准确的Valence和Arousal值：\
                输入：餐厅的价位完全不贵。 输出：(价位, 完全不贵, 6.88#6.5)\
                输入：肉吃起来鲜嫩多汁。 输出：(肉, 鲜嫩多汁, 6.33#6.17)\
                输入：没想到炸韭菜卷的面衣一样酥脆。 输出：(炸韭菜卷的面衣, 酥脆, 6.62#5.88)\
                输入：羊肉拉面趁热吃不错。 输出：(羊肉拉面, 不错, 5.75#5.0)\
                接下来我会给你一个输入，请你给出输出："



task3_prompt = "给你一个句子，请你提取出句子中的每一个aspect，并提取出句子中对他们的描述和他们属于的类别，然后给出他们的valence值和arousal值，\
                aspect应该是情绪主体，通常为名词,可能会重复出现\
                Valence和Arousal维度上的值1分别表示极高的负面情绪和低Arousal。\
                相反，9表示极高的正面情绪和高Arousal，5表示中性和中等唤醒情绪。\
                Valence和Arousal值由一个标记标签（符号“#”）分隔。\
                valence值和arousal值之间用#连接，\
                接下来我会给你一个例子：\
                输入：这碗拉面超级无敌霹雳难吃 输出：(拉面, 食物#品质, 超级无敌霹雳难吃, 2.00#7.88)\
                其中“拉面”是aspect，“食物#品质”是“拉面”的类别，“超级无敌霹雳难吃”是对“拉面”的描述，“2.00#7.88”是对应的valence和arousal值\
                我会为你提供一些例子供你学习：\
                输入：感觉很久没吃到这么好吃的烧腊饭了。 输出：(烧腊饭, 食物#品质, 好吃, 6.25#5.62)\
                输入：菜色非常丰富。 输出：(菜色, 食物#份量与款式, 非常丰富, 6.83#6.67)\
                输入：鸡肉的肉汁很丰富。 输出：(鸡肉的肉汁, 食物#品质, 很丰富, 6.62#6.5)\
                输入：黑麻糬的店面蛮好找。 输出：(黑麻糬的店面, 地点#概括, 蛮好找, 5.5#5.25)\
                下面我会给你一个句子，请严格按照例子中的输出格式返回答案，不要输出任何多余的字符"


creation_params = {
    "temperature": 1.0,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0,
}

def chat(mess):
    response = dashscope.Generation.call(
        dashscope.Generation.Models.qwen_plus,
        messages=mess,
        result_format='message',  # set the result to be "message" format.
    )

    res = response['output']['choices'][0]['message']['content'] if response.status_code == HTTPStatus.OK else 'null'
    return res


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--prompt", type=str, default=None)
    arg_parser.add_argument("--load", type=str, default=None)
    arg_parser.add_argument("--save", type=str, default=None)
    arg_parser.add_argument("--temperature", type=float, default=creation_params["temperature"],
                            help="The higher the value, the random the text.")
    arg_parser.add_argument("--frequency_penalty", type=float, default=creation_params["frequency_penalty"],
                            help="The higher the value, the less repetitive text.")
    arg_parser.add_argument("--presence_penalty", type=float, default=creation_params["presence_penalty"],
                            help="The higher the value, the more likely the model will talk about new topics.")
    # arg_parser.add_argument("--max_tokens", type=int, default=creation_params["max_tokens"],
    #                         help="The maximum number of tokens to generate.")
    # arg_parser.add_argument("--n", type=int, default=1,
    #                         help="How many chat completion choices to generate for each input message.")
    args = arg_parser.parse_args()

    args.prompt = prompt + "\n" + args.prompt if args.prompt is not None else prompt
# ------------------------task1------------------------
    # 处理数据得到id sentence aspects
    path = "C:/Users/10780/Desktop/dimABSA_TestingSet/SIGHAN2024_dimABSA_Testing_Task1_Simplified.txt"
    sentences = []
    ids = []
    aspects = []
    with open('/home/menglingang/utils/task1s_info_true.txt', 'r', encoding='UTF-8') as FA:
        for line in FA:
            line = line.split('  ')
            ids.append(line[0])
            sentences.append(line[1])
            aspects.append(line[2])
    # # 运行
    for i in tqdm(range(2000)):
        samples = sample_selector(sentences[i], aspects[i])
        mess = [{"role": "system", "content": prompt+samples}, ]
        mess.append({"role": "user", "content": "请严格按输出格式(服务,6.12#5.38)给出句子："+sentences[i]+"中的以下aspect的valence和arousal值："+aspects[i]+"请注意括号的使用以确保格式一致。"})
        with open('task1s_qwen_plus_prompt_setting5.txt', 'a', encoding='utf-8') as file:
            file.write(ids[i])
            file.write(' ')
            file.write(chat(mess))
            file.write('\n')


# ------------------------task2------------------------
    # task2_path = "C:/Users/10780/Desktop/dimABSA_TestingSet/SIGHAN2024_dimABSA_Testing_Task2+3_Simplified.txt"
    # task2_sentences = []
    # task2_ids = []
    # with open(task2_path, 'r', encoding='UTF-8') as FA:
    #     for line in FA:
    #         line = line.split(', ')
    #         task2_ids.append(line[0])
    #         task2_sentences.append(line[1])
    # task2_sentences.pop(0)
    # task2_ids.pop(0)

    # for i in tqdm(range(len(task2_sentences))):
    #     mess = [{"role": "system", "content": task2_prompt}, ]
    #     mess.append({"role": "user", "content": "请严格按输出格式(餐点, 美味, 6.63#4.63)给出句子："+task2_sentences[i]+"中的aspect，描述和valence/arousal值，不要输出任何多余字符"})
    #     with open('task2.txt', 'a', encoding='utf-8') as file:
    #         file.write(task2_ids[i])
    #         file.write(' ')
    #         file.write(chat(mess))
    #         file.write('\n')




# ------------------------task3------------------------
#     task3_path = "C:/Users/10780/Desktop/dimABSA_TrainingSetValidationSet/dimABSA_TrainingSet&ValidationSet/dimABSA_Validation/SIGHAN2024_dimABSA_Validation_Task2+3_Simplified.txt"
#     task3_sentences = []
#     task3_ids = []
#     with open(task3_path, 'r', encoding='UTF-8') as FA:
#         for line in FA:
#             line = line.split(' ')
#             task3_ids.append(line[0])
#             task3_sentences.append(line[1])
#     task3_sentences.pop(0)
#     task3_ids.pop(0)
#
#     for i in tqdm(range(100)):
#         task3_sentences[i] = task3_sentences[i][:-2]
#         mess = [{"role": "system", "content": task3_prompt}, ]
#         mess.append({"role": "user", "content": task3_sentences[i]})
#         with open('task3.txt', 'a', encoding='utf-8') as file:
#             file.write(task3_ids[i][:-1])
#             file.write(' ')
#             file.write(chat(mess))
#             file.write('\n')

# do interface
# sent = "除了舒适的氛围外，COFFEE LAW 敦南概念店的餐点更是吸引人的亮点"
# mess = [{"role": "system", "content": prompt}, ]
# mess.append({"role": "user", "content": sent})
# print(chat(mess))



