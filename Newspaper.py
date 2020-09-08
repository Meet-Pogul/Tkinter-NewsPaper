# Newspaper 10 images and corresponding .txt file show gui file
from tkinter import *
from tkinter import messagebox
from json import loads
from requests import get
from bs4 import BeautifulSoup
from requests.exceptions import MissingSchema
from json.decoder import JSONDecodeError
import pyttsx3
import webbrowser
import threading

data = {}
pno = 1
lab = []


def combine(func, **kw):
    k = func
    lab.append(k)
    k.pack(kw)


def Auto():
    global pno
    pno = 1
    try:
        for i in range(1, len(data)+1):
            page(i)
            speak()
            forward()
    except RuntimeError:
        pass


def Run(func):
    threading.Thread(target=func).start()


def gotoUrl():
    chrome = r"C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
    webbrowser.get(chrome).open_new_tab(data[pno]["url"])


def speak():
    """Speak the string which have been passed as an argument"""
    try:
        engine = pyttsx3.init('sapi5')
        # get voice from microsoft text to speech
        voice = engine.getProperty('voices')[1]
        # set above voice by default [0] is selected
        engine.setProperty('voice', voice.id)
        engine.setProperty('rate', 170)  # set speed of voice, by default 200
        for i in data[pno]:
            if data[pno][i] != None and i in ["author", "title", "description"]:
                engine.say(data[pno][i])
        engine.runAndWait()
    except RuntimeError:
        print("Unable to start")


def forward():
    global pno
    pno += 1
    page(pno)


def backward():
    global pno
    pno -= 1
    page(pno)


def details(category="technology"):
    with open("newsapi.txt", "r") as f:
        api = f"apiKey={f.readline()}"
    category = "category="+category
    country = "country=in"
    what = "top-headlines"
    try:
        content_j = get(
            f"https://newsapi.org/v2/{what}?{country}&{category}&{api}")
        content_p = loads(content_j.text)
    except MissingSchema:
        print("Schema or site Not found")
    except JSONDecodeError:
        print("Content not found")
    except Exception:
        print("Conncetion Time out")
    k = 1
    for i in content_p["articles"]:
        t = {"From": i["source"]["name"]}
        for j in i:
            if j in ["author", "title", "description", "content", "url"]:
                if i[j] == None:
                    t.update({j: None})
                else:
                    if j == "content" and "<li>" in i["content"]:
                        conli = BeautifulSoup(i[j], "html.parser")
                        con = ""
                        for p in conli.find_all("li"):
                            con += p.text + "\n"
                        i[j] = con
                    elif j == "author":
                        i[j] = "This News is From " + i[j]
                    t.update({j: i[j]})
        data.update({k: t})
        k += 1


def welcome():
    global pno
    for i in lab:
        i.destroy()
    combine(Label(root, text="Welcome\nto\nMSP News", bg="Green", font=("Times New Roman", int(texlen.get()/100+20)),
                  wraplength=texlen.get()),
            pady=10, fill=X)

    combine(Label(root, text="Choose Category", bg="lightblue", font=("Times New Roman", int(texlen.get()/100+10)),
                  wraplength=texlen.get()),
            pady=10, fill=X)

    l = ["Business", "Entertainment", "General",
         "Health", "Science", "Sports", "Technology"]
    var = StringVar()
    var.set("technology")
    for i in l:
        combine(Radiobutton(root, text=i, padx=14, variable=var, value=i.lower(), bg="black", fg="red",font=("Times New Roman", int(texlen.get()/100+10))),
                anchor="w")
    pno=1
    combine(Button(root, text="Start", command=lambda: [details(var.get()), page(1)],
                   font="bold"),pady=20)


def page(no):
    texlen.set(root.winfo_width()/1.2)
    for i in lab:
        i.destroy()
    color = ("green", "lightblue", "yellow", "orange", "lightgreen", "cyan")
    c = 0
    for i in data[no]:
        if data[no][i] != None:
            root.update()
            combine(Label(root, text=data[no][i], bg=color[c], font=("Times New Roman", int(texlen.get()/100+10)), wraplength=texlen.get()),
                    pady=10, fill=X)
            c += 1

    f1 = Frame(root, bg="black")
    f1.pack(fill=X, side=BOTTOM)
    combine(Button(f1, text="Home",  borderwidth=5, command=welcome),
            padx=5, side=LEFT)

    combine(Button(f1, text="Visit",  borderwidth=5, command=gotoUrl),
            padx=5, side=LEFT)

    combine(Button(f1, text="Auto",  borderwidth=5, command=lambda: Run(Auto)),
            padx=5, side=LEFT)

    combine(Button(f1, text="Speak",  borderwidth=5, command=lambda: Run(speak)),
            padx=5, side=LEFT)

    if no > len(data)-1:
        combine(Label(root, text="You Reached Last News", bg="red", font=("Times New Roman", 10)),
                pady=5)
    else:
        combine(Button(f1, text="Next",  borderwidth=5, command=forward),
                padx=5, side=RIGHT)

    if no < 2:
        combine(Label(root, text="You are in First News", bg="red", font=("Times New Roman", 10)),
                pady=5)
    else:
        combine(Button(f1, text="Previous",  borderwidth=5, command=backward),
                padx=5, side=RIGHT)

    lab.append(f1)


if __name__ == "__main__":
    root = Tk()
    root.geometry("700x625")
    root.minsize(340,625)
    root.title("Daily News")
    root.wm_iconbitmap("news.ico")
    root.config(bg="black")
    texlen = DoubleVar()
    texlen.set(root.winfo_screenwidth()/2)
    welcome()
    root.mainloop()
