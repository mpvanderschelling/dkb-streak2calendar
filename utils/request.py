import requests
import json


def getPipelineData():
    
    with open('./streak_keys/streak_pipelinekey.txt') as f:
        pipelineKey = f.read().rstrip()
    
    with open('./streak_keys/streak_apikey.txt') as g:
        apiKey = g.read().rstrip()
    
    url = f"https://www.streak.com/api/v1/pipelines/{pipelineKey}/boxes"
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Basic {apiKey}"
    }
    
    response = requests.request("GET", url, headers=headers)
    
    
    return json.loads(response.text)



if __name__ == '__main__':
    pass
