import requests

if __name__ == '__main__':
    resp = requests.get('http://127.0.0.1:80/building/')
    data = resp.json()['data']
    refresh = [requests.delete(f'http://127.0.0.1:80/building/{item["_id"]}') for item in data]
    resp = requests.get('http://127.0.0.1:80/building/')
    data = resp.json()['data']
    print(data)
