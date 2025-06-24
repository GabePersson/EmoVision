import base64
import PIL
import requests
import json
import time
import io
from PIL import Image

url = "https://aip.baidubce.com/oauth/2.0/token"

# 通过 params 传递参数
params = {
    'grant_type': 'client_credentials',
    'client_id': 'client_id',  # 替换为你的 client_id
    'client_secret': 'client_secret'  # 替换为你的 client_secret
}

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

# 发送请求
response = requests.post(url, headers=headers, params=params)

# 检查响应状态
if response.status_code == 200:
    # 解析并打印 access_token
    data = response.json()
    access_token = data.get('access_token')
    print("Access Token:", access_token)
else:
    print("获取 Access Token 失败:", response.text)


def submit_image_request(text, image_data, style='黑白线条', resolution='1024*1024', num=1):
    image_base64 = base64.b64encode(image_data).decode('utf-8')
    url = f'https://aip.baidubce.com/rpc/2.0/ernievilg/v1/txt2imgv2?access_token={access_token}'
    headers = {
        'Content-Type': 'application/json'
    }
    body = {
        "prompt": "黑白素描 极简风格" + text,
        "style": style,
        "width": 1024,
        "height": 1024,
        "resolution": resolution,
        "num": num,
        "image": image_base64,
        "change_degree": 5
    }

    response = requests.post(url, headers=headers, json=body)
    return response.json()


def get_image_result(access_token, task_id):
    url = f"https://aip.baidubce.com/rpc/2.0/ernievilg/v1/getImgv2?access_token={access_token}"
    headers = {'Content-Type': 'application/json'}
    body = {
        "task_id": task_id
    }

    response = requests.post(url, headers=headers, data=json.dumps(body))
    return response.json()


def download_image(image_url, filename):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"图片保存成功: {filename}")
    else:
        print("下载图片失败:", response.text)


def generate(image_path: str, prompt: str):
    image = PIL.Image.open(image_path)
    with io.BytesIO() as output:
        image.save(output, format='PNG')  # 根据需要选择合适的格式
        image_data = output.getvalue()

        # 提交请求
    result = submit_image_request(prompt, image_data)
    task_id = result.get('data', {}).get('task_id')
    result = None
    while True:
        time.sleep(5)  # 每5秒查询一次
        status_result = get_image_result(access_token, task_id)

        # 检查状态
        status = status_result.get('data', {}).get('task_status')

        if status == "SUCCESS":
            # 获取图片链接
            image_url = status_result['data']['sub_task_result_list'][0]['final_image_list'][0]['img_url']
            print("图片生成成功，图片链接:", image_url)
            result = image_url
            break
        elif status == "RUNNING":
            print("图片正在生成，继续等待...")
        else:
            print("查询状态失败:", status_result)
            break
    return result


if __name__ == '__main__':
    text = input()
