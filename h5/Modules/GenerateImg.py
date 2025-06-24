import erniebot
import requests
import time
import re

# Set ErnieBot API type and access token
# TODO：修改为你的文生文API密匙
erniebot.api_type = "aistudio"
erniebot.access_token = "your_erniebot_token"

# Set Baidu API credentials
# TODO：修改为你的文生图API密匙
client_id = 'your_client_id'
client_secret = 'your_client_secret'
access_token = None


# Function to retrieve the access token
def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
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
        data = response.json()
        return data.get('access_token')
    else:
        print("Failed to get access token:", response.text)
        return None


# Function to optimize the text prompt
def optimize_text_prompt(input_text):
    response = erniebot.ChatCompletion.create(
        model="ernie-3.5",
        messages=[{
            "role": "user",
            "content": "将以下内容优化为文生图的提示词，字数不要太多：" + input_text
        }],
        top_p=0.95,
        stream=False
    )

    result = response.get_result()
    matches = re.findall(r'"(.*?)"', result)
    return matches[0] if matches else ""


# Function to submit image request
def submit_image_request(text, style='油画', resolution='1024*1024', num=1):
    url = f'https://aip.baidubce.com/rpc/2.0/wenxin/v1/basic/textToImage?access_token={access_token}'
    headers = {'Content-Type': 'application/json'}
    body = {
        "text": text,
        "style": style,
        "resolution": resolution,
        "num": num
    }

    response = requests.post(url, headers=headers, json=body)
    return response.json()


# Function to get the image result
def get_image_result(task_id):
    url = f'https://aip.baidubce.com/rpc/2.0/wenxin/v1/basic/getImg?access_token={access_token}'
    headers = {'Content-Type': 'application/json'}
    body = {"taskId": task_id}

    response = requests.post(url, headers=headers, json=body)
    return response.json()


# Function to download the image
def download_image(image_url, filename):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Image saved successfully: {filename}")
    else:
        print("Failed to download image:", response.text)


# Main function to generate the image from text
def generate_image_from_text(input_text):
    global access_token

    # Get access token if not already obtained
    if not access_token:
        access_token = get_access_token()
        if not access_token:
            print("Failed to get access token.")
            return None

    # Optimize the text prompt
    optimized_text = optimize_text_prompt(input_text)
    if not optimized_text:
        print("Failed to optimize the text prompt.")
        return None

    # Submit image request
    result = submit_image_request(optimized_text)
    task_id = result.get('data', {}).get('taskId')
    if not task_id:
        print("Failed to submit image request:", result)
        return None

    # Wait for the image generation to complete
    while True:
        time.sleep(5)  # Check every 5 seconds
        status_result = get_image_result(task_id)
        status = status_result.get('data', {}).get('status')

        if status == 1:
            image_url = status_result['data']['imgUrls'][0]['image']
            print("Image generated successfully, URL:", image_url)
            return image_url  # Return image URL
        elif status == 0:
            print("Image is being generated, please wait...")
        else:
            print("Failed to get image status:", status_result)
            return None
