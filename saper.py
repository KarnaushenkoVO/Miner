#!/usr/bin/env python3

from tkinter import *
from tkinter import messagebox
import random,time,sys,os
import shelve

EmptySquares = {}
Mine_Objects = []
unflag = 99
has_been_closed = []

win = Tk()
win.title('Сапер')
os.chdir(os.path.dirname(__file__))
icon = PhotoImage(file = '548591.gif')
win.tk.call('wm', 'iconphoto',win._w, icon)
win['bg']="white"
win.resizable(width=False, height=False)
w = 600
h = 450
ws = win.winfo_screenwidth() 
hs = win.winfo_screenheight() 
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
win.geometry('%dx%d+%d+%d' % (w, h, x, y))
panel = Frame(win, height = 50, bg="white")
    
bomb_cnt = Label(panel,text=str(unflag), font=("Helvetica", 16),bg = "white")
bomb_cnt.pack(side=LEFT, padx=50, pady=10)
game_name = Label(panel,text='Сапер!', font=("Helvetica", 16), bg="white")
game_name.pack(side=LEFT, padx=130, pady=10)
time_cnt = Label(panel,text=str(0), font=("Helvetica", 16),bg = "white")
time_cnt.pack(side=LEFT, padx=50, pady=10)
panel.pack(side=TOP, fill=BOTH, expand=YES)
Canv = Canvas(win,height=320, width=600)
quiter = Button(win,text="Вийти",bg="white",bd=0, font=("Helvetica",14),command =lambda zero=0: sys.exit(zero))
quiter.pack(side=BOTTOM,fill=X,pady=0)
new_game = Button(win, text="Нова гра" , bg="white",bd=0,font=("Helvetica",14),command = lambda x=win,y=Canv: New_game(x,y))
new_game.pack(side=BOTTOM, fill=X,pady=0)
Canv.pack(side=TOP, fill=BOTH, expand=YES)
menus = Menu(win, bg="white")
win.config(menu=menus)


def Rules():
    Rule = Toplevel()
    w=350
    h=150
    x = win.winfo_rootx() + 180
    y = win.winfo_rooty() + 70
    Rule.geometry('%dx%d+%d+%d' % (w, h, x, y))
    rule_text = Label(Rule,text="Гравець відкриває комірки, намагаясь не відкрити\n комірку з міною. Якщо комірка містить число, то воно\n показує, скільки мін знаходиться навколо цієї комірки. " ,font=("Helvetica", 10))
    rule_text.pack(side=TOP, fill=BOTH, expand=YES)
    oker = Button(Rule, text='Ok',font=("Helvetica",14), command = Rule.destroy)
    oker.pack(expand=YES,padx=30,pady=10)

def Author():
    Auth = Toplevel()
    w=400
    h=200
    x = win.winfo_rootx() + 180
    y = win.winfo_rooty() + 70
    Auth.geometry('%dx%d+%d+%d' % (w, h, x, y))
    auth_text = Label(Auth,text="Автор гри: Карнаушенко Владислав\n Email:KarnaushenkoVO@gmail.com", font=("Helvetica", 14))
    auth_text.pack(side=TOP, fill=BOTH, expand=YES)
    oker = Button(Auth, text='Ok',font=("Helvetica",14), command = Auth.destroy)
    oker.pack(side=LEFT,padx=30,pady=10)

def ShowRecords():
    try:
        dbase = shelve.open('Records')
    except:
        print('no')
    results = [int(x) for x in dbase.keys()]
    results.sort()
    Rec = Toplevel()
    w=400
    h=200
    x = win.winfo_rootx() + 180
    y = win.winfo_rooty() + 70
    Rec.geometry('%dx%d+%d+%d' % (w, h, x, y))
    rec_text = Label(Rec, text = "Найкращі результати:" , font = ("Helvetica",18))
    rec_text.pack(side=TOP,expand=YES,fill=BOTH)
    if len(results) > 0:
        i = 1
        for res in results:
            text = "%d. %s ----- %d" % (i, dbase[str(res)],res)  
            Label(Rec,text = text,font = ("Helvetica",14)).pack(side=TOP)
    dbase.close()
    oker = Button(Rec, text='Ok',font=("Helvetica",14), command = Rec.destroy)
    oker.pack(side=BOTTOM)              
                 
                 
        
    


file = Menu(menus, tearoff=False, bg="white")
file.add_command(label="Нова гра", command = lambda x=win,y=Canv: New_game(x,y))
file.add_command(label="Рекорди", command = ShowRecords)
file.add_command(label="Вийти", command = lambda zero=0: sys.exit(zero))
menus.add_cascade(label="Файл", menu=file)
helper = Menu(menus, tearoff=False, bg="white")
helper.add_command(label="Правила гри", command = Rules)
helper.add_command(label="Автор", command = Author)
menus.add_cascade(label="Допомога", menu=helper)



def Factory(win,canv):
    Mines = Destiny()
    index = []
    global Mine_Objects
    global EmptySquares
    global unflag
    unflag = 99
    chg_lab(unflag)
    EmptySquares = {}
    Mine_Objects = []
    square_size = 20
    for i in range(30):
        for j in range(16):
            if (i,j) in Mines:
                Mine_Objects.append(Mine(square_size*i,square_size*j,canv))
            else:
                index = (i,j) 
                EmptySquares[index] = EmptySquare(square_size*i,square_size*j,canv,Mines)
    Scanning(EmptySquares,Mines)
    win.mainloop()        

def check_finish(func):
    def wrapper(self,*args):
        global EmptySquares, Mine_Objects
        if len(has_been_closed) + 1 == len(EmptySquares):
            Storage()
            timer.stop_it()
            Canv.itemconfig(self.id, fill = "black")
            Warn = Toplevel()
            Warn.geometry('370x140')
            warning = Label(Warn,text="Вітаємо з перемогою!!\n Ваш час: %dc" % (timer.time), font=("Helvetica", 24))
            warning.pack(side=TOP, fill=BOTH, expand=YES)
            ok = Button(Warn, text='Ok',font=("Helvetica",14), command = Warn.destroy)
            ok.pack(side=LEFT,padx=30,pady=10)
            new_game = Button(Warn, text="Нова гра" , font=("Helvetica",14),command = lambda x=win,y=Canv,Frm=Warn: New_game(x,y,frm=Frm))
            new_game.pack(side=RIGHT,padx=30,pady=10)
            for key in EmptySquares.keys():
                EmptySquares[key].clickable = False
            for obj in Mine_Objects:
                obj.clickable = False
        else:
                func(self,*args)
    return wrapper
        
    
def Storage():
    result_time = timer.time
    dbase = shelve.open('Records')
    minimum = min(list(int(dbase.keys)))
    if result_time > minimum:
        ask_name= Toplevel()
        ask_name.geometry('370x140')
        ask_label = Label(ask_name,text = "Введіть ваше ім'я:", font = ("Helvetica",24))
        ask_label.pack(side=TOP,fill=BOTH,expand=YES)
        ask = Entry(ask_name, font=("Helvetica",16))
        ask.pack(side=TOP, expand=YES)
        ask_ok = Button(ask_name, text= "Ок", font = ("Helvetica",14), command = ask_name.destroy)
        ask_ok.pack(side=BOTTOM)
        if len(dbase) == 3:
            del dbase[str(minimum)]
        dbase[str(result_time)] = ask
    dbase.close()
  
                

class GameObject():
    def __init__(self,x,y,canv,Mines=[]):
        self.Mines = Mines
        self.x = x
        self.y = y
        self.canv = canv
        self.mark = False
        self.clickable = True
        self.id = canv.create_rectangle(x,y,x+20,y+20,width=1,outline='grey98', fill="grey", tags="unknown")
        self.canv.tag_bind(self.id, '<ButtonPress-3>', self.Marked)


    def Marked(self, *args):
        global unflag
        if self.mark == False:
            self.mark = True
            self.canv.itemconfig(self.id, fill = "tomato2", outline='grey40')
            unflag -= 1
        else:
            self.mark = False
            self.canv.itemconfig(self.id, fill = "grey", outline = 'grey98')
            unflag += 1
        chg_lab(unflag)
        
            

class EmptySquare(GameObject):
    def __init__(self,x,y,canv,Mines=[]):
        GameObject.__init__(self,x,y,canv,Mines)
        self.canv.itemconfig(self.id, tags = "EmptySquare" )
        self.canv.tag_bind(self.id, '<ButtonPress-1>', self.OnEmptyClick)
        self.has_been_clicked = False
        self.bombs=0

    @check_finish
    def OnEmptyClick(self,*args):
        global has_been_closed
        global unflag
        if self.clickable == True:
            if self.mark == False:
                if self.has_been_clicked == False:
                    self.has_been_clicked = True
                    has_been_closed.append(self)
                    self.canv.itemconfig(self.id, fill='floral white', outline='grey40')
                    self.lab = Label(self.canv, bg='floral white')
                    if self.bombs != 0:
                        self.lab.config(text = str(self.bombs))
                        self.win_id = self.canv.create_window(self.x+10, self.y+10,width=19,height=19, window=self.lab)
                        self.lab.bind('<ButtonPress-2>', self.Around)
                    else:
                        self.SelfClicking()


    def SelfClicking(self):
        for i in (-1,0,1):
            for j in (-1,0,1):
                if (i != 0 or j != i):
                    a = self.x/20 + i
                    b = self.y/20 + j
                    if ((a,b) in EmptySquares.keys() and EmptySquares[(a,b)].has_been_clicked == False):
                        EmptySquares[(a,b)].OnEmptyClick()
                        

    def Around(self,*args):
        if self.has_been_clicked == True:
            num = 0
            not_mark = []
            not_markb = []
            for i in (-1,0,1):
                for j in (-1,0,1):
                    if (i != 0 or j != i):
                        a = self.x/20 + i
                        b = self.y/20 + j
                        if (a,b) in EmptySquares.keys():
                            if EmptySquares[(a,b)].mark == True:
                                if EmptySquares[(a,b)].has_been_clicked == False:
                                    num += 1
                            else:
                                if EmptySquares[(a,b)].has_been_clicked == False:
                                    not_mark.append(EmptySquares[(a,b)])
                        for mine_obj in Mine_Objects:
                            if mine_obj.x/20 == a and mine_obj.y/20 == b:
                                if mine_obj.mark == True:
                                    num += 1
                                else:
                                    not_markb.append(mine_obj)
            if num == self.bombs:
                for sqr in not_mark:
                    sqr.OnEmptyClick()
                for mine in not_markb:
                    mine.Boom()
            else:
                for sqr in not_mark:
                    sqr.canv.itemconfig(sqr.id,tags="blink")
                for mine in not_markb:
                    mine.canv.itemconfig(mine.id,tags="blink")
                self.canv.itemconfig("blink", fill='gold')
                self.canv.update()
                time.sleep(0.3)
                self.canv.itemconfig("blink", fill='grey')
                all_obj = not_markb + not_mark
                for x in all_obj:
                    x.canv.itemconfig(x.id, tags="unknown")
                        
                        
     
        
    
class Mine(GameObject):
    def __init__(self,x,y,canv,Mines=[]):
        GameObject.__init__(self,x,y,canv,Mines)
        self.canv.itemconfig(self.id, tags = "Mine")
        self.canv.tag_bind(self.id, '<ButtonPress-1>', self.Boom )
        
    def Boom(self,*args):
        if self.clickable == True:
            if self.mark == False:
                timer.stop_it()
                self.canv.itemconfig(self.id, fill = "black")
                global EmptySquares, Mine_Objects
                Warn = Toplevel()
                w=270
                h=140
                x = win.winfo_rootx() + 180
                y = win.winfo_rooty() + 70
                Warn.geometry('%dx%d+%d+%d' % (w, h, x, y))
                warning = Label(Warn,text="Ви програли!\n Ваш час: %dc" % (timer.time), font=("Helvetica", 24))
                warning.pack(side=TOP, fill=BOTH, expand=YES)
                ok = Button(Warn, text='Ok',font=("Helvetica",14), command = Warn.destroy)
                ok.pack(side=LEFT,padx=30,pady=10)
                new_game = Button(Warn, text="Нова гра" , font=("Helvetica",14),command = lambda x=self.canv.master,y=self.canv,Frm=Warn: New_game(x,y,frm=Frm))
                new_game.pack(side=RIGHT,padx=30,pady=10)
                for key in EmptySquares.keys():
                    EmptySquares[key].clickable = False
                for obj in Mine_Objects:
                    obj.clickable = False
                

def Scanning(ESquares,Mines):
    for square in ESquares.keys():
        for i in (-1,0,1):
            for j in (-1,0,1):
                    if (ESquares[square].x/20+i,ESquares[square].y/20+j) in Mines:
                        ESquares[square].bombs += 1
    for square in ESquares.keys():
        if ESquares[square].bombs  == 0:
            ESquares[square].OnEmptyClick()
            break
    
def New_game(win,Canv,frm=0):
    global has_been_closed
    has_been_closed = []
    timer.stop_it()
    timer.restart()
    if frm != 0:
        frm.destroy()
    Canv.delete('all')
    Factory(win,Canv)



def Destiny():
    Mines = []
    while len(Mines) < 99:
        b = random.randint(0,15)
        a = random.randint(0,29)
        if (a,b) not in Mines:
            Mines.append((a,b))
    return Mines



def chg_lab(unflags):
    bomb_cnt.config(text=str(unflags))
    
class chg_time_cnt():
    def __init__(self):
        self.time = 0
        self.stop = False
        self.timer()

    def timer(self):
        if self.stop == False:
            self.time += 1
            time_cnt.config(text=str(self.time))
            self._job = time_cnt.after(1000,self.timer)
        else:
            return
        
    def stop_it(self):
        time_cnt.after_cancel(self._job)

    def restart(self):
        self.stop = False
        self.time = 0
        self.timer()
        

if __name__ == "__main__":
    random.seed(time.time())
    timer = chg_time_cnt()
    Factory(win,Canv)
