# -*- coding: utf-8 -*-
import os
import telebot
import time
import chlenomerconfig
import telebot
import random
from telebot import types
from pymongo import MongoClient
import threading

client1=os.environ['database']
client=MongoClient(client1)
db=client.chlenomer
idgroup=db.ids
iduser=db.ids_people

ban=[]

wait=[]
ch=[]
members=[]
play=[]




token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)
writed=[
]
massive=['Хер','хер','Член','член','Хуй','хуй']
elita=[441399484, 55888804, 314238081]


@bot.message_handler(commands=['id'])
def iddd(m):
    if m.reply_to_message!=None:
        user=m.reply_to_message.from_user
        bot.send_message(m.chat.id, 'id выбранного пользователя:\n'+'`'+str(user.id)+'`',reply_to_message_id=m.message_id,parse_mode='markdown')
    else:
        bot.send_message(m.chat.id, 'Чтобы узнать id пользователя, введите эту команду, ответив на его сообщение.')

@bot.message_handler(commands=['donate'])
def donatemes(m):
    bot.send_message(m.chat.id, 'Если вам нравится бот и вы хотите поддержать разработчика, переводите деньги на карту:\n`5336 6900 5562 4037`\nЗаранее благодарю)', parse_mode='markdown')

@bot.message_handler(commands=['removedailyuser'])
def removedailyu(m):
    x=get.chat.administrators()
    tr=0
    for ids in x:
        print(ids)
        if m.from_user.id==ids.id:
            tr=1
    if tr==1:
        bot.send_message(m.chat.id, 'Вы админ чата!')
    else:
        bot.send_message(m.chat.id, 'Вы не админ чата!')
    
    
    
@bot.message_handler(commands=['sendm'])
def sendmes(message):
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
    if m.from_user.id in elita:
        Kb = types.ReplyKeyboardMarkup()
        Kb.add(types.KeyboardButton("Член"))
        Kb.add(types.KeyboardButton("Хер"))
        bot.send_message(m.from_user.id, 'Вы элита!', reply_markup=Kb)
    
    
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
        
def turn2(id):
    bot.send_message(id, 'Сканирую каждый член, не двигайтесь...')
    t=threading.Timer(2, turn3, args=[id])
    t.start()
    
    
def turn3(id):
    x=idgroup.find_one({'id':id})
    lst=[]
    for ids in x['topdaily']:
        try:
            lst.append(x['topdaily'][ids]['id'])
        except:
            pass
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
      if x['topdaily'][ids]['id']!=y:
        idgroup.update_one({'id':id},{'$set':{'topdaily.'+str(x['topdaily'][ids]['id'])+'.currentwinstreak':0}})
    bot.send_message(id, 'Измерения успешно проведены. В данный момент стояк можно наблюдать у пользователя:\n\n'+name+' (@'+username+')!')

    
    
@bot.message_handler(commands=['topchlens'])
def topchlen(m):
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

                
                
                        
                       
    
@bot.message_handler(commands=['dailychlenreg'])
def dailyr(m):
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


@bot.message_handler(commands=['usecoins'])
def usecoins(m):
    bot.send_message(m.chat.id, '@petwarbot - тут можно подраться своим питомцем')
    
    
@bot.message_handler(commands=['mysize'])
def size(m):
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
                        
    
    
@bot.message_handler(commands=['me'])
def mme(m):
    x=iduser.find_one({'id': m.from_user.id})
    try:
     bot.send_message(m.chat.id, m.from_user.first_name+', Ваши членокоины: '+str(x['chlenocoins'])+'. За 5 вы можете купить питомца! (Команда /buypet).')
     bot.send_message(441399484, m.from_user.first_name+', Ваши членокоины: '+str(x['chlenocoins'])+'. Сейчас они не нужны, но следите за обновлениями - в будущем они понадобятся!')                                                                                                                                     
    except:
        bot.send_message(m.chat.id, 'Упс! Какая-то ошибка! Наверное, вы ни разу не измеряли член! (напишите боту "член")')
        bot.send_message(441399484, 'Упс! Какая-то ошибка! Наверное, вы ни рару не измеряли член!')                                                                                                                               
                                                                 
                                                                  
@bot.message_handler(commands=['challenge'])
def challenge(m):
    if m.from_user.id==441399484:
      if len(ch)<1:
        bot.send_message(m.chat.id, 'Конкурс за приз - кнопки внутри членомера - начинается! Жмите /joen для присоединения!')
        ch.append(m.chat.id)
                
                

@bot.message_handler(commands=['joen'])
def joen(m):
    if m.chat.id in ch and m.from_user.id not in members:
        if m.chat.id==ch[0]:
            members.append(m.from_user.id)
            
            
@bot.message_handler(commands=['begin'])
def begin(m):
    pass
                
@bot.message_handler(commands=['channel'])
def channel(message):
    bot.send_message(message.chat.id, 'Канал обновлений: @chlenomer')
                     

@bot.message_handler(commands=['start'])
def startms(message):
  if message.from_user.id==message.chat.id:
    bot.send_message(message.from_user.id, 'Если ты здесь, то ты наверняка хочешь измерить член! Пиши /commands, чтобы узнать, на какие слова реагирует бот')


@bot.message_handler(commands=['info'])
def info(message):
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
    bot.send_message(message.from_user.id, 'Умеет менять размер члинуса')
                     
        
@bot.message_handler(commands=['name'])
def name(m):
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
            
        
        
        

@bot.message_handler(commands=['fight'])
def fight(m):
  if m.from_user.id==441399484 or m.from_user.id==314238081:
    if m.chat.id>0:
      z=iduser.find_one({'id':m.from_user.id})
      if z!=None:
        if z['pet']!=None:
          if z['pet']['name']!=None:
            t=threading.Timer(300, noplayers, args=[m.from_user.id])
            t.start()
            bot.send_message(m.chat.id, 'Вы встали в очередь на поединок питомцев! Ожидайте игроков...')
            wait.append(m.from_user.id)
            player=iduser.find_one({'id':m.from_user.id})
            for id in wait:
                if id!=m.from_user.id:
                    x=iduser.find_one({'id':id})
                    if x['pet']['level']==player['pet']['level']: 
                        name1=player['pet']['name']
                        name2=x['pet']['name']
                        try:
                            wait.remove(player['id'])
                        except:
                            pass
                        try:
                            wait.remove(x['id'])
                        except:
                            pass
                        gofight(player['id'], x['id'], name1, name2)                
          else:
            bot.send_message(m.from_user.id, 'Сначала дайте питомцу имя! (команда /name)') 
        else:
            bot.send_message(m.from_user.id, 'У вас нет питомца!')
      else:
        bot.send_message(m.from_user.id, 'Сначала напишите боту "член"!')
    else:
       bot.send_message(m.from_user.id, 'Эту команду можно использовать только в личных сообщениях бота!') 
  else:
    bot.send_message(m.chat.id, 'В будущих обновлениях...')

@bot.message_handler(commands=['cancel'])
def cancel(m):
    try:
        wait.remove(m.from_user.id)
        bot.send_message(m.from_user.id, 'Вы  были успешно удалены из очереди.') 
    except:
        pass
    
    
@bot.callback_query_handler(func=lambda call:True)
def inline(call):
    ataka=0
    user=call.from_user.id
    if call.data=='atk+1':
        ataka=1
    elif call.data=='atk+2':
        ataka=2
    elif call.data=='atk+5':
        ataka=5
    elif call.data=='atk+10':
        ataka=10
    if ataka>0:
        x=0
        for ids in play:
            if ids['id1']['id']==user:
                x=1
                y=ids['id1']
            if ids['id2']['id']==user:
                x=1
                y=ids['id2']
        if x==1:
            if y['attackselect']==1:
                if y['attack']>=ataka:
                    y['attackround']+=ataka
                    y['attack']-=ataka
                    Keyboard=types.InlineKeyboardMarkup()
                    Keyboard.add(types.InlineKeyboardButton(text='+1', callback_data='atk+1'))
                    Keyboard.add(types.InlineKeyboardButton(text='+2', callback_data='atk+2'))
                    Keyboard.add(types.InlineKeyboardButton(text='+5', callback_data='atk+5'))
                    Keyboard.add(types.InlineKeyboardButton(text='+10', callback_data='atk+10'))
                    Keyboard.add(types.InlineKeyboardButton(text='Окончить выбор', callback_data='endattack'))
                    medit('Теперь выставьте количество атаки, которое хотите поставить в этом ходу. Текущая атака: '+str(y['attackround']),
                    call.from_user.id,
                    call.message.message_id, reply_markup=Keyboard)
                else:
                    bot.send_message(user, 'У вас недостаточно атаки!')
            else:
                bot.send_message(user, 'Нет!')
                
                
    defence=0
    user=call.from_user.id
    if call.data=='def+1':
        defence=1
    elif call.data=='def+2':
        defence=2
    elif call.data=='def+5':
        defence=5
    elif call.data=='def+10':
        defence=10
    if defence>0:
        x=0
        for ids in play:
            if ids['id1']['id']==user:
                x=1
                y=ids['id1']
            if ids['id2']['id']==user:
                x=1
                y=ids['id2']
        if x==1:
            if y['defenceselect']==1:
                if y['defence']>=defence:
                    y['defenceround']+=defence
                    y['defence']-=defence
                    Keyboard=types.InlineKeyboardMarkup()
                    Keyboard.add(types.InlineKeyboardButton(text='+1', callback_data='def+1'))
                    Keyboard.add(types.InlineKeyboardButton(text='+2', callback_data='def+2'))
                    Keyboard.add(types.InlineKeyboardButton(text='+5', callback_data='def+5'))
                    Keyboard.add(types.InlineKeyboardButton(text='+10', callback_data='def+10'))
                    Keyboard.add(types.InlineKeyboardButton(text='Окончить выбор', callback_data='enddefence'))
                    medit('Теперь выставьте количество защиты, которое хотите поставить в этом ходу. Текущая защита: '+str(y['defenceround']),
                    call.from_user.id,
                    call.message.message_id, reply_markup=Keyboard)
                else:
                    bot.send_message(user, 'У вас недостаточно защиты!')
            else:
                bot.send_message(user, 'Нет!')
                    
    elif defence==0:
        if call.data=='endattack':
          x=0
          for ids in play:
            if ids['id1']['id']==user:
                x=1
                y=ids['id1']
            if ids['id2']['id']==user:
                x=1
                y=ids['id2']
          if x==1:
            if y['attackselect']==1:
                y['attackselect']=0
                y['defenceselect']=1
                Keyboard=types.InlineKeyboardMarkup()
                Keyboard.add(types.InlineKeyboardButton(text='+1', callback_data='def+1'))
                Keyboard.add(types.InlineKeyboardButton(text='+2', callback_data='def+2'))
                Keyboard.add(types.InlineKeyboardButton(text='+5', callback_data='def+5'))
                Keyboard.add(types.InlineKeyboardButton(text='+10', callback_data='def+10'))
                Keyboard.add(types.InlineKeyboardButton(text='Окончить выбор', callback_data='enddef'))
                medit('Теперь выставьте количество защиты, которое хотите поставить в этом ходу. Текущая защита: 0', call.from_user.id, call.message.message_id, reply_markup=Keyboard)
                        
    else:
        if call.data=='enddefence':
          x=0
          for ids in play:
            if ids['id1']['id']==user:
                x=1
                y=ids['id1']
            if ids['id2']['id']==user:
                x=1
                y=ids['id2']
          if x==1:
            try:
                y['timer'].cancel()
            except:
                pass
            ready(call.from_user.id)


            

            
            
            
def medit(message_text,chat_id, message_id,reply_markup=None,parse_mode='Markdown'):
    return bot.edit_message_text(chat_id=chat_id,message_id=message_id,text=message_text,reply_markup=reply_markup,
                                 parse_mode=parse_mode)


def gofight(id1, id2, name1, name2):
    player1=iduser.find_one({'id':id1})
    player2=iduser.find_one({'id':id2})
    player1['pet']['attack']=player1['pet']['maxattack']
    player1['pet']['defence']=player1['pet']['maxdefence']
    player2['pet']['attack']=player2['pet']['maxattack']
    player2['pet']['defence']=player2['pet']['maxdefence']
    play.append(creategame(id1, id2, player1, player2))
    bot.send_message(id1, 'Битва начинается! Ваш питомец дерётся с питомцем, которого зовут '+'"'+name2+'"'+'! Его уровень: '+str(player2['pet']['level']))
    bot.send_message(id2, 'Битва начинается! Ваш питомец дерётся с питомцем, которого зовут '+'"'+name1+'"'+'! Его уровень: '+str(player1['pet']['level']))
    xod(id1, id2, name1, name2, player1, player2)
    
    
    
def xod(id1, id2, name1, name2, player1, player2):
    if player1['pet']['skill']==None:
        skill1='Отсутствует'
    else:
        skill1=player1['pet']['skill']
        
    if player2['pet']['skill']==None:
        skill2='Отсутствует'
    else:
        skill2=player2['pet']['skill']
    bot.send_message(id1, 'Информация о вашем питомце:\n'+'❤️ХП: '+str(player1['pet']['hp'])+
                     '\n⚔️Атака: '+str(player1['pet']['attack'])+'/'+str(player1['pet']['maxattack'])+'\n'+
                     '⚡️Реген атаки: '+str(player1['pet']['regenattack'])+'\n'+
                    '🛡Защита: '+str(player1['pet']['defence'])+'/'+str(player1['pet']['maxdefence'])+'\n'+
                     '🔵Реген защиты: '+str(player1['pet']['regendefence'])+'\n'+
                     '🔺Скилл: '+skill1       
                    )
    
    bot.send_message(id2, 'Информация о вашем питомце:\n'+'❤️ХП: '+str(player2['pet']['hp'])+
                     '\n⚔️Атака: '+str(player2['pet']['attack'])+'/'+str(player2['pet']['maxattack'])+'\n'+
                     '⚡️Реген атаки: '+str(player2['pet']['regenattack'])+'\n'+
                    '🛡Защита: '+str(player2['pet']['defence'])+'/'+str(player2['pet']['maxdefence'])+'\n'+
                     '🔵Реген защиты: '+str(player2['pet']['regendefence'])+'\n'+
                     '🔺Скилл: '+skill2       
                    )
    for ids in play:
            if ids['id1']['id']==id1:
                ids['id1']['attackselect']=1
            if ids['id2']['id']==id1:
                ids['id2']['attackselect']=1
            if ids['id1']['id']==id2:
                ids['id1']['attackselect']=1
            if ids['id2']['id']==id2:
                ids['id2']['attackselect']=1
    t=threading.Timer(60, noready, args=[ids])
    t.start()
    ids['timer']=t
    Keyboard=types.InlineKeyboardMarkup()
    Keyboard.add(types.InlineKeyboardButton(text='+1', callback_data='atk+1'))
    Keyboard.add(types.InlineKeyboardButton(text='+2', callback_data='atk+2'))
    Keyboard.add(types.InlineKeyboardButton(text='+5', callback_data='atk+5'))
    Keyboard.add(types.InlineKeyboardButton(text='+10', callback_data='atk+10'))
    Keyboard.add(types.InlineKeyboardButton(text='Окончить выбор', callback_data='endattack'))
    msg1=bot.send_message(id1, 'Теперь выставьте количество атаки, которое хотите поставить в этом ходу. Текущая атака: 0', reply_markup=Keyboard)  
    msg2=bot.send_message(id2, 'Теперь выставьте количество атаки, которое хотите поставить в этом ходу. Текущая атака: 0', reply_markup=Keyboard)
    

def ready(id):
    for ids in play:
            if ids['id1']['id']==id:
                ids['id1']['ready']=1
            if ids['id2']['id']==id:
                ids['id2']['ready']=1
            if ids['id1']['ready']==1 and ids['id2']['ready']==1:
                endturn(ids)


def noready(game):
    endturn(game)
                

def endturn(game):#############################################################  ENDTURN
    text1=''
    text2=''
    player1=game['id1']
    player2=game['id2']
    damage1=player1['attackround']
    damage2=player2['attackround']
    defence1=player1['defenceround']
    defence2=player2['defenceround']
    losehp1=damage2-defence1
    if losehp1<0:
        losehp1=0
    player1['hp']-=losehp1
    text1+=player1['name']+':\n'+'Выставленная атака: '+str(player1['attackround'])+'\nВыставленная защита: '+str(player1['defenceround'])+'\nПолученный урон: '+str(losehp1)
    
        
    losehp2=dagame1-defence2
    if losehp2<0:
        losehp2=0
    player2['hp']-=losehp2
    text2+=player2['name']+':\n'+'Выставленная атака: '+str(player2['attackround'])+'\nВыставленная защита: '+str(player2['defenceround'])+'\nПолученный урон: '+str(losehp2)
        
        
    bot.send_message(player1['id'], 'Результаты хода:\n\n'+text1+'\n'+text2)
    bot.send_message(player2['id'], 'Результаты хода:\n\n'+text1+'\n'+text2)
        
        
        
def noplayers(id):
    try:
        wait.remove(id)
        bot.send_message(id, 'Вы ожидали оппонента 5 минут и были удалены из очереди! Попробуйте позже, когда будут ещё бойцы.')
    except:
        pass
        
@bot.message_handler(commands=['buypet'])
def buypet(m):
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
        

        
        
@bot.message_handler(commands=['pethelp'])
def pethelp(m):
    bot.send_message(m.chat.id, 'Питомец вам нужен для участия в боях. Чтобы поучаствовать, нужно написать боту в личные сообщения команду /fight.\n'+
                     'У питомца есть ХП, Атака, Защита, Регенерация атаки, Регенерация защиты. '+
                     'Каждый ход вы выбираете, сколько атаки и сколько защиты поставить на раунд... И ваш питомец сражается своим членом! Каждая поставленная единица защиты заблокирует единицу атаки соперника.\n'+
                     'Таким образом, если вы ставите 2 атаки и 3 брони, а ваш соперник - 3 атаки и 1 броню, то вы получите 0 урона, а он получит 1 урон.\n'+
                     'Прокачка питомца сейчас недоступна, но в будущем появится!'
                    )
                             
                             
                             
                             
@bot.message_handler(commands=['commands'])
def commessage(message):
    bot.send_message(message.chat.id, 'Все фразы, связанные со словом "член"')
        
@bot.message_handler(commands=['feedback'])
def feedback(message):
    if message.from_user.username!=None:
      bot.send_message(314238081, message.text+"\n"+'@'+message.from_user.username)
      bot.send_message(message.chat.id, 'Сообщение отправлено!')
    else:
        bot.send_message(314238081, message.text+"\n"+'@'+'None')
        bot.send_message(message.chat.id, 'Сообщение отправлено!')


texts=['Как у коня', '5000км! Мужик!', '1 миллиметр... В стоячем состоянии',
      'Ваши яйца поглотили член', 'Ваш член разбил мультивселенную', 'Член в минусе', 'Ваш писюн не даёт себя измерить',
       'Член в астрале', 'Прислоните член к экрану, я не вижу'
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
  m=message
  if message.from_user.id not in ban:
    if message.chat.id<0:
      if idgroup.find_one({'id':message.chat.id}) is None:
        idgroup.insert_one(createchat(message.chat.id))
      if iduser.find_one({'id':message.from_user.id}) is None:
            iduser.insert_one({'id':message.from_user.id, 'summ':0, 'kolvo':0, 'chlenocoins':0, 'pet':None})
      idgroup.update_one({'id':m.chat.id},{'$set':{'topdaily.'+str(m.from_user.id)+'.name':m.from_user.first_name,'topdaily.'+str(m.from_user.id)+'.username':m.from_user.username}})
    elif message.chat.id>0:
        if iduser.find_one({'id':message.from_user.id}) is None:
            iduser.insert_one({'id':message.from_user.id, 'summ':0, 'kolvo':0, 'chlenocoins':0, 'pet':None})
        x=idgroup.find_one({'id':message.chat.id})
        if x!=None:
          try:
            z=x['topdaily'][message.from_user.id]
            if z!=None:
                idgroup.update_one({'id':message.chat.id},{'$set':{'topdaily.'+message.from_user.id+'.name':message.from_user.first_name}})
          except:
            pass
                                          
    spisok=['член','хер','хуй','залупа','пися','пись','пенис','хуе','хуё','хуя','елда','таежный прибор','таёжный прибор','пися','огурец','огурчик','чимчима',
           'дроч']
    tr=0
    for ids in spisok:
        if ids in m.text.lower():
            tr=1
    if tr==1:
        print(message.chat.id)
        mega=random.randint(1,100)
        ultramega=random.randint(1,1000)
        hyperultramega=random.randint(1, 10000)
        win=random.randint(1, 100000)
        xxx=0
        listtt=[]
        while xxx<=100:
            listtt.append(xxx)
            xxx+=1
        chlen=int(random.choice(listtt))
        mm=random.randint(0,9)
        randomvoice=random.randint(1,100)
        t=0
        if randomvoice>90:
              chlen = random.randint(1, 6)
              text=texts[chlen-1]
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
        

 
def creategame(id1, id2, player1, player2):
            return{
                'timer':None,
                'id1':{'id':id1,
                       'attackselect':0,
                       'defenceselect':0,
                       'maxattack':player1['pet']['maxattack'],
                       'maxdefence':player1['pet']['maxdefence'],
                       'attack':player1['pet']['maxattack'],
                       'defence':player1['pet']['maxdefence'],
                       'attackround':0,
                       'defenceround':0,
                       'ready':0,
                       'name':player1['pet']['name']
                      },
                'id2':{
                    'id':id2,
                    'attackselect':0,
                    'defenceselect':0,
                    'maxattack':player2['pet']['maxattack'],
                    'maxdefence':player2['pet']['maxdefence'],
                    'attack':player2['pet']['maxattack'],
                    'defence':player2['pet']['maxdefence'],
                    'attackround':0,
                    'defenceround':0,
                    'ready':0,
                    'name':player2['pet']['name']
                     }
            }
            
            
            
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
    
    
if True:
    dailyroll()

if True:
 try:
   print('7777')
   bot.polling(none_stop=True,timeout=600)
 except:
        print('!!! READTIME OUT !!!')           
        bot.stop_polling()
        time.sleep(1)
        check = True
        while check==True:
          try:
            bot.polling(none_stop=True,timeout=1)
            print('checkkk')
            check = False
          except:
            time.sleep(1)                    






