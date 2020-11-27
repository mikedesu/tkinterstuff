
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

window             = None
main_frame         = None
my_canvas          = None
my_scrollbar       = None
my_scrollbarH      = None
second_frame       = None
genrepop           = None
yearlist_attribute = None
artist_entry       = None
attribute_entries  = None

btn1               = None
btn2               = None
btn3               = None
btn1a              = None
btn3a              = None
btn4               = None
btn4a              = None
btn5               = None

listbox            = None

label1             = None
lb2                = None
lb3                = None
lb4                = None
lb5                = None

val1               = None
val2               = None
val3               = None
val2a              = None
val4               = None
val5               = None

listbox1           = None
listbox2           = None

artistlist         = None
attributelist      = None
attribute_list     = None
genrelist          = None

compare_genres     = None

bar1 = None

attributeList = [
    "acousticness",
    "danceability",
    "duration_ms",
    "energy",
    "instrumentalness",
    "liveness",
    "loudness",
    "speechiness",
    "tempo",
    "valence",
    "popularity",
    "key",
    "mode",
    "count"
]

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

def generate_simple_graph( xAxis=None, yAxis=None, xLabel=None, yLabel=None ):
    global window
    global bar1
    assert( xAxis != None )
    assert( yAxis != None )
    assert( xLabel  != None )
    assert( yLabel != None )
    figureSize = (10,2)
    figuredpi = 100
    figure1 = Figure(figsize=figureSize, dpi=figuredpi)
    nrows = 6
    ncols = 1
    beginEndPair = (1,5)
    subplot1 = figure1.add_subplot(nrows, ncols, beginEndPair) 
    subplot1.bar(xAxis,yAxis, color = 'blue') 
    figure1.suptitle("Genre Pop")
    subplot1.set_xlabel(xLabel)
    subplot1.set_ylabel(yLabel)
    if bar1 != None:
        bar1.get_tk_widget().pack_forget()
    bar1 = FigureCanvasTkAgg(figure1, window)
    bar1.get_tk_widget().pack( side=tk.LEFT, fill=tk.BOTH, expand=0)

def genre_popularity():
    global window
    global bar1
    genrelst = genre_popularityLst()
    popularity= get_popularity(genrelst)
    generate_simple_graph( genrelst, popularity, "xlabel", "ylabel" )

def get_popularity(genre_list):
    dataWithGenresFilepath = "Datasets/data_w_genres.csv"
    with open(dataWithGenresFilepath, newline='', encoding="utf-8") as csvfile:
        genrepop=csv.DictReader(csvfile)   
        genre_popularity=[]
        for genre in genre_list:
            genre_popularity.append(0)
        for row in genrepop:
            genrestr=row['genres']
            popularity=float(row['popularity'])
            genre_current_row=ast.literal_eval(genrestr)
            i = 0
            len_genre_list = len(genre_list)
            while i < len_genre_list:
                genre = genre_list[i]
                for genre_a in genre_current_row:
                    if genre == genre_a:
                        genre_popularity[i]+=1
                i+=1
        return genre_popularity
    
def genre_popularityLst():
    genrepopstr=genrepop.get()
    genrepoplst=[x.strip() for x in genrepopstr.split(",")]
    return genrepoplst

#def onClick():
#    newwindow = tk.Toplevel()
#    newwindow.title("Genre List")
#    newwindow.geometry("400x400")
#    lab1= tk.Label(newwindow, text="hip hop, rock, traditional country, pop")
#    lab1.grid(column=0, row=0)

def get_danceabilitylist(year_list, attributelst_task2):
    dataByYearFilepath = "Datasets/data_by_year.csv"
    with open(dataByYearFilepath, newline='', encoding="utf-8") as csvfile:
        genredata =csv.DictReader(csvfile)
        year_list=list(map(float, year_list))
        attribute1_list=[]
        attribute2_list=[]
        for attribute in year_list:
            attribute1_list.append(0)
            attribute2_list.append(0)
        for row in genredata:
            len_year_list=len(year_list)
            len_year_list=len(year_list)
            for i in range(len_year_list):
                int_year_current_row=int(row['year'])
                int_year_list=int(year_list[i])
                if int_year_list == int_year_current_row:
                    attribute1_list[i] = row[attributelst_task2[0]]
                    attribute2_list[i] = row[attributelst_task2[1]]
        attribute1_list=[ float(i) for i in attribute1_list ]
        attribute2_list=[ float(i) for i in attribute2_list ]
        return attribute1_list, attribute2_list

def get_artist_pop(artist_list):
    dataFilepath = "Datasets/data.csv"
    try:
        with open(dataFilepath, newline='', encoding="utf-8") as csvfile:
            genrepop = csv.DictReader(csvfile)  
            popularity_threshold = 50
            artist_popularity = [ 0 for artist in artist_list ]
            for row in genrepop:
                artist_str=row['artists']
                popularity=float(row['popularity'])
                if popularity < popularity_threshold:
                       continue
                artist_current_row=ast.literal_eval(artist_str)
                len_artist_list = len(artist_list) 
                for i in range(len_artist_list):  
                    artist = artist_list[i]
                    for artist_a in artist_current_row:
                        if artist.lower() == artist_a.lower():
                            artist_popularity[i]+=1
            return artist_popularity
    except Exception as e:
        tk.messagebox.showerror(title="Error", message=str(e))

def get_attribute_lists(artist_list, attributelst):
    with open('Datasets/data_by_artist.csv', newline='',  encoding="utf-8") as csvfile:
        genrepop=csv.DictReader(csvfile)
        attribute1_list=[ 0 for artist in artist_list ]
        attribute2_list=[ 0 for artist in artist_list ]
        for row in genrepop:
            artist_str=row['artists']
            artist_current_row=[artist_str]
            len_artist_list = len(artist_list)
            for i in range(len_artist_list):
                artist = artist_list[i]
                for artist_a in artist_current_row:
                    if artist.lower() == artist_a.lower():
                        attribute1_list[i]=row[attributelst[0]]
                        attribute2_list[i]=row[attributelst[1]]
        attribute1_list=[float(i) for i in attribute1_list]
        attribute2_list=[float(i) for i in attribute2_list]
        return attribute1_list, attribute2_list

def pressed_track_attributes():
    global window
    global bar1
    global artist_entry 
    global attribute_entries
    artist_str=artist_entry.get()
    artist_list=[x.strip() for x in artist_str.split(",")]
    attribute_str=attribute_entries.get()
    attributelst=[x.strip() for x in attribute_str.split(",")]
    attribute1_list, attribute2_list=get_attribute_lists(artist_list, attributelst)
    fig, (ax1, ax2)=plt.subplots(2)
    fig.suptitle("Tracking attributes throughout the years")
    ax1.plot(artist_list, attribute2_list, color="blue")
    ax1.set_ylabel("%s" %(attributelst[1]))
    ax2.plot(artist_list, attribute1_list, color="orange")
    ax2.set_ylabel("%s" %(attributelst[0]))
    ax2.set_xlabel("Artist")
    if bar1 != None:
        bar1.get_tk_widget().pack_forget()
    bar1 = FigureCanvasTkAgg(fig, window)
    bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=0)

def generate_attributes_graph():
    global window
    global bar1
    global yearlist_attribute 
    global attribute_list 
    year_liststr=yearlist_attribute.get()
    year_list=[x.strip() for x in year_liststr.split(",")]
    attributestr=attribute_list.get()
    attribute_list_task2=[x.strip() for x in attributestr.split(",")]
    # awful naming schema here, no hard feelings lol
    attribute1_list, attribute2_list=get_danceabilitylist(year_list, attribute_list_task2)
    fig, (ax1, ax2)=plt.subplots(2)
    fig.suptitle("Tracking attributes throughout the years")
    ax1.plot(artist_list, attribute2_list, color="blue")
    ax1.set_ylabel("%s" %(attributelst[1]))
    ax2.plot(artist_list, attribute1_list, color="orange")
    ax2.set_ylabel("%s" %(attributelst[0]))
    if bar1 != None:
        bar1.get_tk_widget().pack_forget()
    bar1 = FigureCanvasTkAgg(fig, window)
    bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=0)

def pressed_artist_pop():
    global artist_entry
    global bar1
    artist_str=artist_entry.get()
    artist_list=[x.strip() for x in artist_str.split(",")]
    artist_popularity=get_artist_pop(artist_list)
    colors = ['r','y','b','g','m']
    fig, ax1 = plt.subplots()
    ax1.pie(artist_popularity, labels=artist_list, colors=colors, startangle=90, shadow = True, explode = (0.1, 0.1, 0.1, 0.1, 0.1), radius = 1.2, autopct = '%1.1f%%') 
    ax1.legend(bbox_to_anchor=(.1,.1), loc="lower right")
    if bar1 != None:
        bar1.get_tk_widget().pack_forget()
    bar1 = FigureCanvasTkAgg(fig, window)
    bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=0)

def generate_simple_graph2( stitle=None, xLabel=None ):
    global window
    global bar1
    global yearlist_attribute 
    global attribute_list 
    year_list = [x.strip() for x in yearlist_attribute.get().split(",")]
    user_entered_attributes_list = [x.strip() for x in attribute_list.get().split(",")]
    attribute1_list, attribute2_list=get_danceabilitylist(year_list, user_entered_attributes_list)
    fig, (ax1, ax2) = plt.subplots(2)
    fig.suptitle( stitle )
    ax1.plot(year_list, attribute2_list, color="m")
    ax1.set_ylabel("music %s" %( user_entered_attributes_list[1] ))
    ax2.plot(year_list, attribute1_list, color="y")
    ax2.set_xlabel( xLabel )
    ax2.set_ylabel("music %s" %( user_entered_attributes_list[0] ))
    if bar1 != None:
        bar1.get_tk_widget().pack_forget()
    bar1 = FigureCanvasTkAgg(fig, window)
    bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=0)

def pressed_danceabilitybtn():
    generate_simple_graph2( "Tracking attributes throughout the years", "Year" )
 
def get_genrelist():
    dataByGenreFilepath = "Datasets/data_by_genres.csv"
    with open(dataByGenreFilepath, newline='', encoding="utf-8") as csvfile:
        newfile = csv.DictReader(csvfile)
        alist=[]
        for row in newfile:
            alist.append(row['genres'])
        return alist

def get_artistlist():
    dataByArtistFilepath = "Datasets/data_by_artist.csv"
    with open(dataByArtistFilepath, newline='', encoding="utf-8") as csvfile:
        alist=[]
        try:
            newfile =csv.DictReader(csvfile)
            for row in newfile:
                artistRow = row['artists']
                alist.append(artistRow)
        except Exception as e:
            print("get_artistlist exception: " + str(e))
        return alist

def get_attributes():
    dataByArtistFilepath = "Datasets/data_by_artist.csv"
    attribute_data = pd.read_csv(dataByArtistFilepath, nrows=0)
    a = [a for a in attribute_data]
    a.remove('artists')
    return a

def initVars():
    global genrepop 
    global yearlist_attribute 
    global attribute_list 
    global artist_entry 
    global attribute_entries 
    global label1
    global val1
    global btn1
    global btn2
    global btn1a
    global listbox
    global genrelist
    global lb2
    global lb3
    global val2
    global val3
    global val2a
    global btn3
    global btn3a
    global listbox1
    global artistlist
    global lb4
    global val4
    global btn4
    global btn4a
    global listbox2
    global attributelist
    global lb5
    global val5
    global btn5
    global compare_genres
    genrepop           = StringVar( second_frame, value="" )
    yearlist_attribute = StringVar( second_frame, value="" )
    attribute_list     = StringVar( second_frame, value="" )
    artist_entry       = StringVar( second_frame, value="" )
    attribute_entries  = StringVar( second_frame, value="" )
    compare_genres     = StringVar( second_frame, value="" )
    
    label1 = Label(second_frame, text="Please enter genres from 'Genre List': ", font=("times new roman", 16, "bold"), bg="powder blue", fg="black")
    label1.grid(column=0, row=0)

    val1 = Entry(second_frame, font = ("times new roman", 16, "bold"),bd = 8, bg = "grey", fg='black', textvariable= genrepop, justify=LEFT, width=50)
    val1.grid(column=1, row=0)
    
    btn1 = ttk.Button(second_frame, text="Determine how many times the genres of interest \n have been associated with popular artists", width=35, command=genre_popularity)
    btn1.grid(column=0, row=2)
    
    btn1a = tk.Button(second_frame, text="Genre List:", font =("times new roman", 16, "bold"), width=35)
    btn1a.grid(column=1, row =2)
    
    listbox = Listbox(second_frame)
    listbox.grid(column=1, row=4)  #10
    
    for g in get_genrelist():
        listbox.insert(END, g)
    
    lb2 = Label(second_frame, text="Please enter years of interest in first entry\nFollowed by two attributes (from 'Attribute List' below)\nIn second entry:", font=("times new roman", 16, "bold"), bg="powder blue", fg="black")
    lb2.grid(column=0, row=8)
    
    val2 = Entry(second_frame, font = ("times new roman", 16, "bold"),bd = 8, bg = "grey", fg='black',textvariable= yearlist_attribute, justify=LEFT, width=50)
    val2.grid(column=1, row=8)  #6
    
    val2a = Entry(second_frame, font = ("times new roman", 16, "bold"),bd = 8, bg = "grey", fg='black',textvariable= attribute_list,justify=LEFT, width=50)
    val2a.grid(column=2, row=8)  #6
    
    btn2=ttk.Button(second_frame, text="Track attributes throughout the years", width=35, command=pressed_danceabilitybtn)
    btn2.grid(column=0, row=9) #row 8

    lb3= Label(second_frame, text="Please enter five artists of interest \n from 'Artist List': ", font=("times new roman", 16, "bold"), bg="powder blue", fg="black")
    lb3.grid(column=0, row=12)  #18
    
    val3=Entry(second_frame, font = ("times new roman", 16, "bold"),bd=8, bg="grey", fg='black', textvariable= artist_entry,justify=LEFT, width=50)
    val3.grid(column=1, row=12)  #6
    
    btn3=ttk.Button(second_frame, text="Compare artist popularity (based upon the number \n of popular songs assoicated with each artist)", width=35,command=pressed_artist_pop)
    btn3.grid(column=0, row=13) 

    btn3a=tk.Button(second_frame, text="Artist List:", font =("times new roman", 16, "bold"), width=35)
    btn3a.grid(column=1, row =13) 
    
    listbox1 = Listbox(second_frame)
    listbox1.grid(column=1, row=15)  #32
    
    artistlist=get_artistlist()
    
    for a in artistlist:
        listbox1.insert(END, a)
    
    lb4 = Label(second_frame, text="Please enter two attributes from 'Attribute List' \n (ensure that five artists are entered in above entry)", font = ("times new roman", 16, "bold"), bg ="powder blue", fg="black")
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
    
    val5 = Entry(second_frame, font = ("times new roman", 16, "bold"),bd = 8, bg = "grey", fg='black', textvariable= compare_genres, justify=LEFT, width=50)
    val5.grid(column=1, row=25)
    
    btn5=ttk.Button(second_frame, text="Compare Genres", width=35, command=compareGenresButtonPressed )
    btn5.grid(column=0, row=35)


def compareGenresButtonPressed():
    global compare_genres 
    global bar1
    compare_genres_str = compare_genres.get()
    new_genre_list = compare_genres_str.split(",")
    with open('Datasets/data_by_genres.csv', newline='') as csvfile:
        genre_data = csv.DictReader(csvfile)
        #genres_list=["pop", 'traditional country', "jazz", 'metal']
        genres_list = new_genre_list 
        len_genres_list = len(genres_list)
        acousticness = [0 for genre in genres_list]
        danceability = [0 for genre in genres_list]
        duration_ms  = [0 for genre in genres_list]
        energy       = [0 for genre in genres_list]
        instrumentalness = [0 for genre in genres_list]
        liveness     = [0 for genre in genres_list]
        loudness     = [0 for genre in genres_list]
        speechiness  = [0 for genre in genres_list]
        tempo        = [0 for genre in genres_list]
        valence      = [0 for genre in genres_list]
        popularity   = [0 for genre in genres_list]
        key          = [0 for genre in genres_list]
        mode         = [0 for genre in genres_list]
        #count        = [0 for genre in genres_list]

        for row in genre_data:
            for i in range(len_genres_list):
                genre=genres_list[i]
                if genre==row['genres']:
                    acousticness[i]     = row[ 'acousticness'     ]
                    danceability[i]     = row[ 'danceability'     ]
                    duration_ms[i]      = row[ 'duration_ms'      ]
                    energy[i]           = row[ 'energy'           ]
                    instrumentalness[i] = row[ 'instrumentalness' ]
                    liveness[i]         = row[ 'liveness'         ]
                    loudness[i]         = row[ 'loudness'         ]
                    speechiness[i]      = row[ 'speechiness'      ]
                    tempo[i]            = row[ 'tempo'            ]
                    valence[i]          = row[ 'valence'          ]
                    popularity[i]       = row[ 'popularity'       ]
                    key[i]              = row[ 'key'              ]
                    mode[i]             = row[ 'mode'             ]
                    #count[i]        = row['count']

        acousticness     = list( map( float, acousticness) )
        danceability     = list( map( float, danceability) )
        duration_ms      = list( map( float, duration_ms) )
        energy           = list( map( float, energy) )
        instrumentalness = list( map( float, instrumentalness) )
        liveness         = list( map( float, liveness) )
        loudness         = list( map( float, loudness) )
        speechiness      = list( map( float, speechiness) )
        tempo            = list( map( float, tempo) )
        valence          = list( map( float, valence) )
        popularity       = list( map( float, popularity) )
        key              = list( map( float, key) )
        mode             = list( map( float, mode) )

        attributeList = [
            "acousticness",
            "danceability",
            "energy",
            "instrumentalness",
            "liveness",
        ]

        combined_attributes_list = [
            acousticness,
            danceability,
            energy,
            instrumentalness,
            liveness,
        ]
        attribute_list = attributeList
        assert( len(attribute_list) == len(combined_attributes_list) ) 

        fig, ax = plt.subplots()
        im      = ax.imshow( combined_attributes_list )

        plt.colorbar(im)

        ax.set_xticks(np.arange(len(genres_list)))
        ax.set_yticks(np.arange(len(attribute_list)))

        # ... and label them with the respective list entries
        ax.set_xticklabels(genres_list)
        ax.set_yticklabels(attribute_list)

        # Rotate the tick labels and set their alignment.
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

        # Loop over data dimensions and create text annotations.
        for i in range(len(attribute_list)):
            for j in range(len(genres_list)):
                x = float( f"{combined_attributes_list[i][j]:0.2f}" )
                text = ax.text(j, i, x, ha="center", va="center", color="w")
        ax.set_title("Genre Comparison")
        fig.tight_layout()
        if bar1 != None:
            bar1.get_tk_widget().pack_forget()
        bar1 = FigureCanvasTkAgg(fig, window)
        bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=0)

def main():
    try:
        createWindow()
        createMainframe()
        createMyCanvas()
        createScrollbars()
        configMyCanvas()
        createSecondFrame()
        initVars()
        window.mainloop()
    except Exception as e:
        print("Error: " + str(e))
        input()
    
if __name__ == "__main__":
    main()
