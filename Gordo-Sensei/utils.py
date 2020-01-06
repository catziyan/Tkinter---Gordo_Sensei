#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# Author:CatZiyan
# @Time :2019/12/6 11:00
import time
import datetime
import matplotlib.pyplot as plt
import numpy as np
def get_lines(file):
    file_path = ('./data/'+file+'.txt')
    today = open(file_path, 'r')
    lines = today.readlines()
    today.close()
    return  lines


## 显示学习内容函数
def study_contxt(time_now):
    lines = get_lines('today')
    context = []
    today_flag = False
    for i in range(len(lines)):
        line = lines[i]
        data = line.split()

        if today_flag == True:
            if data[0].isdigit()==True:
                return context
            context.append(data[0])

        if data[0]==time_now:
            today_flag = True
    return context

## 插入学习内容函数
def insert_contxt(time_now,item):
    lines = get_lines('today')
    for i in range(len(lines)):
        line = lines[i]
        if line[:-1] == time_now:
            today_flag = True
            break
        else:
            today_flag = False

    if today_flag==False:
        i = i+1
        lines.insert(i,time_now+'\n')
    lines.insert(i+1,item+' '+'未插入'+' '+'未插入'+' '+'False'+  '\n',)
    today_write = open('./data/today.txt', 'w')
    today_write.writelines(lines)
    today_write.close()


##删除学习内容函数
def delete_contxt(time_now,value):
    delete_flag = False
    re_context = []
    lines = get_lines('today')
    for i in range(len(lines)):
        line = lines[i]
        data = line.split()
        if delete_flag == True:
            if data[0].isdigit() == True:
                break
            if data[0] != value:
                re_context.append(data[0])
            else:
                delete_row = i


        if data[0] == time_now:
            delete_flag = True

    lines[delete_row] = ''
    re_write = open('./data/today.txt', 'w+')
    lines = re_write.writelines(lines)
    re_write.close()
    return  re_context

##插入学习预计时间
def insert_preTime(value,item,time_now,pre_or_done):
    flag = False
    lines = get_lines('today')
    for i in range(len(lines)):
        line = lines[i]
        data = line.split()
        if data[0] == value and flag==True:
            row = i
            if pre_or_done==1:
                row_item = (data[0] + ' ' +item + ' ' + data[2]+' '+'False' + '\n')
            if pre_or_done==2:
                row_item = (data[0] + ' ' +data[1] + ' ' + item +' '+'True' + '\n')
            break
        if data[0] == time_now:
            flag = True
    lines[row] = row_item
    re_write = open('./data/today.txt', 'w+')
    lines = re_write.writelines(lines)
    re_write.close()

def is_done(done,value,time_now):
    lines = get_lines('today')
    flag = False
    for i in range(len(lines)):
        line = lines[i]
        data = line.split()
        if data[0] == value and flag==True:
            row = i
            if done=='True':
                row_item2 = (data[0] + ' ' +data[1] + ' ' + data[2] +' '+'True'+ '\n')
            if done=='False':
                row_item2 = (data[0] + ' ' +data[1] + ' ' + '0' +' '+'False'+ '\n')
            break
        if data[0] == time_now:
            flag = True

    lines[row] = row_item2
    re_write = open('./data/today.txt', 'w+')
    lines = re_write.writelines(lines)
    re_write.close()


def draw_picture(this_week_start,num_day):
    count = 0
    flag = False
    lines = get_lines('today')
    true_now = datetime.datetime.now()
    # this_week_start = now - datetime.timedelta(days=now.weekday())
    day = []
    day_picture = []
    for i in range(num_day):
        if true_now>=(this_week_start + datetime.timedelta(days=i)):
            day_picture.append((this_week_start + datetime.timedelta(days=i)).strftime('%m-%d'))
            day.append((this_week_start + datetime.timedelta(days=i)).strftime('%y%m%d'))

    num = len(day)
    is_done =  ['×']*num
    pre_time = [0]*num
    true_time = [0]*num
    faild  = False
    for i in range(len(lines)):
        line = lines[i]
        data = line.split()

        if flag == True:
            if len(data)>2:
                if data[1].isdigit():
                    pre_time[ID] = pre_time[ID] + int(data[1])
                if data[2].isdigit():
                    true_time[ID] = true_time[ID] + int(data[2])
                    if faild == False:
                        is_done[ID] = '√'
                if data[3] == 'False':
                    is_done[ID] = '×'
                    faild = True

            else:
                flag = False

        if data[0] in day:
            if count>num:
                break
            ID = day.index(data[0])
            pre_time[ID]=0
            flag = True
            faild = False


    # print(pre_time,true_time)
    X = np.arange(num)
    # p1=plt.bar(X, pre_time, color='#9999ff', edgecolor='white',width=0.3)
    # p2= plt.bar(X + 0.3, true_time, color='#ff9999', edgecolor='white', alpha=0.5, width=0.3)
    # for i in range(7):
    #     plt.text(X[i],max(pre_time[i],true_time[i])+10,is_done[i])
    # plt.ylabel('time(min)')
    # plt.xlabel('date')
    # plt.title('Total study time per week')
    # plt.xticks(X, day_picture)
    # plt.legend((p1[0], p2[0]), ('scheduled time', 'actual time'))
    # plt.show()
    return X,pre_time,true_time,day_picture,is_done


def get_all_data():
    today_delete = open('./data/today.txt', 'r')
    lines = today_delete.readlines()
    today_delete.close()
    DATE = []
    for i in range(len(lines)):
        line = lines[i]
        data = line.split()
        if data[0].isdigit():
            DATE.append(int(data[0]))
    time_start = datetime.datetime.strptime(str(min(DATE)), '%y%m%d')
    time_end = datetime.datetime.strptime(str(max(DATE)), '%y%m%d')
    Days = (time_end - time_start).days
    # days  =0
    return time_start,time_end,Days

# print(get_all_data())