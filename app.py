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
import difflib
# import multiprocessing
from multiprocessing.pool import ThreadPool
# from multiprocessing import Pool
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
    print(request.json)
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
    print("数据：",request.json)
    url = 'http://172.188.112.9:5000/audiototext'# 请求接口
    req = requests.post(url, data=json.dumps(request.json), headers={'Content-Type': 'application/json'})
    print(req.json())
    return req.json()


@app.route('/search', methods=['POST'])  # 匹配接口
def search():
    print("接收请求，数据",request.json)
    url = 'http://172.188.112.9:5000/search'# 请求接口
    req = requests.post(url, data=json.dumps(request.json), headers={'Content-Type': 'application/json'})
    print("结果：",req.json())
    return req.json()


@app.route('/test', methods=['POST'])  # 用户基本信息维护
def test():
    print("接收到请求")
    return {
        'code': 200,
        'message': "注册成功！"
    }



@app.route('/')
def hello():
    return "Hello"


if __name__ == "__main__":
    # torch.multiprocessing.set_start_method('spawn')
    app.run(host='0.0.0.0', port=5000, debug=True)
