import requests
import json


class StreakAPI:
    def __init__(self, PIPELINEKEY='agxzfm1haWxmb29nYWVyPgsSDE9yZ2FuaXphdGlvbiIXZGVrbGl0dGVuYmFuZEBnbWFpbC5jb20MCxIIV29ya2Zsb3cYgIDKl7bc5wsM',
                 APIKEYLOC='./streak_keys/streak_apikey.txt',):
        
        self.pipelineKey = PIPELINEKEY
        self.url = f"https://www.streak.com/api/v1/pipelines/{PIPELINEKEY}/boxes"
        
        with open('./streak_keys/streak_apikey.txt') as g:
            self.apiKey = g.read().rstrip()
            
            
        self.headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Basic {self.apiKey}"
            }
        
    def getPipelineData(self):
        response = requests.request("GET", self.url, headers=self.headers)
        return json.loads(response.text)        



if __name__ == '__main__':
    pass
