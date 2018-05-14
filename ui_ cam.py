import threading
import time
from tkinter import *
import cv2
from PIL import Image, ImageTk
import cam_new


class Window:
    # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):

        # root window created. Here, that would be the only window, but
        # you can later have windows within windows.
        self.root = Tk()
        self.root.geometry("640x500")

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
        self.root.title("GUI")

        # allowing the widget to take the full space of the root window
        # self.root.pack(fill=BOTH, expand=1)

        # self.destructor function gets fired when the window is closed
        self.root.protocol('WM_DELETE_WINDOW', self.destructor)

        # create a button, that when pressed, will take the current
        # frame and save it to file
        global EntryC
        EntryC=Entry(self.root,width=20,font='Arial 16')
        EntryC.pack(side="bottom")
        btn = Button(self.root, text="TRW",
                     command=self.TRW)
        btn.pack(side="bottom", fill="both", expand="no", padx=10,
                 pady=1)
        btn = Button(self.root, text="TRH",
                     command=self.TRH)
        btn.pack(side="bottom", fill="both", expand="yes", padx=10,
                 pady=1)
        btn = Button(self.root, text="LW",
                     command=self.LW)
        btn.pack(side="bottom", fill="both", expand="yes", padx=10,
                 pady=1)
        btn = Button(self.root, text="LH",
                     command=self.LH)
        btn.pack(side="bottom", fill="both", expand="yes", padx=10,
                 pady=1)
        
        # start a thread that constantly pools the video sensor for
        # the most recently read frame
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()
       

    def destructor(self):
        """ Destroy the root object and release all resources """
        print("[INFO] closing...")
        self.root.destroy()
        self.stopEvent.set()
        cv2.destroyAllWindows()  # it is not mandatory in this application

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

    def TRW(self):
        cap = cv2.VideoCapture(1)
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('capture.jpg', gray)
        # self.calculator.gray = self.gray
        ma=cam_new.doe()
        res=cam_new.TRW(ma)
        EntryC.insert(0,'Результат:'+str(res) )
    def TRH(self):
        cap = cv2.VideoCapture(1)
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('capture.jpg', gray)
        # self.calculator.gray = self.gray
        ma=cam.doe()
        cam.TRH(ma)
    def LW(self):
        cap = cv2.VideoCapture(1)
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('capture.jpg', gray)
        # self.calculator.gray = self.gray
        ma=cam.doe()
        cam.line_W(ma)
    def LH(self):
        cap = cv2.VideoCapture(1)
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('capture.jpg', gray)
        # self.calculator.gray = self.gray
        ma=cam.doe()
        cam.line_H(ma)
        print('jhghv')
# creation of an instance
app = Window()

# mainloop
app.root.mainloop()
