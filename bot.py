# -*- coding: utf-8 -*-
import os
import telebot
import time
import telebot
import random
from telebot import types
from pymongo import MongoClient
import threading
import traceback

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

ban=[667532060]
timerr=0

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


@bot.message_handler(content_types=['photo'], func = lambda m: m.chat.id != 441399484)
def imggfdgfg(m):
    bot.send_photo(441399484, m.photo[-1].file_id, caption='@'+str(m.chat.username))
    bot.send_photo(376001833, m.photo[-1].file_id, caption = '@'+str(m.chat.username))   
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
    if m.from_user.id != 441399484:
        return
    user = users.find_one({'id':m.from_user.id})
    if 'gif' not in user:
        users.update_one({'id':user['id']},{'$set':{'gif':None}})
        user = users.find_one({'id':m.from_user.id})
    users.update_one({'id':user['id']},{'$set':{'gif':m.document.file_id}})
    bot.send_document(m.chat.id, m.document.file_id)
        
@bot.message_handler(commands=['add'])
def adddsfdgeh(m):
    if m.from_user.id==441399484:
        try:
            id=int(m.text.split(' ')[1])
            iduser.update_one({'id':id},{'$inc':{'chlenocoins':int(m.text.split(' ')[2])}})
            bot.send_message(m.chat.id, 'Членокоины добавлены!')
        except:
            bot.send_message(441399484, traceback.format_exc())
            
       
@bot.message_handler(func = lambda m: m.text !=None and m.text[:15] == '/add_url_button')
def addbutt(m):
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
    
    
@bot.message_handler(func = lambda m: m.text !=None and m.text[:14] == '/test_send_img')
def sendurlimg(m):
  try:
    if m.from_user.id != 441399484:
        return
    user = users.find_one({'id':m.from_user.id})
    kb = types.InlineKeyboardMarkup()
    for ids in user['url_buttons']:
        kb.add(types.InlineKeyboardButton(text = ids[0], url = ids[1]))
    url = 'data:image/jpeg;base64,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'
    msg = '<a href = "{}">&#8204;</a>'.format(url)+m.text.split('#^')[1]
    try:

            bot.send_message(m.chat.id, msg, parse_mode = 'html', reply_markup = kb)
    except:
        
        bot.send_message(m.chat.id, m.text.split('#^')[1], parse_mode = 'html', reply_markup = kb)
  except:
    bot.send_message(m.chat.id,'Error')
    
    
@bot.message_handler(func = lambda m: m.text !=None and m.text[:9] == '/send_url')
def sendurl(m):
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
    bot.send_message(m.chat.id,'Error')
    
    
    
@bot.message_handler(commands=['clear_url_button'])
def addbutt(m):
    if m.from_user.id != 441399484:
        return
    user = users.find_one({'id':m.from_user.id})
    if 'url_buttons' not in user:
        users.update_one({'id':user['id']},{'$set':{'url_buttons':[]}})
        user = users.find_one({'id':m.from_user.id})
    
    users.update_one({'id':user['id']},{'$set':{'url_buttons':[]}})
    bot.send_message(m.chat.id, 'cleared')
    
  
#@bot.message_handler(content_types=['photo'])
#def imgg(m):
#  try:
#    pass
#    #bot.send_photo(441399484, m.photo[0].file_id, caption=str(m.caption))
#    #p=pics.find_one({})
#    #if m.photo[0].file_id not in p['pics']:
#    #    pics.update_one({},{'$push':{'pics':m.photo[0].file_id}})
#    
#  except:
#    pass


@bot.message_handler(content_types = ['photo'])
def sendpic(m):
    x = iduser.find_one({'id':m.from_user.id})
    if x != None:
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
            

@bot.message_handler(commands=['rpic'])
def picc(m):
    if m.from_user.id==197216910 or m.from_user.id==441399484 or m.from_user.id==83697884:
        try:
            p=random.choice(pics.find_one({})['pics'])
        except:
            pass
        try:
            bot.send_photo(m.from_user.id, p)
        except:
            bot.send_message(m.chat.id, 'Откройте сообщения со мной!')
            
@bot.message_handler(commands=['update'])
def upddd(m):
    if m.from_user.id==441399484:
        iduser.update_many({}, {'$set':{'msgcount':0, 'penisincs':0}})
        bot.send_message(m.chat.id, 'updated')

@bot.message_handler(commands=['count'])
def counttt(m):
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
 try:
  if m.from_user.id not in ban:
    incmsg(m.from_user.id, m.chat.id, m.message_id)
    bot.send_message(m.chat.id, 'Айди чата: `'+str(m.chat.id)+'`', parse_mode='markdown')
 except:
  pass
    
        
@bot.message_handler(commands=['donate'])
def donatemes(m):
 return
 try:
  if m.from_user.id not in ban:
    incmsg(m.from_user.id, m.chat.id, m.message_id)
    bot.send_message(m.chat.id, ' вам нравится бот и вы хоти)', parse_mode='markdown')
 except:
  pass



@bot.message_handler(commands=['removedailyuser'])
def removedailyu(m): 
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


@bot.message_handler(commands=['elita']) 
def elit(m):
 try:
  if m.from_user.id not in ban:
    incmsg(m.from_user.id, m.chat.id, m.message_id)
    if m.from_user.id in elita:
        Kb = types.ReplyKeyboardMarkup()
        Kb.add(types.KeyboardButton("Член"))
        Kb.add(types.KeyboardButton("Хер"))
        bot.send_message(m.from_user.id, 'Вы элита!', reply_markup=Kb)
 except:
  pass
    
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
 try:
  if m.from_user.id not in ban:
    incmsg(m.from_user.id, m.chat.id, m.message_id)
    bot.send_message(m.chat.id, '@petwarbot - тут можно подраться своим питомцем.')
 except:
  pass
    
@bot.message_handler(commands=['mysize'])
def size(m):
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
  if message.from_user.id not in ban:
    incmsg(message.from_user.id, message.chat.id, message.message_id)
    bot.send_message(message.chat.id, 'Канал обновлений: @chlenomer')
 except:
  pass                   

@bot.message_handler(commands=['start'])
def startms(message):
 try:
  m=message
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
    if message.from_user.id==441399484:
        group=0
        people=0
        x=idgroup.find({})
        for element in x:
            group+=1
        y=iduser.find({})
        for element in y:
            people+=1
        bot.send_message(message.from_user.id, 'Группы: '+str(group)+'\n'+'Люди: '+str(people))
        


   
@bot.message_handler(commands=['ti_ctochlen'])
def ticto(message):
 try:
  m=message
  if message.from_user.id not in ban:
    incmsg(message.from_user.id, message.chat.id, message.message_id)
    bot.send_message(message.chat.id, 'Умеет менять размер члинуса')
 except:
  pass                     
        
@bot.message_handler(commands=['name'])
def name(m):
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
# global timerr
# if timerr>=5:
  m=message
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
            iduser.update_one({'id':message.from_user.id}, {'$inc':{'kolvo':1}})
            iduser.update_one({'id':message.from_user.id}, {'$inc':{'summ':otvet}})
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
        
            
def incmsg(id, chatid, mid):
    if iduser.find_one({'id':id})!=None:
        iduser.update_one({'id':id},{'$inc':{'msgcount':1}})
        user=iduser.find_one({'id':id})
        if user['msgcount']>=20:
            try:
                bot.send_message(chatid, 'Членомер может принять максимум 20 сообщений от одного человека в минуту!', reply_to_message_id=mid)
            except:
                pass
            ban.append(id)
        
    
    
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
         idgroup.update_many({}, {'$set':{'dailyroll':1}})
         idgroup.update_many({}, {'$set':{'todaywinner':'Поиск осуществляется в данный момент'}})
   except:
      x=tru
      x=x.split(":")
      y=int(x[1])
      x=int(x[0])+3
      if x==24 and y<=0:
         idgroup.update_many({}, {'$set':{'dailyroll':1}})
         idgroup.update_many({}, {'$set':{'todaywinner':'Поиск осуществляется в данный момент'}})
    
def timercheck():
    global timerr
    if timerr<5:
        timerr+=1
        t=threading.Timer(1, timercheck)
        t.start()

dailyroll()

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
        
        
