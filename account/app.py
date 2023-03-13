import requests
import json
import gradio as gr

def get_token(username, password):
    try:
        url = "https://api-vngpt.aivgroup.vn/api/auth/login/"

        payload = json.dumps({
        "username": username,
        "password": password
        })
        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        response = response.json()
        return response["key"], gr.update(value="""<i style="color:#3ADF00"><center>Đăng nhập thành công. Mời sử dụng</center></i>""")
    except:
        return "", gr.update(value="""<i style="color:red"><center>Tài khoản hoặc mật khẩu không đúng. Xin thử lại</center></i>""")
