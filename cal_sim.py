from http import HTTPStatus
import dashscope
dashscope.api_key='replace_this_str_with_your_own_api'
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from torchvision import transforms
import json
from tqdm import tqdm

path = '/home2/menglingang/models/bert-base-chinese'
tokenizer = AutoTokenizer.from_pretrained(path)
model = AutoModel.from_pretrained(path)
train_path = '/home/menglingang/utils/SIGHAN2024_dimABSA_TrainingSet1_Simplified.json'

def calculate_cosine_similarity(s1, s2):
    with torch.no_grad():
        s1_inputs = tokenizer(s1, return_tensors='pt', padding=True, truncation=True)
        s1_outputs = model(**s1_inputs)
        s1_embeddings = s1_outputs.last_hidden_state.mean(dim=1)
        s2_inputs = tokenizer(s2, return_tensors='pt', padding=True, truncation=True)
        s2_outputs = model(**s2_inputs)
        s2_embeddings = s2_outputs.last_hidden_state.mean(dim=1)
    cos_sim = cosine_similarity(s1_embeddings,s2_embeddings)
    return cos_sim

def calculate_aspect_cosine_similarity(as1, as2):
    sim = 0
    for a1 in as1:
        for a2 in as2:
            sim = max(0, calculate_cosine_similarity(a1, a2))
    return sim

alpha_1 = 0.5
alpha_2 = 0.5
def sim(s1,s2,as1,as2):
    return alpha_1 * calculate_cosine_similarity(s1,s2) + alpha_2 * calculate_aspect_cosine_similarity(as1,as2)

with open(train_path,'r',encoding='utf-8') as f:
    data = json.load(f)
# s1 = "这款沙拉真是我的爱"
# as1 = ['沙拉']
# s2 = data[0]['Sentence']
# as2 = data[0]['Aspect']
# print(sim(s1,s2,as1,as2))


def sample_selector(s1, as1):
    sentences = {}
    for i in tqdm(range(len(data))):
        sentences.update({i: sim(s1, data[i]['Sentence'],as1,data[i]['Aspect'])})
    sorted_sentences = sorted(sentences.items(),key=lambda x:x[1],reverse=True)
    samples = ''
    for j in range(10):
        samples += '输入：(' + str(data[sorted_sentences[j][0]]['Sentence'])+')' + '输出：'
        for k in range(len(data[sorted_sentences[j][0]]['Intensity'])):
            samples += '(' + data[sorted_sentences[j][0]]['Aspect'][k] + ',' + data[sorted_sentences[j][0]]['Intensity'][k] + ')'
        samples += '。'
    return samples
