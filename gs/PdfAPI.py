import requests
from config import *

class PdfApi():
    def __init__(self) -> None:
        self.x_api_key = X_API_KEY
    
    def add_adf_via_url(self, path):
        files = [
            ('file', ('file', open(path, 'rb'), 'application/octet-stream'))
        ]
        headers = {
            'x-api-key': self.x_api_key
        }

        response = requests.post(
            'https://api.chatpdf.com/v1/sources/add-file', headers=headers, files=files)

        if response.status_code == 200:
            print('Source ID:', response.json()['sourceId'])
            return response.json()['sourceId']
        else:
            print('Status:', response.status_code)
            print('Error:', response.text)
            
    def ask_of_pdf(self, s_id):
        headers = {
            'x-api-key': self.x_api_key,
            "Content-Type": "application/json",
        }

        data = {
            'sourceId': s_id,
            'messages': [
                {
                    'role': "user",
                    'content': "What is this theis's title? and Who wrote this theis? and What is acknoledgements of this theis? if has nothing tell me nothing"
                }
            ]
        }

        response = requests.post(
            'https://api.chatpdf.com/v1/chats/message', headers=headers, json=data)

        if response.status_code == 200:
            print('Result:', response.json()['content'])
            return response.json()['content']
            
        else:
            print('Status:', response.status_code)
            print('Error:', response.text)
            
    def extract_result(self, text):
        # 패턴을 기준으로 문장 분리
        split_pattern = ["The title of this thesis is ", "The author of this thesis is ", "The acknowledgements of this thesis are "]
        for pattern in split_pattern:
            text = text.replace(pattern, "")

        # '.'을 기준으로 문장 분리
        split_text = text.split('.')

        # 리스트에서 공백 제거
        result = [s.strip() for s in split_text if s]
        result = [None if i == 'not mentioned in the provided pages' else i for i in result]
        return result
        # 결과 출력
        # for r in result:
        #     print(f"\"{r}\"")               
