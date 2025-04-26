import speedtest
from tkinter.ttk import *
from tkinter import *
import threading


root = Tk()
root.title("Test Internet Speed")
root.geometry('480x360')
root.resizable(False, False)
root.configure(bg="#ffffff")

# design
Label(root, text ='Test Internet Speed', bg='#ffffff', fg='#404042', font = 'arial 23 bold').pack()
Label(root, text ='by Aadil Faheem', bg='#fff', fg='#404042', font = 'arial 10 italic').pack(side =BOTTOM)

# label to show internet speed
down_label = Label(root, text="⏬ Download Speed - ", bg='#fff', font = 'arial 15 bold')
down_label.place(x = 120, y= 80)
up_label = Label(root, text="⏫ Upload Speed - ", bg='#fff', font = 'arial 15 bold')
up_label.place(x = 120, y= 120)
ping_label = Label(root, text="Your Ping - ", bg='#fff', font = 'arial 15 bold')
ping_label.place(x = 120, y= 160)

# check speed function
def check_speed():
    global download_speed, upload_speed
    speed_test= speedtest.Speedtest()
    download= speed_test.download()
    upload = speed_test.upload()

    download_speed = round(download / (10 ** 6), 2)
    upload_speed = round(upload / (10 ** 6), 2)
    
# function for progress bar and update text
def update_text():
    thread=threading.Thread(target=check_speed, args=())
    thread.start()
    progress=Progressbar(root, orient=HORIZONTAL,
                         length=210, mode='indeterminate')
    progress.place(x = 120, y = 260)
    progress.start()
    while thread.is_alive():
        root.update()
        pass
    down_label.config(text="⏬ Download Speed - "+str(download_speed)+"Mbps")
    up_label.config(text="⏫ Upload Speed - "+str(upload_speed)+"Mbps")

    # Fetch the ping
    st.get_servers([])
    ping = st.results.ping
    
    ping_label.config(text="Your Ping is - "+str(ping))
    
    progress.stop()
    progress.destroy()

# button for call to function
button = Button(root, text="Check Speed ▶", width=30, bd = 0, bg = 'green', fg='#fff', pady = 5, command=update_text)
button.place(x=120, y = 200)
root.mainloop()