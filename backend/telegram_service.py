from pyrogram import Client
from firestore_client import database
from flask import Flask,jsonify,request
import asyncio, os
from dotenv import load_dotenv
from telethon import TelegramClient,functions
load_dotenv(".env.local")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
app=Flask(__name__)
pyr_app = Client('my_account', api_id=API_ID, api_hash=API_HASH)


db = database()

class PyrogramFunctions:
    def __init__(self):
        self.app = pyr_app
    def block_user(self, user_id):
        try:
            self.app.start()
            self.app.block_user(user_id)
        finally:
            self.app.stop()
            return f"User {user_id} blocked successfully"
    
    def monitor_sessions(self, name):
        name = name.lower()
        session_dic = {}
        telethon_client = TelegramClient('telethon_session', API_ID, API_HASH)
        async def update_sessions():
            try:
                await telethon_client.start()
                result = await telethon_client(functions.account.GetAuthorizationsRequest())
                session_dic[name] = []
                for session in result.authorizations:
                    session_dic[name].append({
                        "Device": session.device_model,
                        "App": session.app_name,
                        "ID": session.hash
                        })
                    db.add("Sessions", name, {"sessions": session_dic[name]})
            finally:
                await telethon_client.disconnect()
        asyncio.run(update_sessions())

    def get_sessions(self,name):
        name=name.lower()
        existing_sessions = db.get("Sessions", name)
        if existing_sessions.to_dict() is None:
            print("Updating database!")
            self.monitor_sessions(name)
            return "Sessions updated successfully"
        else:
            return {"Sessions": existing_sessions.to_dict()}
    def terminate_session(self, name, session_id):
        telethon_client = TelegramClient('telethon_session', API_ID, API_HASH)
        async def terminate():
            try:
                await telethon_client.start()
                await telethon_client(functions.account.ResetAuthorizationRequest(session_id))
            finally:
                await telethon_client.disconnect()
        asyncio.run(terminate())
    def update_chats(self, name):
        name = name.lower()
        existing_chats = db.get('Chats',name)
        chats={}
        try:
            self.app.start()
            chats[name]=[
                {
                    "id":chat.chat.id,
                    "name":chat.chat.title or chat.chat.first_name or chat.chat.last_name
                }for chat in self.app.get_dialogs()
            ]
            db.add("Chats",name,{"chats":chats})
        finally:
            self.app.stop()
        return "Chats retrieved successfully"
    def get_chats(self,name):
        name=name.lower()
        exising_chats=db.get('Chats',name)
        if exising_chats.to_dict() is None:
            print("Updating database!")
            return self.update_chats(name)
        else:
            return exising_chats.to_dict()
account = PyrogramFunctions()
print(account.get_chats("bi"))