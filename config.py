import os
from pymongo import MongoClient
import time
import threading

mongo_client = MongoClient(os.environ['database'])


pasyuk_id = 441399484
senderman_id = 94197300
admins = (pasyuk_id, senderman_id)


def creategroup(m, bot):
    return {
        'title':m.chat.title,
        'username':m.chat.username,
        'description':bot.get_chat(m.chat.id).description
    
           }

def aboutt(m, bot):
    return

def about(m, bot):
    return
    
    
    
