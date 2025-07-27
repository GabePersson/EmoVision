import os

import paddle
import numpy as np
from functools import partial
import paddle.nn.functional as F
from paddlenlp.datasets import load_dataset
from paddlenlp.data import Stack, Tuple, Pad
from paddlenlp.transformers import SkepForSequenceClassification, SkepTokenizer


def convert_data(data, tokenizer, max_seq_length=256, is_test=False):
    encoded_inputs = tokenizer(
        text=data["text"], max_seq_len=max_seq_length)

    input_ids = encoded_inputs["input_ids"]

    token_type_ids = encoded_inputs["token_type_ids"]

    if not is_test:
        label = np.array([data["label"]], dtype="int64")
        return input_ids, token_type_ids, label
    else:
        qid = np.array([data["qid"]], dtype="int64")
        return input_ids, token_type_ids, qid


def create_dataloader(dataset, trans_fn=None, mode='train', batch_size=1, use_gpu=False, pad_token_id=0,
                      batchify_fn=None):
    if trans_fn:
        dataset = dataset.map(trans_fn)

    if mode == 'train' and use_gpu:
        sampler = paddle.io.DistributedBatchSampler(dataset=dataset, batch_size=batch_size, shuffle=True)
    else:
        shuffle = True if mode == 'train' else False
        sampler = paddle.io.BatchSampler(dataset=dataset, batch_size=batch_size, shuffle=shuffle)  # 生成一个取样器
    dataloader = paddle.io.DataLoader(dataset, batch_sampler=sampler, return_list=True, collate_fn=batchify_fn)
    return dataloader


BATCH_SIZE = 1
model = SkepForSequenceClassification.from_pretrained(pretrained_model_name_or_path='skep_ernie_1.0_large_ch',
                                                      num_classes=6)
tokenizer = SkepTokenizer.from_pretrained('skep_ernie_1.0_large_ch')
model.set_dict(paddle.load(os.path.join("Srcs/TextModel/model_state.pdparams")))
model.eval()

# 处理测试集数据
trans_func = partial(
    convert_data,
    tokenizer=tokenizer,
    max_seq_length=256,
    is_test=True)
batchify_fn = lambda samples, fn=Tuple(
    Pad(axis=0, pad_val=tokenizer.pad_token_id),
    Pad(axis=0, pad_val=tokenizer.pad_token_type_id),
    Stack()
): [data for data in fn(samples)]

labels = {'happy': '0', 'angry': '1', 'sad': '2', 'fear': '3', 'surprise': '4', 'neutral': '5'}

def predict(text):
    global labels
    test = load_dataset("chnsenticorp", splits=['test'])
    test.data = [{'text': text, 'label': '', 'qid': '0'}]
    test.new_data = [{'text': text, 'label': '', 'qid': '0'}]

    data_loader = create_dataloader(
        test,
        mode='test',
        batch_size=BATCH_SIZE,
        batchify_fn=batchify_fn,
        trans_fn=trans_func)

    for batch in data_loader:
        input_ids, token_type_ids, qids = batch
        # 喂数据给模型
        logits = model(input_ids, token_type_ids)
        # 预测分类
        probs = F.softmax(logits, axis=-1).tolist()[0]
        label = {
            key: probs[int(value)] for key, value in labels.items()
        }
        return label


if __name__ == '__main__':
    print(predict("你好世界"))
