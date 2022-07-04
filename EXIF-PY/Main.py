"""
Create EXIF Tkinter program
Able to input photos and get back exif data like camera make, model, software and geolocation data
Get a map visualisation of the Lat/Long from the tags
Maybe use folium just for saving locations to viewable file, or use a screenshot module
"""

from GPSPhoto import gpsphoto   # For getting LatLong
from tkinter import *           # For GUI components
import tkintermapview           # For the map widget used to display location
from tkinter import ttk         # For GUI components
import tkinter.filedialog as filedialog     # For the user's file selection
from Exif_reader import ExifTags        # For getting non-GPS related EXIF data (make, model, software, date)


class ExifGui():

    def __init__(self):
        self.__title = "EXIF-PY"
        self.__screen_geometry = "1000x900"
        self.__mainScreenFile = "EXIF information.png"
        self.__MainWindow = Tk()

        self.filename = StringVar()

    def ClearWindow(self):
        window = self.__MainWindow
        _list = window.winfo_children()

        for item in _list:
            item.destroy()

    def screen(self):
        self.ClearWindow()

        mainScreen = self.__MainWindow
        mainScreen.title(self.__title)
        mainScreen.geometry(self.__screen_geometry)
        mainScreen.option_add('*tearOff', False)

        mainScreen.attributes("-topmost", False)
        mainScreen.resizable(False, False)
        background = ttk.Label(mainScreen, text="")
        background.place(x=0, y=0)

        logo = PhotoImage(file=self.__mainScreenFile, master=mainScreen)
        background.config(image=logo)
        background.img = logo
        background.config(image=background.img)

        browse_btn = ttk.Button(mainScreen, text="Browse files", command=self.file_browse)
        browse_btn.place(x=883, y=732)

        go_btn = ttk.Button(mainScreen, text="Find", command=self.screen_two)
        go_btn.place(x=883, y=758)

        my_label = LabelFrame(mainScreen)
        my_label.pack(pady=20)

        map_widget = tkintermapview.TkinterMapView(my_label, width=800, height=600)
        map_widget.set_zoom(1)
        map_widget.pack()

        mainScreen.mainloop()

    def screen_two(self):
        self.ClearWindow()

        mainScreen = self.__MainWindow
        mainScreen.title(self.__title)
        mainScreen.geometry(self.__screen_geometry)

        mainScreen.attributes("-topmost", False)
        mainScreen.resizable(False, False)
        background = ttk.Label(mainScreen, text="")
        background.place(x=0, y=0)

        logo = PhotoImage(file=self.__mainScreenFile, master=mainScreen)
        background.config(image=logo)
        background.img = logo
        background.config(image=background.img)

        my_label = LabelFrame(mainScreen)
        my_label.pack(pady=20)

        map_widget = tkintermapview.TkinterMapView(my_label, width=800, height=600)
        map_widget.set_zoom(20)
        map_widget.pack()

        data = gpsphoto.getGPSData(self.filename.get())
        map_widget.set_position(data['Latitude'], data['Longitude'])
        map_widget.set_marker(data['Latitude'], data['Longitude'], text=self.filename.get())

        browse_btn = ttk.Button(mainScreen, text="Back", command=self.screen)
        browse_btn.place(x=883, y=742)

        e = ExifTags()
        tags = e.read_image_tags(self.filename.get())

        lbl_make = ttk.Label(mainScreen, text=tags[0], background="#FFFFFF", foreground="#000000", font=("Roboto", 14))
        lbl_make.place(x=139, y=704)
        lbl_model = ttk.Label(mainScreen, text=tags[1], background="#FFFFFF", foreground="#000000", font=("Roboto", 14))
        lbl_model.place(x=139, y=791)
        lbl_software = ttk.Label(mainScreen, text=tags[2], background="#FFFFFF", foreground="#000000", font=("Roboto", 14))
        lbl_software.place(x=542, y=791)
        lbl_time = ttk.Label(mainScreen, text=tags[3], background="#FFFFFF", foreground="#000000", font=("Roboto", 14))
        lbl_time.place(x=503, y=704)

    def file_browse(self):
        filetypes = (
            ('PNG Files', '*.png'),
            ('JPEG Files', '*.jpeg'),
            ('JPEG Files', '*.jpg'),
            ('TIFF Files', '*.tif'),
            ('TIFF Files', '*.tiff'),
            ('Bitmap files', '*.bmp')
        )
        cwd = os.getcwd()
        filename = filedialog.askopenfilename(title="Choose a file", initialdir=cwd, filetypes=filetypes)
        self.filename.set(filename)


c = ExifGui()
c.screen()
