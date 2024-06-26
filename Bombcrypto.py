import pyautogui
import time
import random


def printSleep(msg, t):
  for i in range(1, t):
    print(msg + "(" + str(i) + "/" + str(t) + ")")
    time.sleep(1)

def moveAndClick(img, confidence=0.8):
  location = list(pyautogui.locateAllOnScreen(img, grayscale=True, confidence=confidence))
  if not location:
    return False

  left, top, width, height = location[-1]

  pyautogui.moveTo(left + random.randint(2, width), top + random.randint(2, height), random.uniform(0.1, 0.15))
  pyautogui.click()
  time.sleep(1)
  return True

def dragTo(img1, img2):
  location = list(pyautogui.locateAllOnScreen(img1, grayscale=True, confidence=0.65))
  if not location:
    return False

  left, top, width, height = location[-1]

  x = left + random.randint(0, width)
  y = top + random.randint(0, height)

  location = list(pyautogui.locateAllOnScreen(img2, grayscale=True, confidence=0.65))
  if not location:
    return False

  left, top, width, height = location[-1]

  moveX = left + random.randint(0, width)
  moveY = top + random.randint(0, height)

  pyautogui.moveTo(x, y, random.uniform(0.05, 0.2))
  pyautogui.dragTo(moveX, moveY, duration=0.5, button='left')

  return True

def moveAndClickCustom(img, randW, randH, confidence=0.8):
  location = list(pyautogui.locateAllOnScreen(img, grayscale=True, confidence=confidence))
  if not location:
    return False

  left, top, width, height = location[-1]

  pyautogui.moveTo(left + random.randint(2, randW), top + random.randint(2, randH), random.uniform(0.1, 0.15))
  pyautogui.click()
  time.sleep(1)
  return True

def whereAmI():
  d = {
    # 登入
    'login': 'img/connect_wallet.png',
    # 地圖頁
    'map': 'img/map.png',
    # 簽證
    'sign': 'img/sign.png',
    # 簽證 (chrome)
    'sign': 'img/sign_chrome.png',
    # 角色頁
    'character': 'img/character.png',
    # 角色頁
    'character': 'img/character_202202.png',
    # 角色頁 (new year)
    'character': 'img/character_new_year.png',
    # 錯誤
    'error': 'img/error.png',
    # new map
    'new': 'img/new_map.png',
    # 遊戲頁
    'game': 'img/backpage.png',
    # 讀取中
    'loading': 'img/loading.png',
  }

  # 是否在地圖頁
  # 是否在遊戲中
  for key, value in d.items():
    location = pyautogui.locateOnScreen(value, grayscale=True, confidence=0.65)
    if (location is not None):
      print("found " + key)
      return key
  print("found reload")
  return 'reload'

def inMapSelectHero():
  # 點上箭頭
  moveAndClick('img/up_arrow.png')
  # 點英雄
  moveAndClick('img/hero2.png')
  # 英雄工作
  work()
  # 點下箭頭
  pyautogui.click() 


# 叫起來工作
def work():
  if whereAmI() != 'character':
    print(whereAmI())
    return False

  for i in range(0, 6):
    if dragTo('img/avatar_sidebar.png', 'img/character.png'):
      continue
    elif dragTo('img/avatar_sidebar.png', 'img/character_202202.png'):
      continue

  count=0
  while moveAndClickCustom('img/not_work.png', 40, 10) == True and count <= 200:
    count+=1
    time.sleep(0.1)

  if count >= 200:
    forceReload()

  moveAndClick('img/close.png')

  return True

def forceReload():
  pyautogui.keyDown('ctrlleft');
  pyautogui.press('f5');
  pyautogui.keyUp('ctrlleft')

def login():
  moveAndClick('img/connect_wallet.png')
  # 等待
  time.sleep(5)
  for i in range(0, 5):
    if moveAndClick('img/sign.png') == True:
      return True
    if moveAndClick('img/sign_chrome.png') == True:
      return True
    print("尋找簽證")
    time.sleep(2)
  
  return False

def back():
  moveAndClick('img/backpage.png')
  if whereAmI() != 'map':
    return False

  time.sleep(1)

  moveAndClick('img/map.png')
  if whereAmI() != 'game':
    return False
  
  return True

printSleep("即將開始執行", 3)

count=0

while True:

  where=whereAmI()
  print('here ' + where)
  # 登入
  if (where == 'login'):
    print("[登入頁]")
    if (login() == False):
      print("登入失敗")
      forceReload()

  while where == 'loading':
    print("[讀取中]")
    time.sleep(2)
    where=whereAmI()

  # 進地圖選英雄工作
  if where == 'map':
    print("[地圖頁]")
    moveAndClick('img/hero.png')
    if (work() == False):
      print("選擇英雄工作失敗")
      forceReload()
    moveAndClick('img/map.png')

  # 遊戲中等待  
  while where == 'game':
    print("[遊戲頁]")
    if (count >= 30):
      moveAndClick('img/backpage.png')
      count=0
      break

    printSleep("[" + str(count) + "] 休息中", random.randint(60-20, 60+20))
    back()
    count+=1

    where=whereAmI()

  if where == 'reload':
    print("[未知錯誤]")
    forceReload()

  if where == 'error':
    print("[發生錯誤]")
    moveAndClick('img/error.png')
    forceReload()

  if where == 'character':
    work()
    moveAndClick('img/map.png')
    pyautogui.click() 

  if where == 'new':
    print('[換新地圖]')
    moveAndClick('img/new_map.png')

  printSleep("等待", 25)