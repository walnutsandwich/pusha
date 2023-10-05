import requests
import json
import uuid

class FakeGPT:
    def __init__(self) -> None:
        # self.message_id = str(uuid.uuid4())
        self.conversation_id = None
        self.parent_message_id = str(uuid.uuid4())
        self.headers = {
            'Accept': 'text/event-stream',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Content-Type': 'application/json',
            'Origin': 'https://xiaoyingchat.zeabur.app',
            'Referer': 'https://xiaoyingchat.zeabur.app/',
            'Sec-Ch-Ua': '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.43',
            'X-Authorization': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJ4aWFveWluZ3dhbmdsdW82MDFAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWV9LCJodHRwczovL2FwaS5vcGVuYWkuY29tL2F1dGgiOnsidXNlcl9pZCI6InVzZXItNk5GYmxVa2phYm8xYkF5ZVhMVnJWcmVnIn0sImlzcyI6Imh0dHBzOi8vYXV0aDAub3BlbmFpLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwMDE5MDQ4MjkxNTY0MDMzOTA5MyIsImF1ZCI6WyJodHRwczovL2FwaS5vcGVuYWkuY29tL3YxIiwiaHR0cHM6Ly9vcGVuYWkub3BlbmFpLmF1dGgwYXBwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2OTU4MTU1MjMsImV4cCI6MTY5NzAyNTEyMywiYXpwIjoiVGRKSWNiZTE2V29USHROOTVueXl3aDVFNHlPbzZJdEciLCJzY29wZSI6Im9wZW5pZCBlbWFpbCBwcm9maWxlIG1vZGVsLnJlYWQgbW9kZWwucmVxdWVzdCBvcmdhbml6YXRpb24ucmVhZCBvcmdhbml6YXRpb24ud3JpdGUgb2ZmbGluZV9hY2Nlc3MifQ.SwdKdMIinup8v19A5_4qxxW7-5PX_BVmYzqx4b7lx1fVXVFCDh1PD2tWyD1-JK2MHmGi1mYCVxk1ho7B56jAwtRsY7vx1q5S_YEwn5LtOdY-KlchQBLhlTzVMMdRk2KNVNgUGYj_i0ajsXF8KNc5nWnvy4sLrMv_IgoEt3vfnXu8yhx8q8RSePqQQHsrHPEwGT36H8pvijChLlcOk3bDKp7WCevp-71j1pq5KPBFjWcZIF8dKq7W_cLDnRgjTtuXf9VAgJsYnHJzOvCS11Wh1nPc3VKYZ1voUdrYuhZzowd_YNu_KaGkttRqfi6cNX2JoKhZhp24rnDYLZnUg-pB_A'
        }
        # URL目标地址
        self.url = "https://ai.fakeopen.com/api/conversation"
    
    def make_post(self,input_str):
        # 请求负载
        if( self.conversation_id ):
            payload = {
                "action": "next",
                "messages": [{
                    "id": str(uuid.uuid4()),
                    "author": {"role": "user"},
                    "content": {
                        "content_type": "text",
                        "parts": [input_str]
                    }
                }],
                "conversation_id": self.conversation_id,
                "parent_message_id": self.parent_message_id,
                "model": "gpt-4",
                "timezone_offset_min": -480,
                "history_and_training_disabled": False
            }
        else:
            payload = {
                "action": "next",
                "messages": [{
                    "id": str(uuid.uuid4()),
                    "author": {"role": "user"},
                    "content": {
                        "content_type": "text",
                        "parts": [input_str]
                    }
                }],
                "parent_message_id": str(uuid.uuid4()),
                "model": "gpt-4",
                "timezone_offset_min": -480,
                "history_and_training_disabled": False
            }

        response = requests.post(url=self.url, headers=self.headers, json=payload,timeout=20)
        if(response.status_code == 200 ):
            return response.text
        else:
            raise requests.exceptions.RequestException("请求失败")

    def get_result(self,input_str):
        try:
            data_strs =  self.make_post(input_str)

            finished_messages = []
            data_strs = data_strs.split("\n\n")
            # 循环处理每一个数据对象
            for data_str in data_strs:
                # print("data_str:",data_str)
                # 将字符串转换为Python字典
                json_str = data_str.replace("data: ", "", 1).strip()
                try:
                    data_dict = json.loads(json_str)
                    self.conversation_id = data_dict['conversation_id']
                    self.parent_message_id = data_dict['message']['id']
                    # 检查消息状态是否为 "finished_successfully"
                    if data_dict["message"]["status"] == "finished_successfully":
                        finished_messages.append(data_dict["message"]["content"]["parts"][0])
                except json.JSONDecodeError:
                    # print(f"解析失败的字符串: {json_str}")
                    None

            if finished_messages:
                return finished_messages[-1]
            else:
                return None
        except:
            return None

if __name__ == '__main__':
    fakegpt = FakeGPT()
    user_input = input("请输入内容: ")
    while user_input:
        # 打印返回内容
        print(fakegpt.get_result(user_input) )
        user_input = input("请输入内容: ")