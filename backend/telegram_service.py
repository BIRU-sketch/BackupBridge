from pyrogram import Client

api_id = ''
api_hash ='' 


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
                    message=input("Enter your message: ")
                    self.send_message(selected_chat.id,message)
                elif choice=="2":
                    self.fetch_messages(selected_chat.id)
                elif choice=="3":
                    self.app.stop()
                    return
                else:
                    print("Invalid choice")
if __name__ == "__main__":
    app = App(api_id, api_hash)
    app.main()