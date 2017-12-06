# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 13:15:21 2017

@author: Pulu
"""
import numpy as np
import copy
import tkinter as tk
import tkinter.filedialog as tkf
import tkinter.scrolledtext as tks
import os

def read_file(file_path,pic_row,pic_column):
    pic = np.matrix(np.full(pic_row*pic_column,-1))
    pic = pic.reshape([pic_row,pic_column])    
    pics = [copy.deepcopy(pic)]
    row = 0
    pic_num = 0
    training_file = open(file_path,"r")
    for i in training_file.readlines():
        for column in range(len(i)):
            if(i[column] == "1"):
                pics[pic_num][row,column] = 1
        row += 1
        if(pic_row == row-1):
            row = 0
            pics.append(copy.deepcopy(pic))
            pics[pic_num] = pics[pic_num].ravel()
            pic_num += 1 
    pics[len(pics)-1] = pics[len(pics)-1].ravel()
    return pics

def hopfield_memory(pics,pic_row,pic_column):    
    x = np.matrix((pic_row*pic_column)*[(pic_row*pic_column)*[0]])
    y = np.identity(pic_row*pic_column)
    for N in range(len(pics)):
        x = x + pics[N].getT()*pics[N]
    w = (x*(1/len(pics[0].getT()))) - y*(len(pics)/len(pics[0].getT()))
    t = w.sum(axis=1)
    return w,t

def hopfield_test(picture_memory,picture_testing,weights,theta):
    recall_result = [[0,0]]
    for pic_num in range(len(picture_testing)):
        x = copy.deepcopy(picture_testing[pic_num])
        recall = False
        while(not recall):
            for xj in range(x.size):
                if((weights[xj]*x.getT()-theta[xj])>0):
                    x[0,xj] = 1
                elif((weights[xj]*x.getT()-theta[xj])<0):
                    x[0,xj] = -1
                else:
                    pass
            for mem in range(len(picture_memory)):
                if(np.any((x-picture_memory[mem]))):
                    pass
                else:
                    if(pic_num==0):
                        recall_result[0] = [pic_num,mem]
                    else:
                        recall_result.append([pic_num,mem])
                    recall = True
                    break
        
        #print(picture_memory[recall_pic].reshape([pic_rows,pic_columns]),recall_pic)
        #print(picture_testing[pic_num].reshape([pic_rows,pic_columns]))
        #print(pic_num,recall_pic)
    return recall_result
pic_rows = 13
pic_columns = 9

win = tk.Tk()
win.title("Hopfield")
win.geometry("800x450")
win.resizable(False,False)
path_f1 = tk.StringVar()
path_f2 = tk.StringVar()
path_label1 = tk.Label(win,textvariable = path_f1)
path_label2 = tk.Label(win,textvariable = path_f2)
result = "123123123"

def open_file():
    openf = tkf.askopenfilename(filetypes = (("Template files", "*.txt"),("HTML files", "*.html;*.htm"),("All files", "*.*") ))
    if(openf):
        path_f1.set(os.path.abspath(openf))
    openf = tkf.askopenfilename(filetypes = (("Template files", "*.txt"),("HTML files", "*.html;*.htm"),("All files", "*.*") ))
    if(openf):
        path_f2.set(os.path.abspath(openf))
open_file = tk.Button(win,text="open file",command = open_file)

def training():
    picture_memory = read_file(path_f1.get(),pic_rows,pic_columns)
    picture_testing = read_file(path_f2.get(),pic_rows,pic_columns)
    weights,theta = hopfield_memory(picture_memory,pic_rows,pic_columns)
    recall_result = hopfield_test(picture_memory,picture_testing,weights,theta)
    for j in recall_result:        
        output = ""
        for i in range(picture_testing[j[0]][0].size):            
            if(picture_testing[j[0]][0,i]==1):
                output += "■"
            else:
                output += "□"
            if((i+1)%pic_columns==0):
                output += "\n"
        output += "\n"
        for i in range(picture_memory[j[1]][0].size):            
            if(picture_memory[j[1]][0,i]==1):
                output += "■"
            else:
                output += "□"
            if((i+1)%pic_columns==0):
                output += "\n"
        output += "\n\n\n\n\n"
        scroll.insert("insert",output)        
        
btn_train = tk.Button(win,text="Start",command = training)

scroll = tks.ScrolledText(win)

path_label1.pack()
path_label2.pack()
open_file.pack()
btn_train.pack()
scroll.pack()
win.mainloop()