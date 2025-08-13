import requests
response=requests.post("http://localhost:5000/get_chats", json={"name": "biruk"})
response=requests.get("http://localhost:5000/get_chats")
print(response.text)

