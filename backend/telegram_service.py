from pyrogram import Client
from dotenv import load_dotenv
from telethon import TelegramClient,functions
import os
from flask_cors import CORS
from flask import Flask, request, jsonify
app=Flask(__name__)
CORS(app)
array={}
load_dotenv('.env.local')
api_id=''
api_hash=''
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')
class App():
    def __init__(self, api_id, api_hash):
        self.app = Client("my_account", api_id=api_id, api_hash=api_hash)
    def list_chats(self):
        print("Fetching chats...")
        chats=[]
        for i,dialog in enumerate(self.app.get_dialogs(),1):
            chat=dialog.chat
            chat_name=chat.first_name or chat.title or  "Unknown"
            print(f"{i}. {chat_name} (ID: {chat.id})")
            chats.append(chat)
        return chats
    def fetch_messages(self, chat_id, limit=10):
        for message in self.app.get_chat_history(chat_id, limit=limit):
            print(f"{message.from_user.first_name}: {message.text}")
    def send_message(self, chat_id, text):
        self.app.send_message(chat_id, text)
    def main(self):
        self.app.start()
        chats=self.list_chats()
        choice=input("Enter chat number you want to interact with: ")
        if choice.isdigit():
            if int(choice)<1 or int(choice)>len(chats):
                print("Invalid choice")
                self.app.stop()
                return
            selected_chat=chats[int(choice)-1]
            while True:
                print("\nOptions")
                print("1.Send Message")
                print("2.Fetch messages")
                print("3.Exit ")
                choice=input("Enter your choice: ")
                if choice=="1":
                    cls()
                    message=input("Enter your message: ")
                    self.send_message(selected_chat.id,message)
                elif choice=="2":
                    cls()
                    self.fetch_messages(selected_chat.id)
                elif choice=="3":
                    cls()
                    self.app.stop()
                    return
                else:
                    print("Invalid choice")
    def sessions(self,choice):
        if choice == "1":
            client=TelegramClient('telethon_session',api_id,api_hash)
            async def monitor_sessions():
                sessions=await client(functions.account.GetAuthorizationsRequest())
                cls()
                for i,session in enumerate(sessions.authorizations,1):
                    print(f"{i}. {session.device_model} -{session.app_name} ID:({session.hash})")
                    stuff={
                        f"{i}":{
                            "device_model": session.device_model, "app_name": session.app_name, "hash": session.hash
                            }
                    }
                    array[f"{i}"]=stuff

            with client:
                client.loop.run_until_complete(monitor_sessions())
        
if __name__=="__main__":
    account=App(api_id,api_hash)
    @app.route('/')
    def Welcome():
        return jsonify({"message":"Welcome to Telegram Backup Service! Please use the following commands for specific services: \n 1. /monitor_sessions-To monitor and terminate active sessions \n 2./chat - to just chat"})
    @app.route('/api/monitor_sessions', methods=['GET'])
    def monitor_sessions():
        account.sessions("1")
        responce={}
        return jsonify({"message": array})
    app.run(debug=True,host='0.0.0.0',port=3558)