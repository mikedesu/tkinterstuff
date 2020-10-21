
from tkinter import *
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
import csv
import ast
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


# Creating a Genre Popularity interface
window = None
main_frame = None
my_canvas = None
my_scrollbar = None
my_scrollbarH = None
second_frame = None


def createWindow():
    global window
    window = Tk()
    window.title("The Music Tracker: Track and Compare Music")
    window.geometry("950x800")

def createMainframe():
    global main_frame
    main_frame=Frame(window)
    main_frame.pack(fill=BOTH, expand=1)

def createMyCanvas():
    global my_canvas 
    my_canvas= Canvas(main_frame)
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

def createScrollbars():
    global my_scrollbar
    global my_scrollbarH 
    my_scrollbar=ttk.Scrollbar(main_frame, orient=VERTICAL,command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)
    my_scrollbarH=ttk.Scrollbar(main_frame, orient=HORIZONTAL, command=my_canvas.xview)
    my_scrollbarH.pack(side=BOTTOM, fill=X)

def configMyCanvas():
    global my_canvas 
    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))
    my_canvas.configure(xscrollcommand=my_scrollbarH.set)

def createSecondFrame():
    global second_frame 
    global my_canvas 
    second_frame=Frame(my_canvas)
    my_canvas.create_window((0,0),window=second_frame, anchor="nw")  


try:
    createWindow()
    createMainframe()
    createMyCanvas()
    createScrollbars()
    configMyCanvas()
    createSecondFrame()
except Exception as e:
    print("Error: " + str(e))
    input()



def genre_popularity():
    global window
    genrelst=genre_popularityLst()
    print("this is the genrelist: ", genrelst)
        #get_popularity based on genre input
    popularity= get_popularity(genrelst)
    print(popularity)
    figure1 = Figure(figsize=(4,3), dpi=100)
    subplot1 = figure1.add_subplot(111) 
    xAxis = genrelst
    yAxis = popularity
    subplot1.bar(xAxis,yAxis, color = 'lightsteelblue') 
    bar1 = FigureCanvasTkAgg(figure1, window)
    #bar1 = FigureCanvasTkAgg(figure1, second_frame)
    bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=0)
    #plt.bar(genrelst,popularity, color = 'blue')
    #plt.xlabel('GENRE')
    #plt.ylabel('NUMBER OF TIMES GENRE WAS POPULAR')
#plt.xticks(index, Popularity)
#displaying the title
    plt.title(label='Genre Popularity Throughout the Years', fontweight=10, pad='2.0')
    #plt.show()


def get_popularity(genre_list):
    with open('Datasets/data_w_genres.csv', newline='', encoding="utf-8") as csvfile:
        #with open('/Users/jennadean/python/dataviz/data_w_genres.csv', newline='') as csvfile:
        genrepop=csv.DictReader(csvfile)
        #genre_list=['comic','rock','metal', 'traditional country', 'hip hop']
        popularity_threshold=50    
        genre_popularity=[]
        for genre in genre_list:
            genre_popularity.append(0)
        for row in genrepop:
            genrestr=row['genres']
            popularity=float(row['popularity'])
            if popularity < popularity_threshold:
                continue
        # genres in current row
            genre_current_row=ast.literal_eval(genrestr)
            i = 0
            len_genre_list = len(genre_list)
            while i < len_genre_list:
                genre = genre_list[i]
                #print("this is genre: ", genre)
                for genre_a in genre_current_row:
                    if genre == genre_a:
                        genre_popularity[i]+=1
                i+=1
        return genre_popularity
    
    
def genre_popularityLst():
    genrepopstr=genrepop.get()
    genrepoplst=[x.strip() for x in genrepopstr.split(",")]
    #genrepoplst=list(genrepopstr.split(","))
    return genrepoplst


def onClick():
    newwindow=tk.Toplevel()
    newwindow.title("Genre List")
    #msg=Message(newwindow, text="test")
    newwindow.geometry("400x400")
    # issue there are close to 2000 genres
    #cvs dictreader that reads the genres? How to display the pleutra of genres here?
    #scroll text?
    lab1= tk.Label(newwindow, text="hip hop, rock, traditional country, pop")
    lab1.grid(column=0, row=0)


def get_danceabilitylist(year_list, attributelst_task2):
    with open('Datasets/data_by_year.csv', newline='', encoding="utf-8") as csvfile:
        genredata =csv.DictReader(csvfile)
        print("this is attribute list: ", attributelst_task2)
        #year_list=['2011', '2012', '2013', '2014', '2015']
        year_list=list(map(float, year_list))
        attribute1_list=[]
        attribute2_list=[]
        for attribute in year_list:
            attribute1_list.append(0)
            attribute2_list.append(0)
        #year_list=list(map(float, year_list))
        for row in genredata:
            len_year_list=len(year_list)
            #year_current_row=ast.literal_eval(row['year'])
            len_year_list=len(year_list)
            for i in range(len_year_list):
                #print(i)
                int_year_current_row=int(row['year'])
                #print("this is year: ", year_list[i])
                int_year_list=int(year_list[i])
                #print("this is year in current row: ", year_current_row)
                if int_year_list == int_year_current_row:
                    attribute1_list[i]=row[attributelst_task2[0]]
                    attribute2_list[i]=row[attributelst_task2[1]]
        attribute1_list=[float(i) for i in attribute1_list]
        attribute2_list=[float(i) for i in attribute2_list]
        return attribute1_list, attribute2_list


def pressed_danceabilitybtn():
    year_liststr=yearlist_attribute.get()
    year_list=[x.strip() for x in year_liststr.split(",")]
    attributestr=attribute_list.get()
    attribute_list_task2=[x.strip() for x in attributestr.split(",")]
    attribute1_list, attribute2_list=get_danceabilitylist(year_list, attribute_list_task2)
    fig, (ax1, ax2)=plt.subplots(2)
    fig.suptitle("Tracking attributes throughout the years")
    ax1.plot(year_list, attribute2_list, color="m")
    ax1.set_ylabel("music %s" %(attribute_list_task2[1]))
    ax2.plot(year_list, attribute1_list, color="y")
    ax2.set_ylabel("music %s" %(attribute_list_task2[0]))
    ax2.set_xlabel("Year")
    fig.show()
  

def get_artist_pop(artist_list):
    with open('Datasets/data.csv', newline='', encoding="utf-8") as csvfile:
        genrepop=csv.DictReader(csvfile)  
        print(artist_list)
        popularity_threshold=50
        artist_popularity=[]
        for artist in artist_list:
            artist_popularity.append(0)
        for row in genrepop:
            artist_str=row['artists']
            popularity=float(row['popularity'])
            if popularity < popularity_threshold:
                   continue
            # artists in current row
            artist_current_row=ast.literal_eval(artist_str)
            len_artist_list = len(artist_list) 
            for i in range(len_artist_list):
                artist = artist_list[i]
                for artist_a in artist_current_row:
                    if artist == artist_a:
                        artist_popularity[i]+=1
        print(artist_popularity)
        return artist_popularity
        

def pressed_artist_pop():
    artist_str=artist_entry.get()
    #artist_list=list(artist_str.split(","))
    artist_list=[x.strip() for x in artist_str.split(",")]
    artist_popularity=get_artist_pop(artist_list)
    print(artist_popularity)
    colors=['r','y','b','g','m']
    #plotting the pie chart
    plt.pie(artist_popularity, labels = artist_list, colors=colors,  
         startangle=90, shadow = True, explode = (0.1, 0.1, 0.1, 0.1, 0.1), 
        radius = 1.2, autopct = '%1.1f%%') 
    plt.legend(bbox_to_anchor=(.1,.1), loc="lower right")
    plt.show()


def get_attribute_lists(artist_list, attributelst):
    with open('Datasets/data_by_artist.csv', newline='',  encoding="utf-8") as csvfile:
        genrepop=csv.DictReader(csvfile)
        attribute1_list=[]
        attribute2_list=[]
        print(artist_list)
        print(attributelst[0], attributelist[1])
        for artist in artist_list:
            attribute1_list.append(0)
            attribute2_list.append(0)
        for row in genrepop:
            artist_str=row['artists']
            # artists in current row
            # Question why does st.literal_eval not work?
            artist_current_row=[artist_str]
            len_artist_list = len(artist_list)
            for i in range(len_artist_list):
                artist = artist_list[i]
                for artist_a in artist_current_row:
                    if artist == artist_a:
                        attribute1_list[i]=row[attributelst[0]]
                        attribute2_list[i]=row[attributelst[1]]
        attribute1_list=[float(i) for i in attribute1_list]
        attribute2_list=[float(i) for i in attribute2_list]
        return attribute1_list, attribute2_list
        

def pressed_track_attributes():
    artist_str=artist_entry.get()
    artist_list=[x.strip() for x in artist_str.split(",")]
    attribute_str=attribute_entries.get()
    attributelst=[x.strip() for x in attribute_str.split(",")]
    print(attributelst)
    attribute1_list, attribute2_list=get_attribute_lists(artist_list, attributelst)
    fig, (ax1, ax2)=plt.subplots(2)
    fig.suptitle("Tracking attributes throughout the years")
    ax1.plot(artist_list, attribute2_list, color="blue")
    ax1.set_ylabel("%s" %(attributelst[1]))
    ax2.plot(artist_list, attribute1_list, color="orange")
    ax2.set_ylabel("%s" %(attributelst[0]))
    ax2.set_xlabel("Year")
    fig.show()
  

def get_genrelist():
    with open('Datasets/data_by_genres.csv', newline='', encoding="utf-8") as csvfile:
        newfile =csv.DictReader(csvfile)
        alist=[]
        for row in newfile:
            #print(row['genres'])
            alist.append(row['genres'])
        return alist


#for listbox "Artist List"
def get_artistlist():
     with open('Datasets/data_by_artist.csv', newline='', encoding="utf-8") as csvfile:
        alist=[]
        try:
            newfile =csv.DictReader(csvfile)
            for row in newfile:
                #print(row['artists'])
                #yield {unicode(key, 'utf-8'):unicode(value, 'utf-8') for key, value in row.iteritems()}
                artistRow = row['artists']
                alist.append(artistRow)
        except Exception as e:
            print("get_artistlist exception: " + str(e))
        return alist


def get_attributes():
    attribute_data = pd.read_csv("Datasets/data_by_artist.csv", nrows=0)
    a = [a for a in attribute_data]
    a.remove('artists')
    return a



genrepop = None
yearlist_attribute = None
attribute_list = None
artist_entry = None
attribute_entries = None
lbl = None
val1 = None
btn1 = None
btn1a = None
listbox = None
genrelist = None

def initVars():
    global genrepop 
    global yearlist_attribute 
    global attribute_list 
    global artist_entry 
    global attribute_entries 
    global lbl
    global val1
    global btn1
    global btn1a
    global listbox
    global genrelist
    genrepop = StringVar(second_frame, value="")
    yearlist_attribute = StringVar(second_frame, value=" ")
    attribute_list = StringVar(second_frame, value=" ")
    artist_entry = StringVar(second_frame, value=" ")
    attribute_entries = StringVar(second_frame,value=" ")
    lbl = Label(second_frame, text="Please enter genres from 'Genre List': \n (with a comma between each genre)\n also enter artists of interest above", font=("times new roman", 16, "bold"), bg="powder blue", fg="black")
    lbl.grid(column=0, row=0)
    val1= Entry(second_frame, font = ("times new roman", 16, "bold"),bd = 8, bg = "grey", fg='black', textvariable= genrepop, justify=LEFT, width=50)
    val1.grid(column=1, row=0)
    btn1=ttk.Button(second_frame, text="Determine how many times the genres of interest \n have been associated with popular artists", width=35, command=genre_popularity)
    btn1.grid(column=0, row=2)
    btn1a=tk.Button(second_frame, text="Genre List:", font =("times new roman", 16, "bold"), width=35)
    btn1a.grid(column=1, row =2)
    listbox = Listbox(second_frame)
    listbox.grid(column=1, row=4)  #10
    genrelist=get_genrelist()
    for g in genrelist:
        listbox.insert(END, g)



initVars()



lb2= Label(second_frame, text="Please enter years of interest here: \n Followed by two attributes (from 'Attribute List' below) \n in the next line: \n (with a comma between each year/attribute)", font=("times new roman", 16, "bold"), bg="powder blue", fg="black")
lb2.grid(column=0, row=8)


val2=Entry(second_frame, font = ("times new roman", 16, "bold"),bd = 8, bg = "grey", fg='black',textvariable= yearlist_attribute, justify=LEFT, width=50)
val2.grid(column=1, row=8)  #6
val2a=Entry(second_frame, font = ("times new roman", 16, "bold"),bd = 8, bg = "grey", fg='black',textvariable= attribute_list,justify=LEFT, width=50)
val2a.grid(column=2, row=8)  #6


btn2=ttk.Button(second_frame, text="Track attributes throughout the years", width=35, command=pressed_danceabilitybtn)
btn2.grid(column=0, row=9) #row 8


lb3= Label(second_frame, text="Please enter five artists of interest \n from 'Artist List': \n (with a comma between each artist)", font=("times new roman", 16, "bold"), bg="powder blue", fg="black")
lb3.grid(column=0, row=12)  #18


val3=Entry(second_frame, font = ("times new roman", 16, "bold"),bd=8, bg="grey", fg='black', textvariable= artist_entry,justify=LEFT, width=50)
val3.grid(column=1, row=12)  #6


btn3=ttk.Button(second_frame, text="Compare artist popularity (based upon the number \n of popular songs assoicated with each artist)", width=35,
                command=pressed_artist_pop)
btn3.grid(column=0, row=13) 


btn3a=tk.Button(second_frame, text="Artist List:", font =("times new roman", 16, "bold"), width=35)
btn3a.grid(column=1, row =13) 


listbox1=Listbox(second_frame)
listbox1.grid(column=1, row=15)  #32
artistlist=get_artistlist()
for a in artistlist:
    listbox1.insert(END, a)


lb4= Label(second_frame, text="Please enter two attributes from 'Attribute List' \n (with a comma and no space between each attribute) \n (also ensure that five artists are entered directly above)",
font = ("times new roman", 16, "bold"), bg ="powder blue", fg="black")
lb4.grid(column=0, row = 19)  #18


val4=Entry(second_frame, font = ("times new roman", 16, "bold"),bd = 8, bg = "grey", fg='black', textvariable= attribute_entries,justify=LEFT, width=50)
val4.grid(column=1, row=19)  #6
btn4=ttk.Button(second_frame, text="Track (and compare) attributes amongst the artists", width=35, command= pressed_track_attributes)
btn4.grid(column=0, row=21)


btn4a=tk.Button(second_frame, text="Attribute List:", font =("times new roman", 16, "bold"), width=35)
btn4a.grid(column=1, row =21)


listbox2=Listbox(second_frame)
listbox2.grid(column=1, row=23)  #10
attributelist=get_attributes()
for a in attributelist:
    listbox2.insert(END, a)


lb5 = Label(second_frame, text="Please enter genres of interest \n from the 'Genre List' (above) for comparision: \n (with a comma between each genre) \n also enter artists of interest above", font = ("times new roman", 16, "bold"), bg = "powder blue", fg="black")
lb5.grid(column=0, row=25)


val5= Entry(second_frame, font = ("times new roman", 16, "bold"),bd = 8, bg = "grey", fg='black', textvariable= genrepop, justify=LEFT, width=50)
val5.grid(column=1, row=25)


btn5=ttk.Button(second_frame, text="Compare Genres", width=35, command= genre_popularity)
btn5.grid(column=0, row=27)

    
window.mainloop()
