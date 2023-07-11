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
        else:
            print('Status:', response.status_code)
            print('Error:', response.text)

pdfapi = PdfApi()
s_id = pdfapi.add_adf_via_url('./thesis/thesis1.pdf')
pdfapi.ask_of_pdf(s_id)