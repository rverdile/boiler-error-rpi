import Tkinter as tk     
import tkFont as tkfont  
import functions as fn

#--Colors--#
light_maroon="#c83b5d"
maroon="#b7284b"
maroon_highlight="#b2526a"
dark_maroon="#81253c"
dark_maroon_highlight="#834353"
black_maroon="#441f28"

class gui(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold")
        self.geometry("464x320")
        self.title("Settings")

        container = tk.Frame(self,bg=maroon)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, ChangeRecipients, PhoneNumbers, EmailList, ChangeAlertMessage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.config(bg=dark_maroon)


            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Settings", font=controller.title_font,bg=maroon,fg="white")
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Recipients",bg=maroon,activebackground=maroon_highlight,highlightbackground=black_maroon,
                            bd=2,highlightthickness=4,fg="white",activeforeground="gray",command=lambda: controller.show_frame("ChangeRecipients"),
                            font="Helvetica 18")
        #button1.config(highlightbackground=dark_maroon)
        button2 = tk.Button(self, text="Alert Message",bg=maroon,activebackground=maroon_highlight,highlightbackground=black_maroon,
                            bd=2,highlightthickness=4,fg="white",activeforeground="gray",command=lambda: controller.show_frame("ChangeAlertMessage"),
                            font="Helvetica 18")
        button1.place(height=60,width=235,rely=0.30,relx=0.26)
        button2.place(height=60,width=235,rely=0.55,relx=0.26)


class ChangeRecipients(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Change Recipients", font=controller.title_font,bg=maroon,fg="white")
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Phone Numbers",bg=maroon,activebackground=maroon_highlight,highlightbackground=black_maroon,
                            bd=2,highlightthickness=4,fg="white",activeforeground="gray",command=lambda: controller.show_frame("PhoneNumbers"),
                            font="Helvetica 18")
       
        button2 = tk.Button(self, text="Emails",bg=maroon,activebackground=maroon_highlight,highlightbackground=black_maroon,
                            bd=2,highlightthickness=4,fg="white",activeforeground="gray",command=lambda: controller.show_frame("EmailList"),
                            font="Helvetica 18")
        button1.place(height=60,width=235,rely=0.30,relx=0.26)
        button2.place(height=60,width=235,rely=0.55,relx=0.26)

        #back to start page
        button5 = tk.Button(self,text="Back to Start Page",bg=maroon,activebackground=maroon_highlight,font="Helvetica 9",fg="white",
                            activeforeground="gray",highlightthickness=4,command=lambda:  controller.show_frame("StartPage"),
                            highlightbackground=black_maroon)
        button5.place(height=25,width=120,relx=.7,rely=.92)


class PhoneNumbers(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller

        #--Displaying current list--#
        numbers = fn.getPhoneNumbers()
        numbersText = [""]*100 #preallocate numbers list

        label = tk.Label(self, text="Numbers on list (first 8)               Example (U.S.): +12223334444", font="Helvetica 11 bold",bg=maroon,fg="white")
        label.place(height=17,width=435,relx=.06,rely=.35)

        for i in range(len(numbers)):
            numbersText[i] = numbers[i]

        index=0
        body=[]
        for i in range(2):
            for j in range(4):
                body.append(tk.Label(self,text=numbersText[index],height=1,width=30,bg=maroon,font=("Helvetica 10"),fg="white"))
                body[index].place(relx=(.058+(i-(i*.53))),rely=(.46+(j-(j*.88))))
                index=index+1

        #--entry--#
        entry = tk.Entry(self,font="Helvetica 25")
        entry.place(height=40,width=440,relx=.05,rely=.02)

        #--Buttons--#
        buttonAdd=tk.Button(self,text="Add Number",bg=maroon,activebackground=maroon_highlight,font="Helvetica 20",fg="white",
                            activeforeground="gray",highlightthickness=4,command=lambda:  fn.addString(entry.get(),body,'/home/pi/Alert_System/phone_numbers.txt'),
                            highlightbackground=black_maroon)
        buttonAdd.place(height=40,width=210,relx=0.05,rely=.18)
        buttonRem=tk.Button(self,text="Remove Number",bg=maroon,activebackground=maroon_highlight,font="Helvetica 19",fg="white",
                            activeforeground="gray",highlightthickness=4,command=lambda:  fn.delString(entry.get(),body,'/home/pi/Alert_System/phone_numbers.txt'),
                            highlightbackground=black_maroon)
        buttonRem.place(height=40,width=210,relx=0.51,rely=.18)

        #back to start page
        button5 = tk.Button(self,text="Back to Start Page",bg=maroon,activebackground=maroon_highlight,font="Helvetica 9",fg="white",
                            activeforeground="gray",highlightthickness=4,command=lambda:  controller.show_frame("StartPage"),
                            highlightbackground=black_maroon)
        button5.place(height=25,width=120,relx=.7,rely=.92)

class EmailList(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller

        #--Displaying current list--#
        emails = fn.getEmailList()
        emailsText = [""]*100 #preallocate email list

        label = tk.Label(self, text="Emails on list (first 8)", font="Helvetica 12 bold",bg=maroon,fg="white")
        label.pack(side="top",pady=87)

        for i in range(len(emails)):
            emailsText[i] = emails[i]

        index=0
        body=[]
        for i in range(2):
            for j in range(4):
                body.append(tk.Label(self,text=emailsText[index],height=1,width=30,bg=maroon,font=("Helvetica 10"),fg="white"))
                body[index].place(relx=(.058+(i-(i*.53))),rely=(.43+(j-(j*.88))))
                index=index+1

        #--entry--#
        entry = tk.Entry(self,font="Helvetica 25")
        entry.place(height=40,width=440,relx=.05,rely=.02)

        #--Buttons--#
        buttonAdd=tk.Button(self,text="Add email",bg=maroon,activebackground=maroon_highlight,font="Helvetica 20",fg="white",
                            activeforeground="gray",highlightthickness=4,command=lambda:  fn.addString(entry.get(),body,'/home/pi/Alert_System/emails.txt'),
                            highlightbackground=black_maroon)
        buttonAdd.place(height=40,width=210,relx=0.05,rely=.18)
        buttonRem=tk.Button(self,text="Remove email",bg=maroon,activebackground=maroon_highlight,font="Helvetica 20",fg="white",
                            activeforeground="gray",highlightthickness=4,command=lambda:  fn.delString(entry.get(),body,'/home/pi/Alert_System/emails.txt'),
                            highlightbackground=black_maroon)
        buttonRem.place(height=40,width=210,relx=0.51,rely=.18)

        #back to start page
        button5 = tk.Button(self,text="Back to Start Page",bg=maroon,activebackground=maroon_highlight,font="Helvetica 9",fg="white",
                            activeforeground="gray",highlightthickness=4,command=lambda:  controller.show_frame("StartPage"),
                            highlightbackground=black_maroon)
        button5.place(height=25,width=120,relx=.7,rely=.92)

class ChangeAlertMessage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller

        #update location 
        entry0 = tk.Entry(self,font="Helvetica 13")
        entry0.place(height=27,width=440,relx=.05,rely=.01)

        button0 = tk.Button(self,text="Update Location",bg=maroon,activebackground=maroon_highlight,font="Helvetica 12",fg="white",
                            activeforeground="gray",highlightthickness=2,command=lambda:  fn.updateFile(entry0.get(),"/home/pi/Alert_System/location.txt"),
                            highlightbackground=black_maroon)
        button0.place(height=21,width=150,relx=.05,rely=.12)

        #update error1
        entry1 = tk.Entry(self,font="Helvetica 13")
        entry1.place(height=27,width=440,relx=.05,rely=.21)

        button1 = tk.Button(self,text="Update Error 1",bg=maroon,activebackground=maroon_highlight,font="Helvetica 12",fg="white",
                            activeforeground="gray",highlightthickness=2,command=lambda:  fn.updateFile(entry1.get(),"/home/pi/Alert_System/error_1.txt"),
                            highlightbackground=black_maroon)
        button1.place(height=21,width=150,relx=.05,rely=.32)

        #N/A
        button1_na = tk.Button(self,text="N/A",bg=maroon,activebackground=maroon_highlight,font="Helvetica 12",fg="white",
        					activeforeground="gray",highlightthickness=2,command=lambda: fn.updateFile("$%gAd.2","/home/pi/Alert_System/error_1.txt"),
        					highlightbackground=black_maroon)
        button1_na.place(height=21,width=50,relx=.47,rely=.32)

        #update error2
        entry2 = tk.Entry(self,font="Helvetica 13")
        entry2.place(height=27,width=440,relx=.05,rely=.41)

        button2 = tk.Button(self,text="Update Error 2",bg=maroon,activebackground=maroon_highlight,font="Helvetica 12",fg="white",
                            activeforeground="gray",highlightthickness=2,command=lambda:  fn.updateFile(entry2.get(),"/home/pi/Alert_System/error_2.txt"),
                            highlightbackground=black_maroon)
        button2.place(height=21,width=150,relx=.05,rely=.52)


        button2_na = tk.Button(self,text="N/A",bg=maroon,activebackground=maroon_highlight,font="Helvetica 12",fg="white",
        					activeforeground="gray",highlightthickness=2,command=lambda: fn.updateFile("$%gAd.2","/home/pi/Alert_System/error_2.txt"),
        					highlightbackground=black_maroon)
        button2_na.place(height=21,width=50,relx=.47,rely=.52)

        #update error3
        entry3 = tk.Entry(self,font="Helvetica 13")
        entry3.place(height=27,width=440,relx=.05,rely=.61)

        button3 = tk.Button(self,text="Update Error 3",bg=maroon,activebackground=maroon_highlight,font="Helvetica 12",fg="white",
                            activeforeground="gray",highlightthickness=2,command=lambda:  fn.updateFile(entry3.get(),"/home/pi/Alert_System/error_3.txt"),
                            highlightbackground=black_maroon)
        button3.place(height=21,width=150,relx=.05,rely=.72)


        button3_na = tk.Button(self,text="N/A",bg=maroon,activebackground=maroon_highlight,font="Helvetica 12",fg="white",
        					activeforeground="gray",highlightthickness=2,command=lambda: fn.updateFile("$%gAd.2","/home/pi/Alert_System/error_3.txt"),
        					highlightbackground=black_maroon)
        button3_na.place(height=21,width=50,relx=.47,rely=.72)

        #update error4
        entry4 = tk.Entry(self,font="Helvetica 13")
        entry4.place(height=27,width=440,relx=.05,rely=.81)

        button4 = tk.Button(self,text="Update Error 4",bg=maroon,activebackground=maroon_highlight,font="Helvetica 12",fg="white",
                            activeforeground="gray",highlightthickness=2,command=lambda:  fn.updateFile(entry4.get(),"/home/pi/Alert_System/error_4.txt"),
                            highlightbackground=black_maroon)
        button4.place(height=21,width=150,relx=.05,rely=.92)


        button4_na = tk.Button(self,text="N/A",bg=maroon,activebackground=maroon_highlight,font="Helvetica 12",fg="white",
        					activeforeground="gray",highlightthickness=2,command=lambda: fn.updateFile("$%gAd.2","/home/pi/Alert_System/error_4.txt"),
        					highlightbackground=black_maroon)
        button4_na.place(height=21,width=50,relx=.47,rely=.92)

        #back to start page
        button5 = tk.Button(self,text="Back to Start Page",bg=maroon,activebackground=maroon_highlight,font="Helvetica 9",fg="white",
                            activeforeground="gray",highlightthickness=2,command=lambda:  controller.show_frame("StartPage"),
                            highlightbackground=black_maroon)
        button5.place(height=25,width=120,relx=.7,rely=.92)


if __name__ == "__main__":
    app = gui()
    app.mainloop()
