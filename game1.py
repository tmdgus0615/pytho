import random, base64
from tkinter import *
from connectDB import cur, conn
from io import BytesIO
from PIL import Image, ImageTk
from tkinter import messagebox


RAND_COUNTRY_LIST = []
PROBLEM = 0
SCORE = 0
LIFE = 3


## START 화면 구현 ## 
def myFrame():
  score_hp_frame = Frame(root, bg="white")
  score_hp_frame.pack(fill='both')

  second_frame = Frame(root, bg="white")
  second_frame.pack()

  img_frame = Frame(root, bg="white")
  img_frame.pack()

  btn_frame = Frame(root, bg="white")
  btn_frame.pack()
  return score_hp_frame, second_frame, img_frame, btn_frame
  

def myWidget(score_hp_frame, second_frame, img_frame, btn_frame):
  score_lbl_text = StringVar()
  score_lbl_text.set(str(PROBLEM+1) + ' / 10')
  score_lbl = Label(score_hp_frame, textvariable=score_lbl_text, width = 15)
  score_lbl.configure(relief='ridge', height=2)
  score_lbl.configure(font=('굴림', 12, 'bold'))
  score_lbl.pack(side=LEFT, padx = 5, pady = 5)

  hp_img = PhotoImage(file='hp.png')
  hp_lbl = Label(score_hp_frame, image=hp_img, width = 90)
  hp_lbl.configure(relief='ridge')
  hp_lbl.pack(side=RIGHT, padx=5, pady = 5)

  score_board = StringVar()
  score_board.set("점수 :" + str(SCORE))
  second_lbl = Label(second_frame, textvariable=score_board)
  second_lbl.configure(font=('굴림', 20, 'bold'))
  second_lbl.pack()
  
  imgTemp = PhotoImage() #빈이미지
  img_lbl = Label(img_frame, image=imgTemp, bg='yellow')
  img_lbl.configure(width=200, height=200)
  img_lbl.pack(pady=5)  

  btn1 = Button(btn_frame, text="1번", width=12, height=2, command=lambda:btn_click(btn1.cget('text')))
  btn1.grid(row=0, column=0, padx=10, pady=6)
  btn2 = Button(btn_frame, text="2번", width=12, height=2, command=lambda:btn_click(btn2.cget('text')))
  btn2.grid(row=0, column=1, padx=10, pady=6)
  btn3 = Button(btn_frame, text="3번", width=12, height=2, command=lambda:btn_click(btn3.cget('text')))
  btn3.grid(row=1, column=0, padx=10, pady=6)
  btn4 = Button(btn_frame, text="4번", width=12, height=2, command=lambda:btn_click(btn4.cget('text')))
  btn4.grid(row=1, column=1, padx=10, pady=6)
  
  return img_lbl, btn1, btn2, btn3, btn4, hp_img, score_lbl_text, score_board, hp_lbl
## END 화면 구현 ##

## START 문제 리스트 ##
def randCountryList():
  rnd = random.sample(range(1,50), 11)
  
  for r in rnd :
    sql = f'select * from worldPopulation where 순번 = {r}'
    cur.execute(sql)
    RAND_COUNTRY_LIST.append(cur.fetchone())
## END 문제 리스트 ##  

def showImg(PROBLEM):
  if(RAND_COUNTRY_LIST[10][0] == PROBLEM):
    pass
  else:
    sql = f'select * from flag where 순번 = {PROBLEM}'
    cur.execute(sql)
    no, code, img = cur.fetchone()

    if img == None :
      imgTemp = PhotoImage()
      img_lbl.configure(image=imgTemp)
    else:
      img = base64.b64decode(img)
      img = Image.open(BytesIO(img))
      resizedImg = img.resize((200,200))
      resizedImg = ImageTk.PhotoImage(resizedImg)
      img_lbl.configure(image=resizedImg)
      img_lbl.image = resizedImg
  
def btn_click(text) :
  global PROBLEM, SCORE, LIFE, score_lbl_text
  
  PROBLEM = PROBLEM + 1
  
  showImg(RAND_COUNTRY_LIST[PROBLEM][0])
  wrongAnser(PROBLEM)
  print("-----", RAND_COUNTRY_LIST[PROBLEM][2])

  if RAND_COUNTRY_LIST[PROBLEM-1][2] == text and PROBLEM !=11 :
    messagebox.showinfo(str(PROBLEM) + "번 문제", "정답입니다.")
    SCORE = SCORE + 10
    score_board.set("점수 : " + str(SCORE))
  else:
    if PROBLEM != 10 :
      LIFE = LIFE - 1
      messagebox.showinfo(str(PROBLEM) + "번 문제", "오답입니다.")

      if LIFE == 3 :
        hp_img.configure(file='hp.png')
      elif LIFE == 2 :
        hp_img.configure(file='hp1.png')
      elif LIFE == 1 :
        hp_img.configure(file='hp2.png')
      elif LIFE == 0 :
        hp_img.configure(file='hp3.png')

  if PROBLEM == 10:
    PROBLEM = 9
  score_lbl_text.set(str(PROBLEM+1) + ' /10')

  if LIFE == 0 :
    messagebox.showinfo("게임종료", "수고하셨습니다.")
    root.destroy()
    
def wrongAnser(PROBLEM):
  answer = RAND_COUNTRY_LIST[PROBLEM][2]
  wAnser = []
  for wa in RAND_COUNTRY_LIST:
    wAnser.append(wa[2])
  wAnser.remove(answer)
  
  btn1_c, btn2_c, btn3_c, btn4_c = random.sample(wAnser,4)
  btn1.configure(text=btn1_c)
  btn2.configure(text=btn2_c)
  btn3.configure(text=btn3_c)
  btn4.configure(text=btn4_c)
  
  answer_num = random.sample(range(1,4),1)
  print(answer, answer_num)
  if answer_num[0] == 1 :
    btn1.configure(text=answer)
  elif answer_num[0] == 2 :
    btn2.configure(text=answer)
  elif answer_num[0] == 3 :
    btn3.configure(text=answer)
  elif answer_num[0] == 4 :
    btn4.configure(text=answer)    
    

def playGame() :
  randCountryList()
  print(RAND_COUNTRY_LIST)
  showImg(RAND_COUNTRY_LIST[0][0])
  wrongAnser(PROBLEM) 
  
  
  
  
  
root = Tk()
root.title('세계 나라별 국기 퀴즈')
root.geometry('300x400')
root.configure(bg="white")


score_hp_frame, second_frame, img_frame, btn_frame = myFrame()
img_lbl, btn1, btn2, btn3, btn4, hp_img, score_lbl_text, score_board, hp_lbl = myWidget(score_hp_frame, second_frame, img_frame, btn_frame)

playGame()

root.mainloop()
