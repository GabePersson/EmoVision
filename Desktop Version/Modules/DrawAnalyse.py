import base64
import io
import json
import time

import requests
from PIL import Image

# 获取 Access Token 的 URL
url = "https://aip.baidubce.com/oauth/2.0/token"


def get_access_token(client_id, client_secret):
    params = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.post(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        print("获取 Access Token 失败:", response.text)
        return None


def submit_image_understanding_request(access_token, image_data, question):
    image_base64 = base64.b64encode(image_data).decode('utf-8')

    url = f"https://aip.baidubce.com/rest/2.0/image-classify/v1/image-understanding/request?access_token={access_token}"
    headers = {'Content-Type': 'application/json'}
    body = {
        "image": image_base64,
        "question": question
    }

    response = requests.post(url, headers=headers, data=json.dumps(body))
    return response.json()


def get_image_understanding_result(access_token, task_id):
    url = f"https://aip.baidubce.com/rest/2.0/image-classify/v1/image-understanding/get-result?access_token={access_token}"
    headers = {'Content-Type': 'application/json'}
    body = {
        "task_id": task_id
    }

    response = requests.post(url, headers=headers, data=json.dumps(body))
    return response.json()


def submit_image_understanding_request_with_retry(access_token, image_data, question, retries=3):
    for i in range(retries):
        response = submit_image_understanding_request(access_token, image_data, question)
        if 'error_code' not in response:
            return response
        elif response.get('error_code') == 18:  # 请求限制错误
            print("请求限制达到，等待一段时间后重试...")
            time.sleep(5)  # 等待5秒后重试
        else:
            print("其他错误:", response)
            break
    return None


def predict(image: Image.Image):
    #TODO:请替换下面两项KEY
    CLIENT_ID = 'your_client_id'
    CLIENT_SECRET = 'your_client_secret'
    QUESTION = "分析这张图片的内容(128字以内)"

    access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)

    if access_token:
        # 将 PIL.Image 转换为字节数据
        with io.BytesIO() as output:
            image.save(output, format='JPEG')  # 根据需要选择合适的格式
            image_data = output.getvalue()

        submit_response = submit_image_understanding_request_with_retry(access_token, image_data, QUESTION)

        if submit_response and 'result' in submit_response:
            task_id = submit_response['result'].get('task_id')
            print("Task ID:", task_id)

            time.sleep(15)  # 根据需要调整

            result_response = get_image_understanding_result(access_token, task_id)
            if 'result' in result_response:
                description = result_response['result'].get('description')
                return description
            else:
                print("获取结果时出错:", result_response)
                return None
        else:
            print("提交请求时出错:", submit_response)
            return None
    else:
        print("无法获取 Access Token")
        return None


