import time

from PIL import Image
import requests

from Modules.GenerateImg import generate_image_from_text
from Modules.MusicPlayer import MusicPlayer
from Modules.VoiceRecognition import voice_input
from Modules.DrawAnalyse import predict as draw_predict
from Modules.EmoAnalyse import predict as face_predict
from Modules.TextEmoAnalyse import predict as text_predict

import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
import cv2
import os

SOURCES_ROOT = 'Srcs'
VOICE_PREDICT_SAVE_PATH = os.path.join(SOURCES_ROOT, 'prompt.txt')
VOICE_PREDICT_SAVE_DIR = os.path.dirname(VOICE_PREDICT_SAVE_PATH)
VIDEO_PICTURE_SAVE_PATH = os.path.join(SOURCES_ROOT, 'video_picture.png')
VIDEO_PICTURE_SAVE_DIR = os.path.dirname(VIDEO_PICTURE_SAVE_PATH)

GENERATION_DRAW_PICTURE_SAVE_PATH = os.path.join(SOURCES_ROOT, 'generation.jpg')

DRAW_PICTURE_SAVE_PATH = os.path.join(SOURCES_ROOT, 'drawing.png')
DRAW_PICTURE_SAVE_DIR = os.path.dirname(DRAW_PICTURE_SAVE_PATH)

DRAW_REF_PICTURE_SAVE_PATH = os.path.join(SOURCES_ROOT,"ref_drawing.png")

SERVER_IP = 'http://localhost:8001'


def sendData(data, datatype: str):
    if datatype not in ['face', 'text', 'draw']:
        return
    url = SERVER_IP + f'/{datatype}Data'
    requests.post(url, data=data)


# 设置页面标题
st.title("EmoVision")

# 创建侧边栏
st.sidebar.title("菜单")

# 绘画框设置
drawing_mode = st.sidebar.selectbox(
    "选择绘画模式：", ("freedraw", "line", "rect", "circle", "transform")
)
stroke_width = st.sidebar.slider("笔触宽度：", 1, 25, 3)
stroke_color = st.sidebar.color_picker("选择颜色：", "#000000")

# 侧边栏按钮
save_reference_image = st.sidebar.button("保存参考图像")
analyze_drawing = st.sidebar.button("绘画分析")
speech_recognition = st.sidebar.button("启用麦克风")
enable_camera = st.sidebar.button("启用摄像头")
enable_music = st.sidebar.button("开启音乐")

# 检查 session_state 中是否有值
if 'input_value' not in st.session_state:
    st.session_state.input_value = ''

# 输入字段和按钮
col1, col2 = st.columns([3, 1])
with col1:
    input_text = st.text_input("输入文本")
with col2:
    st.write("")  # 添加空行以调整按钮位置
    st.write("")  # 添加空行以调整按钮位置
    generate_image = st.button("文本生成图像")

# 使用 session state 管理状态
if "img" not in st.session_state:
    st.session_state.img = None
if "camera_enabled" not in st.session_state:
    st.session_state.camera_enabled = False
if "microphone_enabled" not in st.session_state:
    st.session_state.microphone_enabled = False

if "text_analyse" not in st.session_state:
    st.session_state.text_analyse = {}
elif st.session_state.text_analyse != {}:
    st.text(f"文本情感分析为{st.session_state.text_analyse}")

if "face_analyse" not in st.session_state:
    st.session_state.face_analyse = {}
elif st.session_state.face_analyse != {}:
    st.text(f"面部情感分析为{st.session_state.face_analyse}")

if "draw_analyse" not in st.session_state:
    st.session_state.draw_analyse = {}
elif st.session_state.draw_analyse != {}:
    st.text(f"绘画情感分析为{st.session_state.text_analyse}")

# 按下生成图像按钮后显示预定义图片
if generate_image:
    st.session_state.text_analyse = text_predict(input_text)

    sendData(st.session_state.text_analyse, "text")
    try:
        url = generate_image_from_text(input_text)
        # 发起请求并下载图像
        response = requests.get(url)

        if response.status_code == 200:  # 检查请求是否成功
            # 指定保存路径
            save_path = GENERATION_DRAW_PICTURE_SAVE_PATH  # 替换为你想要保存的路径
            with open(save_path, "wb") as f:
                f.write(response.content)  # 保存图像内容
            print(f"图像已保存到 {save_path}")
        else:
            print("下载失败，状态码:", response.status_code)

            st.session_state.img = Image.open(GENERATION_DRAW_PICTURE_SAVE_PATH)  # 替换为你的图片路径
    except:
        st.session_state.img = Image.open(os.path.join("Srcs", "sample_generation.jpg"))  # 替换为你的图片路径

# 显示预定义图片
if st.session_state.img is not None:
    st.image(st.session_state.img, caption="生成的图像", width=400)

# 启用麦克风功能
if speech_recognition:
    st.session_state.microphone_enabled = not st.session_state.microphone_enabled

if st.session_state.microphone_enabled:
    input_text = voice_input()
    if not os.path.exists(VOICE_PREDICT_SAVE_DIR):
        os.makedirs(VOICE_PREDICT_SAVE_DIR)
    with open(VOICE_PREDICT_SAVE_PATH, 'w', encoding='utf-8') as f:
        f.write(input_text + '\n')
    st.session_state.microphone_enabled = not st.session_state.microphone_enabled

if os.path.exists(VOICE_PREDICT_SAVE_PATH):
    with open(VOICE_PREDICT_SAVE_PATH, "r") as audio_file:
        btn = st.download_button(
            label="下载预测的文本",
            data=audio_file,
            file_name="prompt.txt",
            mime="text"
        )

# 启用摄像头功能
if enable_camera:
    st.session_state.camera_enabled = not st.session_state.camera_enabled

if st.session_state.camera_enabled:
    video_capture = cv2.VideoCapture(0)

    if not video_capture.isOpened():
        st.error("无法打开摄像头")
    else:
        while st.session_state.camera_enabled:
            ret, frame = video_capture.read()
            if not ret:
                st.error("无法读取摄像头数据")
                break
            cv2.imwrite(VIDEO_PICTURE_SAVE_PATH, frame)

            img = Image.open(VIDEO_PICTURE_SAVE_PATH)
            st.session_state.face_analyse = face_predict(img)
            sendData(st.session_state.face_analyse, "face")
            time.sleep(5)

        video_capture.release()

if os.path.exists(VIDEO_PICTURE_SAVE_PATH):
    with open(VIDEO_PICTURE_SAVE_PATH, "rb") as picture_file:
        btn = st.download_button(
            label="下载摄像头采样图片",
            data=picture_file,
            file_name="video_picture.png",
            mime="mine/png"
        )

# 输入字段和按钮
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("**手动绘制**")
with col2:
    submit_button = st.button("提交")

# 创建绘画框
canvas_result = st_canvas(
    fill_color="rgba(255, 255, 255, 1)",  # 白色背景
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color="#ffffff",
    update_streamlit=True,
    height=400,
    drawing_mode=drawing_mode,
    key="canvas",
)

# 保存参考图像
if save_reference_image:
    if st.session_state.img is not None:
        st.session_state.img.save(DRAW_REF_PICTURE_SAVE_PATH)
        st.success("参考图像已保存！")
        st.session_state.img = None
    else:
        st.error("没有生成的图像可保存！")

# 按下提交按钮后保存绘画框中的内容
if submit_button:
    if canvas_result.image_data is not None:
        image_data = canvas_result.image_data[:, :, :3]

        trans_image_data = cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB)

        # 使用cv2将图像保存为文件
        cv2.imwrite(DRAW_PICTURE_SAVE_PATH, trans_image_data)

        st.success(f"绘图已保存到 {DRAW_PICTURE_SAVE_PATH}")
        img = Image.open(DRAW_PICTURE_SAVE_PATH)
        st.session_state.draw_analyse = text_predict(draw_predict(img))
        sendData(st.session_state.draw_analyse, "draw")
    else:
        st.error("绘画框中没有内容可保存！")

if os.path.exists(DRAW_PICTURE_SAVE_PATH):
    with open(DRAW_PICTURE_SAVE_PATH, "rb") as draw_file:
        btn = st.download_button(
            label="下载绘画图片",
            data=draw_file,
            file_name="drawing.png",
            mime="mine/png"
        )
if os.path.exists(DRAW_REF_PICTURE_SAVE_PATH):
    with open(DRAW_REF_PICTURE_SAVE_PATH, "rb") as draw_file:
        btn = st.download_button(
            label="下载参考图片",
            data=draw_file,
            file_name="ref_drawing.png",
            mime="mine/png"
        )

if "text_analyse" not in st.session_state and st.session_state.text_analyse != {}:
    st.text(f"文本情感分析为{st.session_state.text_analyse}")

if "face_analyse" in st.session_state and st.session_state.face_analyse != {}:
    st.text(f"面部情感分析为{st.session_state.face_analyse}")

if "draw_analyse" in st.session_state and st.session_state.draw_analyse != {}:
    st.text(f"绘画情感分析为{st.session_state.draw_analyse}")

if enable_music:
    player = MusicPlayer()
    url = SERVER_IP + '/music'
    response = requests.get(url).text
    player.update_music_list(response)
    player.run()