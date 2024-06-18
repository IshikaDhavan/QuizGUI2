import socket
from threading import Thread
from tkinter import *

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#name = "Write your name: "
ipaddr = "127.0.0.1"
port = 7500

client.connect((ipaddr,port))
print("connected with server")

class GUI:
    def __init__(self):
        self.Window = Tk()
        self.Window.withdraw()

        self.login = Toplevel()
        self.login.title("Login")
        self.login.resizable(width= False, height= False)
        self.login.configure(width= 400, height= 300)

        self.pls = Label(self.login, text="Login to continue", justify= CENTER, font="Helvetica 14 bold")
        self.pls.place(relheight= 0.15, relx= 0.2, rely=0.07)

        self.labelName = Label(self.login, text="Enter Name", font="Helvetica 12")
        self.labelName.place(relheight= 0.1, relx= 0.1, rely= 0.3)

        self.entryName = Entry(self.login, font="Helvetica 12")
        self.entryName.place(relwidth= 0.4,relheight= 0.12,relx= 0.35, rely= 0.3)

        self.go = Button(self.login,text="Continue", font="Helvetica 14 bold", command= lambda: self.goAhead(self.entryName.get()))
        self.go.place(relx = 0.4, rely= 0.55)

        self.Window.mainloop()

    def goAhead(self,name):
        self.login.destroy()

        #self.name = name
        self.layout(name)
        rcv = Thread(target= self.receive)
        rcv.start()

    def receive(self):
        while True:
            try:
                message = client.recv(2048).decode('utf-8')
                if message == 'NICKNAME':
                    client.send(self.name.encode('utf-8'))
                else:
                    self.showMessage(message)
            except:
                print("An error occured")
                client.close()
                break

    def layout(self, name):
        self.name = name
        self.Window.deiconify()
        self.Window.title("QUIZ")
        self.Window.resizable(width= FALSE, height= FALSE)
        self.Window.configure(width = 470, height= 550, bg="#17202A")

        self.labelHead = Label(self.Window, bg="17202A", fg = "#EAECEE", text = self.name, pady= 5, font="Helvetica 13 bold")
        self.labelHead.place(relwidth= 1)

        self.line = Label(self.Window, width=450, bg="#ABB2B9")
        self.line.place(rely = 0.07, relheight= 0.012)

        self.textCon = Text(self.Window, width= 20, heigh= 2, bg="#17202A", fg = "#EAECEE", font="Helvetica 14", padx= 5, pady=5)
        self.textCon.place(relheight=0.745, relwidth=1, rely=0.08)

        self.labelBotttom = Label(self.Window, bg="#ABB2B9", height=80)
        self.labelBotttom.place(relwidth= 1, rely= 0.825)

        self.entryMSG = Entry(self.labelBotttom, bg="#2C3E50", fg="#EAECEE", font="Helvetica 13")
        self.entryMSG.place(relwidth= 0.74, relheight= 0.06, rely= 0.008, relx = 0.011)
        self.entryMSG.focus()

        self.buttonMessage = Button(self.labelBotttom, text="send", font="Helvetica 13 bold", width=20, bg="#ABB2B9", command= lambda: self.sendButton(self.entryMSG.get()))
        self.buttonMessage.place(relx =0.77, rely = 0.008, relheight= 0.06, width= 0.22)

        self.textCon.config(cursor= "arrow")
        scrollbar = Scrollbar(self.textCon)
        scrollbar.place(relheight= 1, relx= 0.974)
        scrollbar.config(command = self.textCon.yview)
        self.textCon.config(state= DISABLED)

    def sendButton(self, msg):
        self.textCon.config(state= DISABLED)
        self.msg = msg
        self.entryMSG.delete(0, END)
        snd = Thread(target= self.write)
        snd.start()

    def showMessage(self, message):
        self.textCon.config(state= NORMAL)
        self.textCon.insert(0, message + "\n\n")
        self.textCon.config(state= DISABLED)
        self.textCon.see(END)

    def write(self):
        self.textCon.config(state= DISABLED)
        while True:
            message = (f"{self.name}: {self.msg}")
            client.send(message.encode('utf-8'))
            self.showMessage(message)
            break



g = GUI()


#def write():
#    while True:
#        message = input('')
#        client.send(message.encode('utf-8'))

#recieve_thread = Thread(target= receive)
#recieve_thread.start()

#write_thread = Thread(target= write)
#write_thread.start()