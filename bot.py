# -*- coding: utf-8 -*-
import os
import telebot
import time
import random
from telebot import types
from pymongo import MongoClient
import threading
import traceback
import requests
import config



client1=os.environ['database']
client=MongoClient(client1)
db=client.chlenomer
idgroup=db.ids
iduser=db.ids_people
users = db.ids_people
penis=db.penis
pics=db.pics
if pics.find_one({})==None:
    pics.insert_one({'pics':[]})

numb = db.numb
if numb.find_one({}) == None:
    numb.insert_one({'numb':0})
    
wait_chats = db.wait_chats

#wait_chats.remove({})

if wait_chats.find_one({}) == None:
    wait_chats.insert_one({'chats':[]})

actives = db.actives
if actives.find_one({}) == None:
    actives.insert_one({'actives':[]})

ban=[667532060, -1001267248577]
timerr=0

waitgroup = []

wait=[]
ch=[]
members=[]
play=[]


msgcount=0
pods4et=0


token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)
writed=[
]
massive=['Хер','хер','Член','член','Хуй','хуй']
elita=[]

@bot.message_handler(commands=['combine'])
def combine(m):
    config.about(m, bot)
    if m.from_user.id==441399484:
        try:
            x1=int(m.text.split(' ')[1])
            x2=int(m.text.split(' ')[2])
            iduser.update_one({'id':x2},{'$inc':{'summ':iduser.find_one({'id':x1})['summ']}})
            iduser.update_one({'id':x2},{'$inc':{'kolvo':iduser.find_one({'id':x1})['kolvo']}})
            bot.send_message(x2, 'Перенёс данные со старого аккаунта на новый!')
            bot.send_message(441399484, 'gotovo')
        except:
            bot.send_message(441399484, traceback.format_exc())

            
@bot.message_handler(commands=['getgroup'])
def getgroupp(m):
    config.about(m, bot)
    if m.from_user.id != 441399484:
        return
    bot.send_message(m.chat.id, 'Начат поиск!') 
    try:
        id = int(m.text.split()[1])
        for ids in idgroup.find({}):
            for idss in ids['topdaily']:
                try:
                    if idss == id:
                        bot.send_message(m.chat.id, 'Юзер найден в группе! Ожидаем сообщения оттуда...')
                        waitgroup.append({'group':ids['id'], 'user':id})
                except:
                    try:
                        bot.send_message(m.chat.id, ids['topdaily'])
                    except:
                        pass
    except:
        bot.send_message(m.chat.id, 'error!!!')
        bot.send_message(441399484, traceback.format_exc())

@bot.message_handler(content_types=['photo'], func = lambda m: m.chat.id != 441399484)
def imggfdgfg(m):
    config.about(m, bot)
    x = iduser.find_one({'id':m.from_user.id})
    if x == None:
        return
    if m.chat.id == 441399484:
        try:
            pic = x['pic']
            iduser.update_one({'id':x['id']},{'$set':{'pic':m.photo[0].file_id}})

            bot.send_photo(m.chat.id, iduser.find_one({'id':m.from_user.id})['pic'])
        except:
            iduser.update_one({'id':x['id']},{'$set':{'pic':m.photo[0].file_id}})
            bot.send_photo(m.chat.id, iduser.find_one({'id':m.from_user.id})['pic'])
            
           
@bot.message_handler(content_types = ['animations'])
@bot.message_handler(content_types = ['document'])
def animm(m):
    config.about(m, bot)
    if m.from_user.id != 441399484:
        return
    if m.chat.id != m.from_user.id:
        return
    user = users.find_one({'id':m.from_user.id})
    if 'gif' not in user:
        users.update_one({'id':user['id']},{'$set':{'gif':None}})
        user = users.find_one({'id':m.from_user.id})
    users.update_one({'id':user['id']},{'$set':{'gif':m.document.file_id}})
    bot.send_document(m.chat.id, m.document.file_id)
        
@bot.message_handler(commands=['add'])
def adddsfdgeh(m):
    config.about(m, bot)
    if m.from_user.id==441399484:
        try:
            id=int(m.text.split(' ')[1])
            iduser.update_one({'id':id},{'$inc':{'chlenocoins':int(m.text.split(' ')[2])}})
            bot.send_message(m.chat.id, 'Членокоины добавлены!')
        except:
            bot.send_message(441399484, traceback.format_exc())
            
       
@bot.message_handler(func = lambda m: m.text !=None and m.text[:15] == '/add_url_button')
def addbutt(m):
    config.about(m, bot)
    print('1')
    if m.from_user.id != 441399484:
        return
    user = users.find_one({'id':m.from_user.id})
    if 'url_buttons' not in user:
        users.update_one({'id':user['id']},{'$set':{'url_buttons':[]}})
        user = users.find_one({'id':m.from_user.id})
    try:
        print('2')
        text = m.text.split('#^')[1]
        url = m.text.split('#^')[2]
    except:
        bot.send_message(m.chat.id, 'Error')
        return
    users.update_one({'id':user['id']},{'$push':{'url_buttons':[text, url]}})
    print('3')
    bot.send_message(m.chat.id, text+' ('+url+')')
    
    
@bot.message_handler(func = lambda m: m.text !=None and m.text[:14] == '/test_send_url')
def sendurl(m):
  config.about(m, bot)
  try:
    if m.from_user.id != 441399484:
        return
    user = users.find_one({'id':m.from_user.id})
    kb = types.InlineKeyboardMarkup()
    for ids in user['url_buttons']:
        kb.add(types.InlineKeyboardButton(text = ids[0], url = ids[1]))
    try:
        if user['gif'] == None:
            bot.send_message(m.chat.id, m.text.split('#^')[1], parse_mode = 'markdown', reply_markup = kb)
        else:
            bot.send_document(m.chat.id, user['gif'], caption = m.text.split('#^')[1], parse_mode = 'markdown', reply_markup = kb)
    except:
        
        bot.send_message(m.chat.id, m.text.split('#^')[1], parse_mode = 'markdown', reply_markup = kb)
  except:
    bot.send_message(m.chat.id,'Error')
    
    
@bot.message_handler(func = lambda m: m.text !=None and m.text[:8] == '/add_url')
def addbutt(m):
    config.about(m, bot)
    print('1')
    if m.from_user.id != 441399484:
        return
    user = users.find_one({'id':m.from_user.id})
    if 'url' not in user:
        users.update_one({'id':user['id']},{'$set':{'url':None}})
        user = users.find_one({'id':m.from_user.id})
    try:
        print('2')
        url = m.text.split('#^')[1]
    except:
        bot.send_message(m.chat.id, 'Error')
        return
    users.update_one({'id':user['id']},{'$set':{'url':url}})
    print('3')
    bot.send_message(m.chat.id, '('+url+')')
    
@bot.message_handler(func = lambda m: m.text !=None and m.text[:14] == '/test_send_img')
def sendurlimg(m):
  config.about(m, bot)
  try:
    if m.from_user.id != 441399484:
        return
    user = users.find_one({'id':m.from_user.id})
    kb = types.InlineKeyboardMarkup()
    for ids in user['url_buttons']:
        kb.add(types.InlineKeyboardButton(text = ids[0], url = ids[1]))
    url = user['url']
    msg = '<a href = "{}">&#8204;</a>'.format(url)+m.text.split('#^')[1]
    try:

            bot.send_message(m.chat.id, msg, parse_mode = 'html', reply_markup = kb)
    except:
        
        bot.send_message(m.chat.id, msg, parse_mode = 'html', reply_markup = kb)
  except:
    bot.send_message(m.chat.id,'Error')
    
@bot.message_handler(func = lambda m: m.text !=None and m.text[:9] == '/send_img')
def sendurlimg(m):
  config.about(m, bot)
  try:
    if m.from_user.id != 441399484:
        return
    user = users.find_one({'id':m.from_user.id})
    kb = types.InlineKeyboardMarkup()
    for ids in user['url_buttons']:
        kb.add(types.InlineKeyboardButton(text = ids[0], url = ids[1]))
    url = user['url']
    msg = '<a href = "{}">&#8204;</a>'.format(url)+m.text.split('#^')[1]
    i = 0
    for ids in iduser.find({}):
        try:

            bot.send_message(ids['id'], msg, parse_mode = 'html', reply_markup = kb)
            i+=1
        except:
            pass
    bot.send_message(m.chat.id, '#рассылка получили сообщение '+str(i)+' юзеров!')
  except:
    bot.send_message(m.chat.id,traceback.format_exc())
    bot.send_message(m.chat.id, str(i))
    
@bot.message_handler(commands=['rbt'])
def rbtghk(m):
    config.about(m, bot)
    if m.from_user.id != 441399484:
        return
    numb.update_one({},{'$set':{'numb':0}})
    bot.send_message(m.chat.id, 'Ez')



@bot.message_handler(commands=['amount'])
def amfmmffm(m):
    config.about(m, bot)
    if m.from_user.id != 441399484:
        return
    bot.send_message(m.chat.id, str(len(actives.find_one({})['actives'])))

@bot.message_handler(func = lambda m: m.text !=None and m.text[:10] == '/send_test')
def sendurlimg(m):
  config.about(m, bot)
  try:
    
    if m.from_user.id != 441399484:
        return
    user = users.find_one({'id':m.from_user.id})
    kb = types.InlineKeyboardMarkup()
    i = numb.find_one({})['numb']
    iuf = 11501264660
    acts = actives.find_one({})
    
    while i < iuf:
        try:
            user = iduser.find_one({'id':i})
            if user != None:
                msg = bot.send_message(i, 'Служебное сообщение, оно будет удалено.')
                bot.delete_message(i, msg.message_id)
                if i not in acts:
                    actives.update_one({},{'$push':{'actives':i}})
            
            
            
            
        except:
            pass

        if i%100000 == 0:
            bot.send_message(441399484, str(i))
            numb.update_one({},{'$set':{'numb':i}})
        i+=1

    bot.send_message(m.chat.id, '#рассылка я проверил '+str(i)+' юзеров!')
  except:
    bot.send_message(m.chat.id,traceback.format_exc())
    bot.send_message(m.chat.id, str(i))
    
    
@bot.message_handler(func = lambda m: m.text !=None and m.text[:9] == '/send_url')
def sendurl(m):
  config.about(m, bot)
  try:
    if m.from_user.id != 441399484:
        return
    user = users.find_one({'id':m.from_user.id})
    kb = types.InlineKeyboardMarkup()
    for ids in user['url_buttons']:
        kb.add(types.InlineKeyboardButton(text = ids[0], url = ids[1]))
    i = 0
    if user['gif'] == None:
        for ids in idgroup.find({}):
            try:
                bot.send_message(ids['id'], m.text.split('#^')[1], parse_mode = 'markdown', reply_markup = kb)
                i+=1
            except:
                pass
        bot.send_message(m.chat.id, '#рассылка получили сообщение '+str(i)+' чатов!')
    else:
        for ids in idgroup.find({}):
            try:
                bot.send_document(ids['id'], user['gif'], caption = m.text.split('#^')[1], parse_mode = 'markdown', reply_markup = kb)
                i+=1
            except:
                pass
        bot.send_message(m.chat.id, '#рассылка получили сообщение '+str(i)+' чатов!')

  except:
    bot.send_message(m.chat.id, traceback.format_exc())
    
    
    
@bot.message_handler(commands=['clear_url_button'])
def addbutt(m):
    config.about(m, bot)
    if m.from_user.id != 441399484:
        return
    user = users.find_one({'id':m.from_user.id})
    if 'url_buttons' not in user:
        users.update_one({'id':user['id']},{'$set':{'url_buttons':[]}})
        user = users.find_one({'id':m.from_user.id})
    
    users.update_one({'id':user['id']},{'$set':{'url_buttons':[]}})
    bot.send_message(m.chat.id, 'cleared')
    


@bot.message_handler(content_types = ['photo'])
def sendpic(m):
    config.about(m, bot)
    x = iduser.find_one({'id':m.from_user.id})
    if x != None:
        if m.chat.id != m.from_user.id:
            return
        if x['id'] == 441399484:
            try:
                pic = x['pic']
                iduser.update_one({'id':x['id']},{'$set':{'pic':m.photo[0].file_id}})

                bot.send_photo(m.chat.id, iduser.find_one({'id':m.from_user.id})['pic'])
            except:
                iduser.update_one({'id':x['id']},{'$set':{'pic':m.photo[0].file_id}})
                bot.send_photo(m.chat.id, iduser.find_one({'id':m.from_user.id})['pic'])
            
            
@bot.message_handler(commands=['curpic'])
def cpiccc(m):
    config.about(m, bot)
    x = iduser.find_one({'id':m.from_user.id})
    if x != None:
        if x['id'] == 441399484:
            try:
                pic = x['pic']
                bot.send_photo(m.chat.id, pic)
            except:
                pass
            
@bot.message_handler(commands=['sendpic'])
def sendpiiic(m):
    config.about(m, bot)
    if m.from_user.id == 441399484:
      try:
        param = m.text.split(' ')[1]
        if param == 'users':
            x = iduser.find({})
        elif param == 'groups':
            x = idgroup.find({})
        a = iduser.find_one({'id':m.from_user.id})
        ph = a['pic']
        capti = m.text.split('/sendpic '+param+' ')[1]
        
        y=iduser.find({})
        usend=0
        gsend=0
        for one in x:
            try:
              bot.send_photo(one['id'], ph, caption = capti)
              gsend+=1
            except:
                pass
      #  for one in y:
      #      try:
     #         bot.send_photo(one['id'], ph, caption = capti)
      #        usend+=1
     #       except:
     #           pass
        bot.send_message(441399484,
                         'Отправлено сообщений '+param+': '+str(gsend))
      except:
        bot.send_message(441399484, traceback.format_exc())
            
            
@bot.message_handler(commands=['update'])
def upddd(m):
    config.about(m, bot)
    if m.from_user.id==441399484:
        iduser.update_many({}, {'$set':{'msgcount':0, 'penisincs':0}})
        bot.send_message(m.chat.id, 'updated')

@bot.message_handler(commands=['count'])
def counttt(m):
    config.about(m, bot)
    if m.from_user.id==441399484:
        global pods4et
        pods4et=1
        t=threading.Timer(60, ends4et, args=[m.chat.id])
        t.start()
        bot.send_message(m.chat.id, 'Считаю количество сообщений за минуту.')
        
def ends4et(id):
    global msgcount
    global pods4et
    bot.send_message(id, 'Количество сообщений за минуту: '+str(msgcount)+'.')
    msgcount=0
    pods4et=0
    
    

@bot.message_handler(commands=['globalchlen'])
def globalpeniss(m):
    config.about(m, bot)
    if m.from_user.id not in ban:
        incmsg(m.from_user.id, m.chat.id, m.message_id)
        penis.update_one({},{'$inc':{'penis':0.1}})
        iduser.update_one({'id':m.from_user.id},{'$inc':{'penisincs':0.1}})
        p=penis.find_one({})
        ps=p['penis']
        try:
          bot.send_message(m.chat.id, 'Вы увеличили мой член на 0.1 см! Текущая длина: '+str(round(ps,2))+' см!')
        except:
          pass


@bot.message_handler(commands=['id'])
def iddd(m):
 config.about(m, bot)
 try:
  if m.from_user.id not in ban:
    incmsg(m.from_user.id, m.chat.id, m.message_id)
    if m.reply_to_message!=None:
        user=m.reply_to_message.from_user
        bot.send_message(m.chat.id, 'id выбранного пользователя:\n'+'`'+str(user.id)+'`',reply_to_message_id=m.message_id,parse_mode='markdown')
    else:
        bot.send_message(m.chat.id, 'Чтобы узнать id пользователя, введите эту команду, ответив на его сообщение.')

 except:
  pass


@bot.message_handler(commands=['chatid'])
def chatid(m):
 config.about(m, bot)
 try:
  if m.from_user.id not in ban:
    incmsg(m.from_user.id, m.chat.id, m.message_id)
    bot.send_message(m.chat.id, 'Айди чата: `'+str(m.chat.id)+'`', parse_mode='markdown')
 except:
  pass
    
        
@bot.message_handler(commands=['donate'])
def donatemes(m):
 config.about(m, bot)
 return
 try:
  if m.from_user.id not in ban:
    incmsg(m.from_user.id, m.chat.id, m.message_id)
    bot.send_message(m.chat.id, ' вам нравится бот и вы хоти)', parse_mode='markdown')
 except:
  pass



@bot.message_handler(commands=['removedailyuser'])
def removedailyu(m): 
 config.about(m, bot)
 try:
  if m.from_user.id not in ban:
    incmsg(m.from_user.id, m.chat.id, m.message_id)
    pass
    x=bot.get_chat_member(m.chat.id, m.from_user.id)
    if 'administrator' in x.status or 'creator' in x.status or m.from_user.id==441399484:
            chat=idgroup.find_one({'id':m.chat.id})
            try:
                if len(m.text.split(' '))==2:
                    user=chat['topdaily'][m.text.split(' ')[1]]
                    if user['id']!=441399484:
                        idgroup.update_one({'id':chat['id']},{'$set':{'topdaily.'+str(user['id']):{'name':user['name']}}})
                        bot.send_message(m.chat.id, 'Юзер был успешно удалён из списка!')
                    else:
                        bot.send_message(m.chat.id, 'Вы не можете удалить администратора бота из списка!')
                else:
                    bot.send_message(m.chat.id, 'Чтобы удалить юзера из ежедневного розыгрыша, введите эту команду в таком формате:\n'+
                                     '/removedailyuser *USERID*, где *USERID* - айди участника, которого вы хотите удалить. Взять его можно '+
                                     'по команде /id.\n\nВНИМАНИЕ!!!\nУдалив участника из списка, вы сбросите его чатовую статистику ежедневных '+
                                     'розыгрышей!',parse_mode='markdown')
            except:
                bot.send_message(m.chat.id, 'Юзер с таким id не регистрировался в этом чате!')
               
    else:
        bot.send_message(m.chat.id, 'Вы не админ чата!')
    
 except:
  pass


    
    
@bot.message_handler(commands=['sendm'])
def sendmes(message):
    m=message
    config.about(m, bot)
    if message.from_user.id==441399484:
        x=idgroup.find({})
        y=iduser.find({})
        tex=message.text.split('/sendm')
        usend=0
        gsend=0
        for one in x:
            try:
              bot.send_message(one['id'], tex[1])
              gsend+=1
            except:
                pass
        for one in y:
            try:
              bot.send_message(one['id'], tex[1])
              usend+=1
            except:
                pass
        bot.send_message(441399484, 'Отправлено сообщений юзерам: '+str(usend)+'\n'+
                         'Отправлено сообщений группам: '+str(gsend))
        
        
        
@bot.message_handler(commands=['sendp'])
def sendmesssss(message):
    m=message
    config.about(m, bot)
    if message.from_user.id==441399484:
        y=iduser.find({})
        tex=message.text.split('/sendm')
        usend=0
        for one in y:
            try:
              bot.send_message(one['id'], tex[1])
              usend+=1
            except:
                pass
        bot.send_message(441399484, 'Отправлено сообщений юзерам: '+str(usend))

    
#@bot.message_handler(commands=['update'])
#def upd(m):
#  if m.from_user.id==441399484:
#         try:
#            idgroup.update_many({}, {'$set':{
#                                            
#                                             
#          
#                                            }
#                                    }
#                                )
 #           print('yes')
    #     except:
      #      pass
            
@bot.message_handler(commands=['stoyak'])
def biggest(m):
 config.about(m, bot)
 try:
  if m.from_user.id not in ban:
    incmsg(m.from_user.id, m.chat.id, m.message_id)
    if m.from_user.id!=m.chat.id:
        x=idgroup.find_one({'id':m.chat.id})
        if x!=None:
          if x['dailyroll']==1:
            nmb=0
            for zz in x['topdaily']:
              nmb+=1
            if nmb>0:
              x['dailyroll']=0
              idgroup.update_one({'id':m.chat.id},{'$set':{'dailyroll':0}})
              bot.send_message(m.chat.id, 'Начинаю поиск по базе данных...')
              t=threading.Timer(2, turn2, args=[m.chat.id])
              t.start()
            else:
              bot.send_message(m.chat.id, 'Нет ни одного зарегистрированного пользователя! Нажмите /dailychlenreg для того, '+
                             'чтобы я добавил вас в список.')
          else:
            bot.send_message(m.chat.id, 'Сегодня уже был проведён розыгрыш! Со стояком был замечен:\n\n'+x['todaywinner']+'!')
        else:
            bot.send_message(m.chat.id, 'Сначала напишите в группу что-нибудь!')
        
 except:
  pass


def turn2(id):
 try:
    bot.send_message(id, 'Сканирую каждый член, не двигайтесь...')
    t=threading.Timer(2, turn3, args=[id])
    t.start()
 except:
  pass
    
def turn3(id):
 try:
    x=idgroup.find_one({'id':id})
    lst=[]
    for ids in x['topdaily']:
        try:
            lst.append(x['topdaily'][ids]['id'])
        except:
            pass
    if len(lst)>0:
        y=random.choice(lst)
        name=x['topdaily'][str(y)]['name']
        try:
            username=x['topdaily'][str(y)]['username']
            if username==None:
                username='None'
        except:
            username='None'
        idgroup.update_one({'id':id},{'$inc':{'topdaily.'+str(y)+'.dailywins':1}})
        idgroup.update_one({'id':id},{'$inc':{'topdaily.'+str(y)+'.currentwinstreak':1}})
        x=idgroup.find_one({'id':id})
        if x['topdaily'][str(y)]['maxwinstreak']<x['topdaily'][str(y)]['currentwinstreak']:
            idgroup.update_one({'id':id},{'$set':{'topdaily.'+str(y)+'.maxwinstreak':x['topdaily'][str(y)]['currentwinstreak']}})
        idgroup.update_one({'id':id},{'$set':{'todaywinner':name}})
        for ids in x['topdaily']:
          try:
            if x['topdaily'][ids]['id']!=y:
                idgroup.update_one({'id':id},{'$set':{'topdaily.'+str(x['topdaily'][ids]['id'])+'.currentwinstreak':0}})
          except:
            pass
        bot.send_message(id, 'Измерения успешно проведены. В данный момент стояк можно наблюдать у пользователя:\n\n'+name+' (@'+username+')!')
    else:
        bot.send_message(id, 'В этой группе на ежедневный розыгрыш не зарегистрировано ни одного пользователя!')
 except:
  pass
    
    
@bot.message_handler(commands=['topchlens'])
def topchlen(m):
 config.about(m, bot)
 try:
  if m.from_user.id not in ban:
    incmsg(m.from_user.id, m.chat.id, m.message_id)
    x=idgroup.find_one({'id':m.chat.id})
    if x!=None:
        text=''
        z=1
        winlist=[]
        while z<11:
            winid=0
            maxnumber=-1
            da=0
            for ids in x['topdaily']:
                try:
                    if x['topdaily'][ids]['dailywins']>maxnumber and x['topdaily'][ids]['id'] not in winlist:
                        da=1
                        winid=x['topdaily'][ids]['id']
                        maxnumber=x['topdaily'][ids]['dailywins']
                except:
                    pass
            if da==1:
                winlist.append(winid)
                text+=str(z)+'. '+x['topdaily'][str(winid)]['name']+': '+str(x['topdaily'][str(winid)]['dailywins'])+'\n'
            z+=1
        if text=='':
            text='В этой группе не было проведено ни одного розыгрыша!'
        bot.send_message(m.chat.id, 'Топ-10 пользователей, чей член больше всего раз был замечен в стоячем состоянии:\n\n'+text)

        bot.send_message(441399484, 'Топ-10 пользователей, чей член больше всего раз был замечен в стоячем состоянии:\n\n'+text)

 except:
  pass                
                
                        
                       
    
@bot.message_handler(commands=['dailychlenreg'])
def dailyr(m):
 config.about(m, bot)
 try:
  if m.from_user.id not in ban:
    incmsg(m.from_user.id, m.chat.id, m.message_id)
    if m.from_user.id!=m.chat.id:
        x=idgroup.find_one({'id':m.chat.id})
        if x!=None:
         p=0
         for ids in x['topdaily']:
            try:
                if x['topdaily'][ids]['id']==m.from_user.id:
                    p=1
            except:
                pass
         if p==0:
            idgroup.update_one({'id':m.chat.id},{'$set':{'topdaily.'+str(m.from_user.id):createdailyuser(m.from_user.id, m.from_user.first_name,m.from_user.username)}})
            bot.send_message(m.chat.id, 'Вы успешно зарегистрировались!')
         else:
            bot.send_message(m.chat.id, 'Ты уже в игре!')
        else:
            bot.send_message(m.chat.id, "Сначала напишите в чат что-нибудь!")
    else:
        bot.send_message(m.chat.id, 'Можно регистрироваться только в группах!')

 except:
  pass


@bot.message_handler(commands=['usecoins'])
def usecoins(m):
 config.about(m, bot)
 try:
  if m.from_user.id not in ban:
    incmsg(m.from_user.id, m.chat.id, m.message_id)
    bot.send_message(m.chat.id, '@petwarbot - тут можно подраться своим питомцем.')
 except:
  pass
    
@bot.message_handler(commands=['mysize'])
def size(m):
 config.about(m, bot)
 try:
  if m.from_user.id not in ban:
    incmsg(m.from_user.id, m.chat.id, m.message_id)
    x=iduser.find_one({'id':m.from_user.id})
    try:
        sredn=x['summ']/x['kolvo']
        sredn=round(sredn, 2)
    except:
        sredn=0
    try:
        bot.send_message(m.chat.id, m.from_user.first_name+', средний размер вашего члена: '+str(sredn)+' см.\nВы измеряли член '+str(x['kolvo'])+' раз(а)!') 
        bot.send_message(441399484, m.from_user.first_name+', средний размер вашего члена: '+str(sredn)+' см.\nВы измеряли член '+str(x['kolvo'])+' раз(а)!')
    except:
        bot.send_message(m.chat.id, 'Измерьте член хотя бы 1 раз!')
 except:
  pass                        
    
    
@bot.message_handler(commands=['me'])
def mme(m):
 config.about(m, bot)
 try:
  if m.text.lower()=='/me' or m.text.lower()=='/me@chlenomerbot':
    if m.from_user.id not in ban:
      incmsg(m.from_user.id, m.chat.id, m.message_id)
      x=iduser.find_one({'id': m.from_user.id})
      try:
       bot.send_message(m.chat.id, m.from_user.first_name+', Ваши членокоины: '+str(x['chlenocoins'])+'. За 5 вы можете купить питомца! (Команда /buypet).')
       bot.send_message(441399484, m.from_user.first_name+', Ваши членокоины: '+str(x['chlenocoins'])+'. Сейчас они не нужны, но следите за обновлениями - в будущем они понадобятся!')                                                                                                                                     
      except:
          bot.send_message(m.chat.id, 'Упс! Какая-то ошибка! Наверное, вы ни разу не измеряли член! (напишите боту "член")')
          bot.send_message(441399484, 'Упс! Какая-то ошибка! Наверное, вы ни рару не измеряли член!')                                                                                                                               
 except:
  pass                                                                

                
@bot.message_handler(commands=['channel'])
def channel(message):
 try:
  m=message
  config.about(m, bot)
  if message.from_user.id not in ban:
    incmsg(message.from_user.id, message.chat.id, message.message_id)
    bot.send_message(message.chat.id, 'Канал обновлений: @chlenomer')
 except:
  pass                   

@bot.message_handler(commands=['start'])
def startms(message):
 try:
  m=message
  config.about(m, bot)
  if m.text.lower()=='/start' or m.text.lower()=='/start@chlenomerbot':
    if message.from_user.id not in ban:
      incmsg(message.from_user.id, message.chat.id, message.message_id)
      if message.from_user.id==message.chat.id:
        bot.send_message(message.from_user.id, 'Если ты здесь, то ты наверняка хочешь измерить член! Пиши /commands, чтобы узнать, на какие слова реагирует бот')
 except:
  pass

@bot.message_handler(commands=['info'])
def info(message):
    m=message
    config.about(m, bot)
    if message.from_user.id==441399484:
      try:
        group=0
        people=0
        x=idgroup.find({})
        for element in x:
            group+=1
        y=iduser.find({})
        for element in y:
            people+=1
        bot.send_message(message.from_user.id, 'Группы: '+str(group)+'\n'+'Люди: '+str(people))
      except:
        bot.send_message(441399484, traceback.format_exc())
        bot.send_message(m.chat.id, str(group)+' groups\n'+str(people)+' users')


   
@bot.message_handler(commands=['ti_ctochlen'])
def ticto(message):
 try:
  m=message
  config.about(m, bot)
  if message.from_user.id not in ban:
    incmsg(message.from_user.id, message.chat.id, message.message_id)
    bot.send_message(message.chat.id, 'Умеет менять размер члинуса')
 except:
  pass                     
        
@bot.message_handler(commands=['name'])
def name(m):
 config.about(m, bot)
 try:
  if m.text.lower()=='/name' or m.text.lower()=='/name@chlenomerbot':
      if m.from_user.id not in ban:
        incmsg(m.from_user.id, m.chat.id, m.message_id)
        player=iduser.find_one({'id':m.from_user.id})
        if player!=None:
            x=m.text.split('/name ')
            if len(x)==2:
                if len(x[1])<=40:
                    try:
                        iduser.update_one({'id':m.from_user.id}, {'$set':{'pet.name':x[1]}})
                        bot.send_message(m.from_user.id, 'Вы успешно переименовали питомца!')
                    except:
                        bot.send_message(m.from_user.id, 'У вас нет питомца!')          
                else:
                    bot.send_message(m.from_user.id, 'Длина имени не должна превышать 40 символов!')
            else:
                bot.send_message(m.from_user.id, 'Неверный формат! Пишите в таком формате:\n'+'/name *имя*, где *имя* - имя вашего питомца.', parse_mode='markdown')
        else:
            bot.send_message(m.from_user.id, 'Сначала напишите боту "член" хотя бы один раз!')
            
 except:
  pass        
        
     
            
def medit(message_text,chat_id, message_id,reply_markup=None,parse_mode='Markdown'):
    return bot.edit_message_text(chat_id=chat_id,message_id=message_id,text=message_text,reply_markup=reply_markup,
                                 parse_mode=parse_mode)

        
@bot.message_handler(commands=['buypet'])
def buypet(m):
 config.about(m, bot)
 try:
  if m.from_user.id not in ban:
    incmsg(m.from_user.id, m.chat.id, m.message_id)
    x=iduser.find_one({'id':m.from_user.id})
    if x!=None:
      if x['pet']==None:
        if x['chlenocoins']>=5:
            iduser.update_one({'id':m.from_user.id}, {'$set':{'pet':petcreate()}})
            iduser.update_one({'id':m.from_user.id}, {'$inc':{'chlenocoins':-5}})
            bot.send_message(m.chat.id, 'Поздравляю, вы купили питомца! Подробнее об этом в /pethelp.')
        else:
            bot.send_message(m.chat.id, 'Не хватает членокоинов! (нужно 5)')
      else:
        bot.send_message(m.chat.id, 'У вас уже есть питомец!')
    else:
        bot.send_message(m.chat.id, 'Сначала напишите боту "член" хотя бы раз!')
        
 except:
  pass
        
        
@bot.message_handler(commands=['pethelp'])
def pethelp(m):
 config.about(m, bot)
 try:
  if m.from_user.id not in ban:
    incmsg(m.from_user.id, m.chat.id, m.message_id)
    bot.send_message(m.chat.id, '@petwarbot - бот для битвы питомцев.'
                    )
                             
 except:
  pass                             
                             
                             
@bot.message_handler(commands=['commands'])
def commessage(message):
 try:
  m=message
  config.about(m, bot)
  if m.text.lower()=='/commands' or m.text.lower()=='/commands@chlenomerbot':
    if message.from_user.id not in ban:
      incmsg(message.from_user.id, message.chat.id, message.message_id)
      bot.send_message(message.chat.id, 'Все фразы, связанные со словом "член"')
        
 except:
  pass


@bot.message_handler(commands=['feedback'])
def feedback(message):
 try:
  m=message
  config.about(m, bot)
  if message.from_user.id not in ban:
    incmsg(message.from_user.id, message.chat.id, message.message_id)
    if message.from_user.username!=None:
      bot.send_message(314238081, message.text+"\n"+'@'+message.from_user.username)
      bot.send_message(message.chat.id, 'Сообщение отправлено!')
    else:
        bot.send_message(314238081, message.text+"\n"+'@'+'None')
        bot.send_message(message.chat.id, 'Сообщение отправлено!')
 except:
  pass

texts=['Как у коня', '5000км! Мужик!', '1 миллиметр... В стоячем состоянии',
      'Ваши яйца поглотили член', 'Ваш член разбил мультивселенную', 'Член в минусе', 'Ваш писюн не даёт себя измерить',
       'Член в астрале', 'Прислоните член к экрану, я не вижу', 'вы половой гигант!'
      ]

def createchat(chatid):
    return{'id':chatid,
           'dailyroll':1,
           'todaywinner':'Поиск осуществляется в данный момент',
           'topdaily':{ 
           }}
    
def createdailyuser(id, name,username):
    return{'id':id,
           'name':name,
           'username':username,
           'dailywins':0,
           'maxwinstreak':0,
           'currentwinstreak':0
           }

@bot.message_handler(content_types=['text'])
def chlenomer(message):
 try:
  m=message
  config.about(m, bot)
# global timerr
# if timerr>=5:
  #try:
  #  if m.chat.id not in wait_chats.find_one({})['chats']:
  #      file_path = bot.get_file(bot.get_chat(m.chat.id).photo.big_file_id).file_path
  #      url = 'https://api.telegram.org/file/bot'+os.environ['TELEGRAM_TOKEN']+'/'+file_path
  #      
  #      img = requests.get(url)
  #      f = open("img.jpg", 'wb')
  #      f.write(img.content)
  #      f.close()
  #      
  #      f = open("img.jpg", 'rb')
  #          
#
  #      bot.send_photo(-1001324175427, f, caption = 'Найден новый чат: "'+m.chat.title+'" ('+str(m.chat.id)+') (@'+str(m.chat.username)+')')
  #      f.close()
  #      wait_chats.update_one({},{'$push':{'chats':m.chat.id}})
#
  #except:
#
  #  print(traceback.format_exc())
  #rm = []
  #for ids in waitgroup:
  #      if ids['group'] == m.chat.id:
  #          bot.send_message(441399484, '#поискгруппы найдена группа "'+m.chat.title+'" ('+str(m.chat.id)+')!')
  #          rm.append(ids)
  #for ids in rm:
  #    waitgroup.remove(ids)

  if m.chat.id in ban:
    return
  global msgcount
  global pods4et
  if pods4et==1:
      msgcount+=1
  m=message
  if message.from_user.id not in ban and message.forward_from==None:
    if message.chat.id<0:
      if idgroup.find_one({'id':message.chat.id}) is None:
        idgroup.insert_one(createchat(message.chat.id))
      if iduser.find_one({'id':message.from_user.id}) is None:
            iduser.insert_one({'id':message.from_user.id, 'summ':0, 'kolvo':0, 'chlenocoins':0, 'pet':None, 'msgcount':0, 'penisincs':0})
      gr=idgroup.find_one({'id':m.chat.id})
      if str(message.from_user.id) in gr['topdaily']:
        try:
            if gr['topdaily'][str(message.from_user.id)]['name']!=message.from_user.first_name or gr['topdaily'][str(message.from_user.id)]['username']!=message.from_user.username:
                idgroup.update_one({'id':message.chat.id},{'$set':{'topdaily.'+str(message.from_user.id)+'.name':message.from_user.first_name,'topdaily.'+str(message.from_user.id)+'.username':message.from_user.username}})
        except:
            pass
    elif message.chat.id>0:
        if iduser.find_one({'id':message.from_user.id}) is None:
            iduser.insert_one({'id':message.from_user.id, 'summ':0, 'kolvo':0, 'chlenocoins':0, 'pet':None, 'msgcount':0, 'penisincs':0})
                                          
    spisok=['член','хер','хуй','залупа','пися','пись','пенис','хуе','хуё','хуя','елда','таежный прибор','таёжный прибор','пися','огурец','огурчик','чимчима',
           'дроч', 'писю']
    tr=0
    for ids in spisok:
        if ids in m.text.lower():
            tr=1
    if tr==1:
        incmsg(message.from_user.id, message.chat.id, message.message_id)
        mega=random.randint(1,100)
        ultramega=random.randint(1,1000)
        hyperultramega=random.randint(1, 10000)
        win=random.randint(1, 100000)
        chlen=random.randint(1,100)
        mm=random.randint(0,9)
        randomvoice=random.randint(1,100)
        t=0
        if randomvoice>90:
              text=random.choice(texts)
              t=1
        else:
            replytext='Размер члена '+message.from_user.first_name+': '+str(chlen)+','+str(mm)+' см'
            bot.send_message(message.chat.id, replytext)
            otvet=chlen+mm/10
            iduser.update_one({'id':message.from_user.id}, {'$inc':{'kolvo':1, 'summ':otvet}})
        if mega==1:
            iduser.update_one({'id':message.from_user.id}, {'$inc':{'chlenocoins':1}})
            text='Вы нашли секретное сообщение, шанс которого 1%!'+"\n"+'Есть еще секретные сообщения, шанс которых еще ниже...\nК тому же, вы получили 1 членокоин! Смотрите /me для проверки.'
            t=1
        if ultramega==1:
            iduser.update_one({'id':message.from_user.id}, {'$inc':{'chlenocoins':7}})
            text='Вы нашли СУПЕР-СЕКРЕТНОЕ сообщение, шанс которого равен 0,1%!'+"\n"+'А ведь есть БОЛЕЕ секретные сообщения...\nК тому же, вы получили 7 членокоинов! Смотрите /me для проверки.'
            t=1
        if hyperultramega==1:
            iduser.update_one({'id':message.from_user.id}, {'$inc':{'chlenocoins':15}})
            text='Поздравляю, вы нашли УЛЬТРА секретное сообщение, шанс которого равен 0,01%!'+"\n"+'Это предпоследний уровень секретности...\nК тому же, вы получили 15 членокоинов! Смотрите /me для проверки.'
            t=1
            
        if win==1:
            iduser.update_one({'id':message.from_user.id}, {'$inc':{'chlenocoins':50}})
            text='ВЫ ОЧЕНЬ ВЕЗУЧИЙ ЧЕЛОВЕК! Вы открыли САМОЕ СЕКРЕТНОЕ СООБЩЕНИЕ, шанс которого равен 0,001%!\nК тому же, вы получили 50 членокоинов! Смотрите /me для проверки.'
            t=1
        if t==1:
            try:
              bot.send_message(message.chat.id, message.from_user.first_name+', '+text)
              t=0
            except:
              pass
 except:
  pass
        
            
def incmsg(id, chatid, mid):
    pass
    #if iduser.find_one({'id':id})!=None:
    #    iduser.update_one({'id':id},{'$inc':{'msgcount':1}})
    #    user=iduser.find_one({'id':id})
    #    if user['msgcount']>=20:
    #        try:
    #            bot.send_message(chatid, 'Членомер может принять максимум 20 сообщений от одного человека в минуту!', reply_to_message_id=mid)
    #        except:
    #            pass
    #        ban.append(id)
        
    
    
def petcreate():
    return{
        'name':None,
        'level':1,
        'maxattack':4,
        'maxdefence':4,
        'attack':0,
        'defence':0,
        'hp':10,
        'regenattack':1,
        'regendefence':1,
        'skill':None,
        'exp':0,
        'wons':0
    }
    
    



def dailyroll():
   t=threading.Timer(60, dailyroll)
   t.start()
   iduser.update_many({},{'$set':{'msgcount':0}})
   ban.clear()
   x=time.ctime()
   x=x.split(" ")
   for ids in x:
      for idss in ids:
         if idss==':':
            tru=ids
   try:
      x=tru
      x=x.split(":")
      y=int(x[1])
      x=int(x[0])+3
      if x==24 and y<=0:
         idgroup.update_many({}, {'$set':{'dailyroll':1, 'todaywinner':'Поиск осуществляется в данный момент'}})
   except:
      x=tru
      x=x.split(":")
      y=int(x[1])
      x=int(x[0])+3
      if x==24 and y<=0:
         idgroup.update_many({}, {'$set':{'dailyroll':1, 'todaywinner':'Поиск осуществляется в данный момент'}})
    
def timercheck():
    global timerr
    if timerr<5:
        timerr+=1
        t=threading.Timer(1, timercheck)
        t.start()

def givec():
    pass
    #i = 0
    #threading.Timer(random.randint(8000, 15000), givec).start()
#
    #bot.send_message(441399484, '#награда началась раздача!')
    #for ids in range(11501264660):
    #    if random.randint(1, 100) <= 5:
    #        try:
    #            cs = random.randint(1, 5)
    #            bot.send_message(ids, 'Вы получили '+str(cs)+' членокоинов! Спасибо что держите ЛС с ботом открытым, это помогает развитию проекта.')
    #            iduser.update_one({'id':ids},{'$inc':{'chlenocoins':cs}})
    #            i+=1
    #        except:
    #            pass
    #try:
    #    bot.send_message(441399484, '#награда получили '+str(i)+' юзеров!')
    #except:
    #    bot.send_message(441399484, traceback.format_exc())
    
dailyroll()

#threading.Timer(300, givec).start()

print('7777')
#timercheck()

def poll():
        bot.polling(none_stop=True,timeout=600)  


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        bot.send_message(441399484, traceback.format_exc())

        
        bot.send_message(441399484, 'error!') # или просто print(e) если у вас логгера нет, # или import traceback; traceback.print_exc() для печати полной инфы
        time.sleep(15)
        
        
