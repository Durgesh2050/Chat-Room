import socket
import threading
from tkinter import *

PORT= 50004
SERVER="192.168.43.143"

ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"

client = socket.socket(socket.AF_INET,
                       socket.SOCK_STREAM)
client.connect(ADDRESS)


class chatbox:
    def __init__(self):

        self.Window = Tk()
        self.Window.withdraw()

        self.login = Toplevel()
        self.login.title("Login")
        self.login.resizable(width=False,
                             height=False)
        self.login.configure(width=400,
                             height=300,
                             bg="blue")

        self.label = Label(self.login,
                           text="Please login to continue",
                           justify=CENTER,
                           font="Arial 14 bold",
                           bg="blue",
                           fg="white")
        self.label.place(relheight=0.15,
                         relx=0.2,
                         rely=0.07)

        self.labelName = Label(self.login,
                               text="Name: ",
                               font="Arial 12 ",
                               bg="blue",
                               fg="white")
        self.labelName.place(relheight=0.2,
                             relx=0.1,
                             rely=0.2)

        # create a entry box
        self.entryName = Entry(self.login,
                               font="Arial 14")
        self.entryName.place(relwidth=0.4,
                             relheight=0.12,
                             relx=0.35,
                             rely=0.2)

        self.entryName.focus()

        self.go = Button(self.login,
                         text="CONTINUE",
                         font="Arial 14 bold",
                         command=lambda: self.toChatWindow(self.entryName.get()))
        self.go.place(relx=0.4,
                      rely=0.55)
        self.Window.mainloop()

    def toChatWindow(self, name):  # you have written namme in arguments instead of name
        self.login.destroy()
        self.layout(name)

        rcv = threading.Thread(target=self.receive)
        rcv.start()

    def layout(self, name):
        self.name = name
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width=False,
                              height=False)
        self.Window.configure(width=470, height=550, bg="#17234A")

        self.labelHead = Label(self.Window,
                               bg="#17234A", fg="#EACCEE", text=self.name, font="Helvetica 13 bold", pady=5)
        self.labelHead.place(relwidth=1)

        self.line = Label(self.Window,
                          width=458, bg="#ABB289")
        self.line.place(relwidth=1, rely=0.07, relheight=0.012)  # changed rely to 0.07 from 8.87

        self.textCons = Text(self.Window,
                             width=20, height=2, bg="#17234A", fg="#EACCEE", font="Helvetica 13 bold", padx=5, pady=5) # changed width to 20 from 28
        self.textCons.place(relheight=0.745, relwidth=1, rely=0.08) # changed rely to 0.08 from 0.80

        self.labelBottom = Label(self.Window,
                                 bg="#ABB289", height=88)
        self.labelBottom.place(relwidth=1, rely=0.825)

        self.entryMsg = Entry(self.labelBottom,
                              bg="#2C3E50", fg="#EACCEE", font="Helvetica 13")
        self.entryMsg.place(relwidth=0.74, relheight=0.06, relx=0.011, rely=0.008)
        self.entryMsg.focus()

        self.buttonMsg = Button(self.labelBottom,
                                text="Send",
                                bg="#ABB289", width=28, font="Helvetica 18 bold",
                                command=lambda: self.sendButton(self.entryMsg.get()))
        self.buttonMsg.place(relwidth=0.22, relheight=0.06, relx=0.77, rely=0.008)

        self.textCons.config(cursor="arrow")

        scrollbar = Scrollbar(self.textCons)

        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.config(command=self.textCons.yview)
        self.textCons.config(state=DISABLED)

    def sendButton(self, msg):
        self.textCons.config(state=DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, END)
        snd = threading.Thread(target=self.sendMessage)
        snd.start()

    def receive(self):
        while True:
            try:
                message = client.recv(1024).decode(FORMAT)
                if message == 'NAME':
                    client.send(self.name.encode(FORMAT))
                else:
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END, message + "\n\n")

                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)

            except:
                print("An error occured!!")
                client.close()
                break

    def sendMessage(self):
        self.textCons.config(state=DISABLED)
        while True:
            message = (f"{self.name}: {self.msg}")
            client.send(message.encode(FORMAT))
            break


g = chatbox()

#This code is completed by Durgesh Kumar
