#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Author:CatZiyan
# @Time :2019/12/2 21:42
import time
import tkinter as tk
import sys
from  tkinter import ttk  #导入内部包
from utils import *
import datetime
from clock import Calendar
import calendar
from dateutil.relativedelta import relativedelta
import tkinter.messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
time_now = time.strftime('%y%m%d')
# plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
# plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

## listbox双击关联事件---显示预计时间
def CallOn(v,a):
    flag = False
    item = lb.get(lb.curselection())
    lines = get_lines('today')
    for i in range(len(lines)):
        line = lines[i]
        data = line.split()
        if flag==True and data[0]==item:
            if a==1:
                if data[1] != '未插入':
                    var1.set('预计完成 '+item+' 任务需要'+data[1]+'分钟')
                    return
                else:
                    var1.set('还未插入预计时间')
            if a==2:
                if data[2].isdigit() and data[2]!='0':
                    var1.set('完成 '+item+' 任务用了'+data[2]+'分钟')
                    r1.select()
                    return
                if data[3] == 'False'and data[2]!='未插入':
                    var1.set('未完成任务！')
                    r2.select()
                    return
                if data[2]=='未插入':
                    var1.set('还未插入完成时间')
                    return
        if data[0] == time_now:
            flag = True


window =  tk.Tk()
window.withdraw()
window.title('戈多Sensei')
window.iconbitmap('star.ico')
# window.resizable(False,True)
bg = window.cget("background")


l3 = tk.Label(window,text='',pady=10)
l3.pack()

fram_1 = tk.Frame(window,width=300,height=50)
fram_1.pack_propagate(0)
fram_1.pack()

def updata_time():
    now = time.strftime("%H:%M:%S")
    l3.configure(text=now)
    window.after(1000,updata_time)
updata_time()
fram_11 = tk.Frame(fram_1,width=150,height=50)
fram_11.pack_propagate(0)
fram_12 = tk.Frame(fram_1)
fram_11.pack(side='left')
fram_12.pack(side='right')
e = tk.Entry(fram_12,show=None)
e.pack()


fram_2 = tk.Frame(window,width=300,height=150,pady=30)
fram_2.pack()
fram_2.pack_propagate(0)
var1 = tk.StringVar()
var1.set('预计时间')
l1 = tk.Label(fram_2,textvariable = var1,font=('宋体',11),wraplength = 300,justify = 'center')

l1.pack()
fram_21 = tk.Frame(fram_2,width=150,height=50)
fram_21.pack_propagate(0)
fram_22 = tk.Frame(fram_2,width=150,height=50)
fram_22.pack_propagate(0)
fram_21.pack(side='left')
fram_22.pack(side='right')
e2 = tk.Entry(fram_22,show=None)
e2.pack(side='left')

fram_3 = tk.LabelFrame(window,width=350,height=200,text='任务列表')
# fram_3.place(x=10,y=200,anchor='nw')
fram_3.pack()
fram_3.pack_propagate(0)
var3 = tk.StringVar()
var3.set('')
l = tk.Label(fram_3,textvariable = var3 ,font=('宋体',11))
l.pack()
fram_31 = tk.Frame(fram_3,width=200,height=150)
fram_31.pack_propagate(0)
fram_32 = tk.Frame(fram_3,width=150,height=150)
fram_32.pack_propagate(0)
fram_31.pack(side='left')
fram_32.pack(side='right')

def handlerAdaptor(fun, **kwds):
    '''事件处理函数的适配器，相当于中介，那个event是从那里来的呢，我也纳闷，这也许就是python的伟大之处吧'''
    return lambda event,fun=fun,kwds=kwds: fun(event, **kwds)

# 创建Scrollbar
scrolly = tk.Scrollbar(fram_31)
scrolly.pack(side=tk.RIGHT,fill=tk.Y)
scrollx = tk.Scrollbar(fram_31,orient=tk.HORIZONTAL)
scrollx.pack(side=tk.BOTTOM,fill=tk.X,anchor=tk.S)
var = tk.StringVar()
var.set(study_contxt(time_now))
lb = tk.Listbox(fram_31,listvariable=var,yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
lb.bind('<Double-1>', handlerAdaptor(CallOn,a=1))
# lb.pack(fill=tk.BOTH,expand=tk.YES)
lb.pack()
scrolly.config(command=lb.yview)
scrollx.config(command=lb.xview)
## 插入学习内容回调函数
def inset_end():
    item = e.get()
    if item == '':
        tk.messagebox.showerror(title='傻子', message='不要插入空白任务')
        return
    if item in var.get():
        tk.messagebox.showerror(title='傻子', message='学习内容已存在')
        e.delete(0, 'end')
        return
    insert_contxt(time_now,item)
    lb.insert('end',item)
    e.delete(0, 'end')

b = tk.Button(fram_11,text = '插入学习内容',width = 15, height=2, command = inset_end)
b.pack(side='left')


## 删除学习内容回调函数
def delete_point():
    if lb.curselection() != ():
        value = lb.get(lb.curselection())
    else:
        tk.messagebox.showerror(title='傻子', message='请先选择一项内容')
        return
    re_context = delete_contxt(time_now,value)
    var.set(re_context)

b2 =tk.Button(fram_32,text = '删除学习内容',width = 15, height = 1, command =delete_point)
b2.pack()


#插入学习预计时间回调函数
def insert_pre(pre_or_done):
    if lb.curselection() != ():
        value = lb.get(lb.curselection())
    else:
        tk.messagebox.showerror(title='傻子', message='请先选择一项内容')
        return
    item = e2.get()

    if item.isdigit() == False:
        tk.messagebox.showerror(title='傻子', message='请正确插入时间（数字）')
        return
    e2.delete(0, 'end')
    if pre_or_done==1:
        var1.set('预计完成 '+value+' 任务需要'+item+'分钟')
        insert_preTime(value,item,time_now,pre_or_done)
    if pre_or_done==2:
        var1.set('完成 '+value+' 任务用了'+item+'分钟')
        insert_preTime(value,item,time_now,pre_or_done)

    lb.select_set(lb.curselection()[0]+1)
    lb.select_clear(lb.curselection()[0])


b3 = tk.Button(fram_21,text = '插入预计时间(min)',width=15, height=2, command = lambda :insert_pre(1))
b3.pack(side = 'left')


def print_con(v):
    global l2,s1,s2,s3,var3,time_now
    year = str(s1.get())
    if s2.get()<10:
        mouth=('0'+str(s2.get()))
    else:
        mouth = str(s2.get())
    if s3.get()<10:
        day = ('0'+str(s3.get()))
    else:
        day = str(s3.get())

    l2.config(text=year+'年'+mouth+'月'+day+'日')
    var3.set(year+'年'+mouth+'月'+day+'日')
    time_now =(year+mouth+day)
    var.set(study_contxt(time_now))




def up_day(day):
    global time_now
    timehehe = datetime.datetime.strptime(time_now, '%y%m%d')
    time_now=(timehehe + datetime.timedelta(days=day)).strftime('%y%m%d')
    var.set(study_contxt(time_now))
    var3.set(time_now[0:2] + '年' + time_now[2:4] + '月' + time_now[4:6] + '日')
b4=tk.Button(fram_32,text= '后一天',width = 15, height = 1, command = lambda:up_day(1))
b4.pack()
b5=tk.Button(fram_32,text= '前一天',width = 15, height = 1, command = lambda:up_day(-1))
b5.pack()

width, height =  50, 50  # 窗口大小
x, y = (window.winfo_screenwidth()- width) / 2, (window.winfo_screenheight() - height) / 2
# Calendar((x, y), 'ur').selection() 获取日期，x,y为点坐标

def date_str_gain():
    global time_now
    for date in [Calendar(point=(x+160, y), position='lr').selection()]:
        if date:
            time_now =date[2:4]+date[5:7]+date[8:10]
            var3.set(time_now[0:2] + '年' + time_now[2:4] + '月' + time_now[4:6] + '日')
            var.set(study_contxt(time_now))

b6=tk.Button(fram_32, text='选择日期', width = 15, height = 1, command=date_str_gain).pack()



var4 = tk.StringVar()
fram_4 = tk.Frame(window,width=300,height=50)
fram_4.pack_propagate(0)

def print_selection():
    if lb.curselection() != ():
        value = lb.get(lb.curselection())
    else:
        tk.messagebox.showerror(title='傻子', message='请先选择一项内容')
        return
    done = var4.get()
    is_done(done,value,time_now)




r1 = tk.Radiobutton(fram_4,text='完成',variable = var4,value='True',command = print_selection, cursor="hand2", font=("宋体 14 bold "))
r1.pack(side='left')
r2 = tk.Radiobutton(fram_4,text='未完成',variable = var4,value='False',command = print_selection, cursor="hand2",indicatoron=True,font=("宋体 14 bold "))
r2.pack(side = 'right')
var4.set('初始化')

menubar = tk.Menu(window)
def doing():
    fram_2.pack_forget()
    fram_3.pack_forget()
    fram_4.pack_forget()
    fram_5.pack_forget()
    fram_6.pack_forget()
    fram_7.pack_forget()
    fram_1.pack()
    fram_2.pack()
    fram_3.pack()
    var1.set('预计时间')
    b3.configure(text = '插入预计时间(min)',command=lambda: insert_pre(1))
    lb.bind('<Double-1>', handlerAdaptor(CallOn, a=1))
    l3.configure(background = bg)
    window.configure(background = bg)

def done():
    fram_1.pack_forget()
    fram_2.pack_forget()
    fram_3.pack_forget()
    fram_5.pack_forget()
    fram_6.pack_forget()
    fram_7.pack_forget()
    fram_4.pack()
    fram_2.pack()
    fram_3.pack()
    l3.configure(background = bg)
    window.configure(background = bg)
    # b3 = tk.Button(fram_21, text='插入预计时间(min)', width=15, height=2, command=lambda: insert_pre(1))
    b3.configure(text = '插入完成时间(min)',command=lambda: insert_pre(2))
    var1.set('完成时间')
    lb.bind('<Double-1>', handlerAdaptor(CallOn, a=2))



def re_view():
    fram_1.pack_forget()
    fram_2.pack_forget()
    fram_3.pack_forget()
    fram_4.pack_forget()
    fram_7.pack_forget()
    fram_5.pack()
    fram_6.pack_forget()
    f_plot.clear()
    l3.configure(background = 'white')
    window.configure(background = 'white')
    time_start, time_end, Days = get_all_data()
    X, pre_time, true_time, day_picture, pp = draw_picture(time_start, Days)

    Type1_x = []
    Type1_y = []
    Type2_y = []
    Type2_x = []
    for i in range(len(day_picture)):
        if pp[i] == '√':
            Type1_x.append(X[i])
            Type1_y.append(true_time[i])
        else:
            Type2_x.append(X[i])
            Type2_y.append(true_time[i])
    type1=f_plot.scatter(Type1_x,Type1_y,c='gold',marker='*',s=150,edgecolors='black',linewidths=0.5,zorder=2)
    type2 = f_plot.scatter(Type2_x,Type2_y,c='red',marker='o',zorder=2)
    p1=f_plot.plot(X, pre_time, color='#9999ff',zorder=1)
    p2= f_plot.plot(X , true_time, color='#ff9999',zorder=1)
    f_plot.set_ylabel('time(min)')
    f_plot.set_xlabel('date')
    f_plot.set_title('Total study time')
    show = []
    XX = []
    for i in range(len(day_picture)):
        if len(day_picture)>7:
            if i%2==0:
                XX.append(X[i])
                shows = day_picture[i]
                show.append(shows)
        else:
            XX.append(X[i])
            shows = day_picture[i]
            show.append(shows)
    ticks = f_plot.set_xticks(XX)
    f_plot.set_xticklabels(show)
    f_plot.legend((p1[0], p2[0],type1,type2), ('scheduled time', 'actual time','success','fail'))
    canvs.draw()

global NOW
NOW = 0
def re_view_week(count):
    global NOW
    NOW = NOW+count
    if NOW<0:
        b7.configure(state = 'normal')
    else:
        b7.configure(state = 'disable')
    fram_1.pack_forget()
    fram_2.pack_forget()
    fram_3.pack_forget()
    fram_4.pack_forget()
    fram_7.pack_forget()
    fram_5.pack()
    fram_6.pack()
    l3.configure(background = 'white')
    window.configure(background = 'white')
    f_plot.clear()
    now = datetime.datetime.now()
    now = now+datetime.timedelta(days=7*NOW)
    this_week_end = now + datetime.timedelta(days=6 - now.weekday())
    this_week_start = now - datetime.timedelta(days=now.weekday())
    # print((this_week_end-last_week_start).days)
    X,pre_time,true_time,day_picture,pp=draw_picture(this_week_start,(this_week_end-this_week_start).days)
    p1=f_plot.bar(X, pre_time, color='#9999ff', edgecolor='white',width=0.3)
    p2= f_plot.bar(X + 0.3, true_time, color='#ff9999', edgecolor='white', alpha=0.5, width=0.3)

    for i in range(len(day_picture)):
        f_plot.text(X[i],max(pre_time[i],true_time[i])+10,pp[i])
    f_plot.set_ylabel('time(min)')
    f_plot.set_xlabel('date')
    f_plot.set_title('Total study time per week')
    ticks = f_plot.set_xticks(X)
    f_plot.set_xticklabels(day_picture)
    f_plot.legend((p1[0], p2[0]), ('scheduled time', 'actual time'))
    canvs.draw()



def Score():
    global time_now,window2

    lines = get_lines('today')
    flag = False
    task = []
    S_time = []
    A_time = []
    for i in range(len(lines)):
        line = lines[i]
        data = line.split()
        if flag == True:

            if data[0].isdigit()== False:
                task.append(data[0])
                if data[1].isdigit() == False:
                    tk.messagebox.showerror(title='傻子', message='请先插入 '+ data[0] + '的预计时间')
                    return
                else:
                    S_time.append(int(data[1]))
                if data[2].isdigit() == False:
                    tk.messagebox.showerror(title='傻子', message='请先插入 '+ data[0] + '的完成时间')
                    return
                else:
                    A_time.append(int(data[2]))
            else:
                break
        if data[0]==time_now:

            flag = True
    # print(task,S_time,A_time,sum(S_time))
    sum_S_time = sum(S_time)

    window2 = tk.Tk()
    window2.configure(background='white')
    window2.title('戈多Sensei-得分细则')
    ww = 500
    wh = 400
    window2.geometry("%dx%d+%d+%d" % (ww, wh, (sw - ww) / 2, (sh - wh) / 2))
    # window2.geometry('500x400')
    window2.iconbitmap('star.ico')



    l4 = tk.Label(window2,text = (time_now[0:2]+'年'+time_now[2:4]+'月'+time_now[4:6]+'日'),pady=20,background='white')
    l4.pack()

    tree = ttk.Treeview(window2, columns=['1', '2', '3','4'], show='headings')
    tree.column('1', width=230, anchor='center')
    tree.column('2', width=90, anchor='center')
    tree.column('3',width=90, anchor='center')
    tree.column('4',width=90, anchor='center')
    tree.heading('1', text='学习内容')
    tree.heading('2', text='预计时间')
    tree.heading('3', text='实际时间')
    tree.heading('4', text='单项得分')
    total_score = 0
    for i in range(len(task)):
        tree_data = []
        tree_data.append(task[i])
        tree_data.append(str(S_time[i]))
        tree_data.append(str(A_time[i]))
        if A_time[i]==0:
            Ascore = 0
        else:
            Ascore = int(100*(S_time[i]/sum_S_time)*(S_time[i]/A_time[i]))
        total_score = Ascore + total_score
        tree_data.append(str(Ascore))
        tree.insert('', 'end', values=tree_data)
    tree.pack()
    tk.Label(window2,text=('总得分为：'+str(total_score)),pady=10,font = ('宋体',12),background='white').pack()
    b9 = tk.Button(window2, text='刷新', command=Score_again)
    b9.pack()



def Score_again():
    window2.destroy()
    Score()



global NOW_mouth
NOW_mouth = 0
def re_view_mouth(count):
    global NOW_mouth
    NOW_mouth= NOW_mouth+count
    if NOW_mouth<0:
        b8.configure(state = 'normal')
    else:
        b8.configure(state = 'disable')
    fram_1.pack_forget()
    fram_2.pack_forget()
    fram_3.pack_forget()
    fram_4.pack_forget()
    fram_6.pack_forget()
    fram_5.pack()
    fram_7.pack()
    f_plot.clear()
    now = datetime.datetime.now()

    if NOW_mouth <0:
        now = now-relativedelta(months= abs(NOW_mouth))
    else:
        now = now + relativedelta(months=NOW_mouth)
    this_month_start = datetime.datetime(now.year, now.month, 1)
    # print(calendar.monthrange(now.year,now.month)[1])
    X,pre_time,true_time,day_picture,pp=draw_picture(this_month_start,calendar.monthrange(now.year,now.month)[1])
    # print(this_month_start,calendar.monthrange(now.year,now.month)[1])
    # print(X,pre_time,true_time,day_picture,pp)
    Type1_x = []
    Type1_y = []
    Type2_y = []
    Type2_x = []
    for i in range(len(day_picture)):
        if pp[i] == '√':
            Type1_x.append(X[i])
            Type1_y.append(true_time[i])
        else:
            Type2_x.append(X[i])
            Type2_y.append(true_time[i])
    type1=f_plot.scatter(Type1_x,Type1_y,c='gold',marker='*',s=150,edgecolors='black',linewidths=0.5,zorder=2)
    type2 = f_plot.scatter(Type2_x,Type2_y,c='red',marker='o',zorder=2)
    p1=f_plot.plot(X, pre_time, color='#9999ff',zorder=1)
    p2= f_plot.plot(X , true_time, color='#ff9999',zorder=1)
    f_plot.set_ylabel('time(min)')
    f_plot.set_xlabel('date')
    MM = ['Jan.','Feb.','Mar.','Apr.','May.','Jun.','Jul.','Aug.','Sept.','Oct.','Nov.','Dec.']
    f_plot.set_title('Total study time in '+MM[int(now.month)-1])
    show = []
    XX = []
    for i in range(len(day_picture)):
        if len(day_picture)>15:
            if i%2==0:
                XX.append(X[i])
                shows = day_picture[i]
                show.append(shows[-2:])
        else:
            XX.append(X[i])
            shows = day_picture[i]
            show.append(shows[-2:])
    ticks = f_plot.set_xticks(XX)
    f_plot.set_xticklabels(show)
    f_plot.legend((p1[0], p2[0],type1,type2), ('scheduled time', 'actual time','success','fail'))
    canvs.draw()


fram_5 = tk.Frame(window,width=400,height=400,background='white')
fram_5.pack_propagate(0)
f = Figure(figsize=(1, 1), dpi=80)
f_plot = f.add_subplot(111)
canvs = FigureCanvasTkAgg(f, fram_5)
canvs.get_tk_widget().pack(side = 'top',fill='both', expand=1)
toolbar = NavigationToolbar2Tk(canvs, fram_5)
toolbar.configure(background='white')
toolbar.update()
def on_key_event(event):
    print('you press %s' % event.key)
    key_press_handler(event, canvs, toolbar)

canvs.mpl_connect('key_press_event', on_key_event)

fram_6 = tk.Frame(window,width=200,height=50,background='white')
fram_6.pack_propagate(0)
tk.Button(fram_6,text='上一周',command=lambda :re_view_week(count=-1)).pack(side='left')
b7=tk.Button(fram_6,text='下一周',command=lambda :re_view_week(count=1))
b7.pack(side='right')

fram_7 = tk.Frame(window,width=200,height=50)
fram_7.pack_propagate(0)
tk.Button(fram_7,text='上一月',command=lambda :re_view_mouth(count=-1)).pack(side='left')
b8=tk.Button(fram_7,text='下一月',command=lambda :re_view_mouth(count=1))
b8.pack(side='right')

menubar.add_command(label='制定任务',command=doing)
menubar.add_command(label='完成任务',command=done)
# menubar.add_command(label='学习评估',command=re_view)
filemenu  = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='学习评估',menu=filemenu)
filemenu.add_command(label='学习得分',command=Score)

submenu = tk.Menu(filemenu, tearoff=0)
filemenu.add_cascade(label='学习时间评估',menu=submenu,underline=0)
submenu.add_command(label='周',command=lambda :re_view_week(count=0))
submenu.add_command(label='月',command=lambda :re_view_mouth(count=0))
submenu.add_separator()
submenu.add_command(label='全部',command=re_view)

window.config(menu=menubar)

def callbackClose():
    sys.exit(0)

window.protocol("WM_DELETE_WINDOW", callbackClose)
# window.deiconify()
window.withdraw()
sw = window.winfo_screenwidth()
sh = window.winfo_screenheight()
ww = 400
wh = 500
window.geometry("%dx%d+%d+%d" %(ww,wh,(sw-ww) / 2-450,(sh-wh) / 2))
window.deiconify()
if __name__ == '__main__':
    window.mainloop()
