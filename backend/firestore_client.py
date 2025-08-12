import firebase_admin
from firebase_admin import credentials, firestore
firebase_admin.initialize_app(credentials.Certificate('BackupBridge.json'))
class database():
    def __init__(self):
        self.db = firestore.client()
    def get(self, collection, doc):
        return self.db.collection(collection).document(doc).get()
    def get_all(self,collection):
        return self.db.collection(collection).get()
    def add(self, collection, doc, data):
        self.db.collection(collection).document(doc).set(data)
    def delete(self, collection, doc):
        self.db.collection(collection).document(doc).delete()
    def delete_all(self,collection):
        data=self.db.collection(collection).get()
        for doc in data:
            self.db.collection(collection).document(doc.id).delete()
    def update(self, collection, doc, data):
        self.db.collection(collection).document(doc).update(data)
    