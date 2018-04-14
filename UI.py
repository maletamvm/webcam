import threading
import time
from tkinter import *
import cv2
from PIL import Image, ImageTk


# Here, we are creating our class, Window, and inheriting from the Frame
# class. Frame is a class from the tkinter module. (see Lib/tkinter/__init__)
class Window(Frame):
    # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):
        # parameters that you want to send through the Frame class.
        Frame.__init__(self, master)

        # reference to the master widget, which is the tk window
        self.master = master

        self.gray = None
        self.thread = None
        self.panel = None
        self.stopEvent = None

        # with that, we want to then run init_window, which doesn't yet exist
        self.init_window()

    # Creation of init_window
    def init_window(self):
        # changing the title of our master widget
        self.master.title("GUI")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # creating a button instance
        quitButton = Button(self, text="Exit", command=self.client_exit)
        # placing the button on my window
        quitButton.pack(side="right", padx=10, pady=10)

        # create a button, that when pressed, will take the current
        # frame and save it to file
        btn = Button(self, text="Snapshot!",
                         command=self.takeSnapshot)
        btn.pack(side="bottom", fill="both", expand="yes", padx=10,
                 pady=10)

        # start a thread that constantly pools the video sensor for
        # the most recently read frame
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()

    def client_exit(self):
        self.stopEvent.set()
        exit()

    def videoLoop(self):
        cap = cv2.VideoCapture(0)
        try:
            # keep looping over frames until we are instructed to stop
            while not self.stopEvent.is_set():

                # Capture frame-by-frame
                ret, frame = cap.read()

                # Our operations on the frame come here
                self.gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                pil_im = Image.fromarray(self.gray)
                render = ImageTk.PhotoImage(pil_im)

                # if the panel is not None, we need to initialize it
                if self.panel is None:
                    self.panel = Label(image=render)
                    self.panel.image = render
                    self.panel.pack(side="left", padx=10, pady=10)

                # otherwise, simply update the panel
                else:
                    self.panel.configure(image=render)
                    self.panel.image = render
                time.sleep(0.1)

        except RuntimeError as e:
            print("[INFO] caught a RuntimeError")

    def takeSnapshot(self):
        cv2.imwrite('capture.jpg', self.gray)

# root window created. Here, that would be the only window, but
# you can later have windows within windows.
root = Tk()
root.geometry("1000x500")

# creation of an instance
app = Window(root)

# mainloop
root.mainloop()