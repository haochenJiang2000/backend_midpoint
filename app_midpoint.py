import random
from flask import Flask, request, render_template, make_response
from flask_caching import Cache
import json
import re
import logging
import time, datetime
from flask_cors import CORS
import sqlite3
import copy
import requests
import os
# import torch
import argparse
import base64
import subprocess
# from concurrent.futures import ThreadPoolExecutor
from pprint import pprint
import difflib
# import multiprocessing
from multiprocessing.pool import ThreadPool
# from multiprocessing import Pool
from utils.sendEmail import sendEmail, sendVerifyEmail
from utils.cache import Cache
# from ChatbotVoice import mychat
# # from utils.GPU_autochoice import GPUManager
# from werkzeug.utils import secure_filename
# from flask import send_file
# import tempfile
# import base64
# from table_access import JobStatusDataAccess

# from Zero_Haruhi_main.ChatHaruhi import ChatHaruhi
# from Zero_Haruhi_main.ChatHaruhi.response_openai import get_response
# import gradio as gr
# import os
# import openai

# import re
# from html import unescape
# import soundfile as sf
# import azure.cognitiveservices.speech as speechsdk
# from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, AudioConfig
# from pydub import AudioSegment
# import io

key = "a80e905335c74fb589144adee45b9920"
key_bytes = key.encode()
BASE_URL = "https://canadaazureopenai.openai.azure.com/";

os.environ["AZURE_OPENAI_KEY"] = key_bytes.decode('utf-8')
os.environ["AZURE_OPENAI_URL"] = BASE_URL

speech_subscription_key = "68d5466241bf45379304b107567960ac"
speech_service_region = "eastus"

# ==========================flask uwsgi设置======================================#
processes = 2
pool = ThreadPool(processes=processes)
# pool = multiprocessing.Pool(processes=2)

# executor = ThreadPoolExecutor(6)
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

cache = Cache()
cache.set('all_task', list())  # 设置一个缓存对象

logger = logging.getLogger(__file__)
logger.setLevel(level=logging.INFO)
start_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
handler = logging.FileHandler('./logs/log_2023.txt'.format(str(start_time)))
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info("日志系统启动")
# annotator = ZhAnnotator.create_default(annotator_id=0)
logger.info("进程队列初始化")

# all_task = list()   # 收集当前运行进程
d = difflib.Differ()
# BATCH_SIZE = 6
# DEVICE = [0]
# GM = GPUManager(DEVICE)
# =================================================================#
@app.route('/tableaccess', methods=['POST'])  # 轮询接口
def tableaccess():
    url = 'http://172.188.112.9:5000/tableaccess'# 请求接口
    req = requests.post(url, data=json.dumps(request.json), headers={'Content-Type': 'application/json'})
    return req.json()


@app.route('/chat', methods=['POST'])  # 聊天接口
def chat():
    url = 'http://172.188.112.9:5000/chat'# 请求接口
    req = requests.post(url, data=json.dumps(request.json), headers={'Content-Type': 'application/json'})
    return req.json()


@app.route('/commonchat', methods=['POST'])  # 通用问答，给出三个角色的回复
def commonchat():
    url = 'http://172.188.112.9:5000/commonchat'# 请求接口
    req = requests.post(url, data=json.dumps(request.json), headers={'Content-Type': 'application/json'})
    return req.json()


@app.route('/getaudio1')  # 获得音频文件
def getaudio1():
    url = 'http://172.188.112.9:5000/getaudio1'# 请求接口
    req = requests.post(url, data=json.dumps(request.json), headers={'Content-Type': 'application/json'})
    return req.json()

@app.route('/getaudio2')  # 获得音频文件
def getaudio2():
    url = 'http://172.188.112.9:5000/getaudio2'# 请求接口
    req = requests.post(url, data=json.dumps(request.json), headers={'Content-Type': 'application/json'})
    return req.json()

@app.route('/getaudio3')  # 获得音频文件
def getaudio3():
    url = 'http://172.188.112.9:5000/getaudio3'# 请求接口
    req = requests.post(url, data=json.dumps(request.json), headers={'Content-Type': 'application/json'})
    return req.json()


@app.route('/audiototext', methods=['POST'])  # 聊天接口
def audiototext():
    url = 'http://172.188.112.9:5000/audiototext'# 请求接口
    req = requests.post(url, data=json.dumps(request.json), headers={'Content-Type': 'application/json'})
    return req.json()


@app.route('/search', methods=['POST'])  # 匹配接口
def search():
    url = 'http://172.188.112.9:5000/search'# 请求接口
    req = requests.post(url, data=json.dumps(request.json), headers={'Content-Type': 'application/json'})
    return req.json()


@app.route('/update_information', methods=['POST'])  # 用户基本信息维护
def update_information():
    url = 'http://172.188.112.9:5000/update_information'# 请求接口
    req = requests.post(url, data=json.dumps(request.json), headers={'Content-Type': 'application/json'})
    return req.json()


@app.route('/information', methods=['POST'])  # 请求用户基本信息
def information():
    url = 'http://172.188.112.9:5000/information'# 请求接口
    req = requests.post(url, data=json.dumps(request.json), headers={'Content-Type': 'application/json'})
    return req.json()



@app.route('/autochat', methods=['POST'])  # AI自动回复，给出一些推荐
def autochat():
    url = 'http://172.188.112.9:5000/autochat'# 请求接口
    req = requests.post(url, data=json.dumps(request.json), headers={'Content-Type': 'application/json'})
    return req.json()


@app.route('/Chatmemory', methods=['POST'])  # 请求长期记忆数据
def Chatmemory():
    url = 'http://172.188.112.9:5000/Chatmemory'# 请求接口
    req = requests.post(url, data=json.dumps(request.json), headers={'Content-Type': 'application/json'})
    return req.json()


@app.route('/UpdateChatmemory', methods=['POST'])  # 更新长期记忆
def UpdateChatmemory():
    url = 'http://172.188.112.9:5000/UpdateChatmemory'# 请求接口
    req = requests.post(url, data=json.dumps(request.json), headers={'Content-Type': 'application/json'})
    return req.json()


@app.route('/roleinformation', methods=['POST'])  # 请求角色信息
def roleinformation():
    url = 'http://172.188.112.9:5000/roleinformation'# 请求接口
    req = requests.post(url, data=json.dumps(request.json), headers={'Content-Type': 'application/json'})
    return req.json()


@app.route('/')
def hello():
    return "Hello"


if __name__ == "__main__":
    # torch.multiprocessing.set_start_method('spawn')
    app.run(host='0.0.0.0', port=81, debug=True)