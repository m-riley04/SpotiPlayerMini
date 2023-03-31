import spotipy; from spotipy.oauth2 import SpotifyOAuth; import urllib; from PIL import Image, ImageTk
import tkinter as tk; import threading; import io; import os; import datetime; from tkinter import font as tkfont

class LoginApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        #--Colors/Fonts
        self.bgColor = "#050505"
        self.bgColor_light = "#141414"
        self.textColor = "#00ff55"
        self.buttonColor = "#00ff55"
        self.buttonTextColor = "#050505"
        self.buttonColor_hover = "#00a336"
        self.buttonTextColor_hover = "#ebedec"
        self.entryTextColor = "#ebedec"

        #Window Configuration
        self.configure(bg=self.bgColor)
        self.attributes("-topmost", True)
        self.grid_anchor("center")
        self.geometry("300x200")
        self.title("SpotiPlayerMini - Log In")

        #Stack Container Frame
        container = tk.Frame(self)
        container.grid(column=0, row=0)
        container.grid_anchor("center")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginPage, LoadingPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
    
    def destroy_window(self):
        self.destroy()

    def resize_window(self, width, height):
        self.geometry(f"{width}x{height}")

class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        scriptDirectory = os.path.dirname(os.path.abspath(__file__))
        dataDirectory = "user_data"
        clientIDFile_Dir = "client_id.txt"
        clientSecretFile_Dir = "client_secret.txt"
        clientRememberFile_Dir = "remember.txt"

        #Directory Vars
        scriptDirectory = os.path.dirname(os.path.abspath(__file__))
        dataDirectory = "user_data"
        clientIDFile_Dir = "client_id.txt"
        clientSecretFile_Dir = "client_secret.txt"
        clientRememberFile_Dir = "remember.txt"
        
        #--Check for Directory
        if os.path.exists(f"{scriptDirectory}/{dataDirectory}"):
            pass
        else:
            os.mkdir(f"{scriptDirectory}/{dataDirectory}")
        #--Check for Files
        if os.path.exists(f"{dataDirectory}/{clientRememberFile_Dir}") and os.path.exists(f"{dataDirectory}/{clientIDFile_Dir}") and os.path.exists(f"{dataDirectory}/{clientSecretFile_Dir}"):
            pass
        else:
            clientRememberFile = open(f"{dataDirectory}/{clientRememberFile_Dir}", "w").close()
            clientRememberFile = open(f"{dataDirectory}/{clientIDFile_Dir}", "w").close()
            clientRememberFile = open(f"{dataDirectory}/{clientSecretFile_Dir}", "w").close()

        SPOTIFY_REDIRECT_URI = "http://127.0.0.1/callback"
        scope = "user-library-read user-read-playback-state user-modify-playback-state user-read-currently-playing user-follow-modify user-follow-read user-read-playback-position user-top-read user-read-recently-played user-library-modify user-library-read"

        def try_login():
            try:
                loginID_var.set(loginID_entry.get())
                loginSecret_var.set(loginSecret_entry.get())

                #Remember Check
                if rememberMe_var.get() == True:
                    update_remember()
                else:
                    clientSecretFile = open(f"{dataDirectory}/{clientSecretFile_Dir}", "w").close()
                    clientIDFile = open(f"{dataDirectory}/{clientIDFile_Dir}", "w").close()
                    clientRememberFile = open(f"{dataDirectory}/{clientRememberFile_Dir}", "w").close()

                #Authorize and Update Spotify Object
                global sp
                sp = spotipy.Spotify(oauth_manager=SpotifyOAuth(scope=scope, client_id=loginID_var.get(), client_secret=loginSecret_var.get(), redirect_uri=SPOTIFY_REDIRECT_URI, open_browser=True), requests_timeout=10)
                
            except:
                errorLabel = tk.Label(rememberMeFrame, text="Error: blank field", fg="red", bg=controller.bgColor).grid(column=1, row=0)
            else:
                controller.show_frame("LoadingPage")
    
        def try_remember():
            clientRememberFile = bool(open(f"{dataDirectory}/{clientRememberFile_Dir}", "r").read())
            if clientRememberFile == True:
                clientIDFile = str(open(f"{dataDirectory}/{clientIDFile_Dir}", "r").read())
                loginID_entry.insert(index=0, string=clientIDFile)

                clientSecretFile = str(open(f"{dataDirectory}/{clientSecretFile_Dir}", "r").read())
                loginSecret_entry.insert(index=0, string=clientSecretFile)

                rememberMe_check.select()
            else:
                rememberMe_check.deselect()

        def update_remember():
            clientIDFile = open(f"{dataDirectory}/{clientIDFile_Dir}", "w").write(str(loginID_var.get()))
            clientSecretFile = open(f"{dataDirectory}/{clientSecretFile_Dir}", "w").write(str(loginSecret_var.get()))
            clientRememberFile = open(f"{dataDirectory}/{clientRememberFile_Dir}", "w").write(str(rememberMe_var.get))
        
        

        #--Frames
        loginFrame = tk.Frame(self, bg=controller.bgColor)
        labelentryFrame = tk.Frame(loginFrame, bg=controller.bgColor)
        labelFrame = tk.Frame(labelentryFrame, bg=controller.bgColor)
        entryFrame = tk.Frame(labelentryFrame, bg=controller.bgColor)
        buttonFrame = tk.Frame(loginFrame, bg=controller.bgColor)
        rememberMeFrame = tk.Frame(buttonFrame, bg=controller.bgColor)
        
        #--Dynamic Vars
        loginID_var = tk.StringVar()
        loginSecret_var = tk.StringVar()
        rememberMe_var = tk.IntVar()
        
        #--Widgets
        loginID_label = tk.Label(labelFrame, justify="left", text="Client ID: ", font=("Arial Bold", 10), fg=controller.textColor, bg=controller.bgColor)
        loginSecret_label = tk.Label(labelFrame, justify="left", text="Client Secret: ", font=("Arial Bold", 10), fg=controller.textColor, bg=controller.bgColor)
        #rememberMe_label = tk.Label(rememberMeFrame, text="Remember Me", fg=controller.textColor, bg=controller.bgColor)
        loginID_entry = tk.Entry(entryFrame, bg=controller.bgColor_light, fg=controller.entryTextColor)
        loginSecret_entry = tk.Entry(entryFrame, bg=controller.bgColor_light, fg=controller.entryTextColor, show="*")
        rememberMe_check = tk.Checkbutton(rememberMeFrame, variable=rememberMe_var, onvalue=True, offvalue=False, bg=controller.bgColor, fg=controller.buttonColor, activebackground=controller.bgColor, activeforeground=controller.bgColor_light, highlightbackground=controller.entryTextColor, text="Remember Me",  selectcolor=controller.bgColor_light)
        loginAccept_button = tk.Button(buttonFrame, text="Login", command=try_login, bg=controller.buttonColor, fg=controller.buttonTextColor, activebackground=controller.buttonColor_hover, activeforeground=controller.buttonTextColor_hover)
        
        #--Layout
        self.grid_anchor(anchor="center")
        loginFrame.grid(column=0, row=0)
        labelentryFrame.grid(column=0, row=0)
        labelFrame.grid(column=0, row=0)
        loginID_label.grid(column=0, row=0, sticky="w")
        loginSecret_label.grid(column=0, row=1, sticky="w")
        entryFrame.grid(column=1, row=0)
        loginID_entry.grid(column=0, row=0)
        loginSecret_entry.grid(column=0, row=1)
        buttonFrame.grid(column=0, row=1)
        loginAccept_button.grid(column=0, row=1)
        rememberMeFrame.grid(column=0, row=0)
        rememberMe_check.grid(column=0, row=0)
        #rememberMe_label.grid(column=1, row=0)

        
        try_remember()

class LoadingPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        def try_url():
            try:
                sp.current_playback()['item']
                controller.destroy()
            except:
                tk.Label(self, text="Spotify not recently played by a device. Please open and play a track to connect.", fg="red", font=("Arial", 8), wraplength=200, bg=controller.bgColor).grid(column=0, row=0)

        #Widgets
        self.grid_anchor("center")
        self.configure(bg=controller.bgColor)
        acceptButton = tk.Button(self, command=try_url, text="Submit", bg=controller.buttonColor, fg=controller.buttonTextColor, activebackground=controller.buttonColor_hover, activeforeground=controller.buttonTextColor_hover).grid(column=0, row=1)

class PlayerApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        self.playerView = "PlayerPage"

        #--Fonts and Colors
        self.trackFont = "Bahnschrift Bold"
        self.artistFont = "Bahnschrift Light"
        self.textFont = "Bahnschrift"
        self.textColor = "#ffffff"
        self.trackColor = "#ffffff"
        self.artistColor = "#ffffff"
        self.bgColor = "#050505"
        self.buttonColor = "#ffffff"
        self.buttonOnColor = "#4aff5c"
        self.buttonColor_hover = "#99ff99"
        self.buttonTextColor_hover = "#ebedec"
        self.hoverColor = "#88fcb3"
        self.sliderButtonColor = "#1ac41a"

        #Window Configuration
        self.configure(bg=self.bgColor)
        self.attributes("-topmost", True)
        self.geometry("450x200")

        '''
        #Custom Title Bar   
        self.overrideredirect(True)
        def move_app(e):
            self.geometry(f"+{e.x_root}+{e.y_root}")
        title_bar = tk.Frame(self, bg="blue", relief="raised", bd=2, height=10)
        title_bar.grid(column=0, row=0, sticky="nwe")
        #--Bind Title Bar
        title_bar.bind("<B1-Motion>", move_app)
        '''


        #Stack Container Frame
        container = tk.Frame(self)
        container.grid(column=0, row=0)
        container.configure(bg=self.bgColor)
        container.grid_anchor("center")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (PlayerPage, SettingsPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("PlayerPage")

        

    

    def change_color(self, theme):
        if theme == "Default":
            #--Fonts and Colors
            self.trackFont = "Bahnschrift Bold"
            self.artistFont = "Bahnschrift Light"
            self.textFont = "Bahnschrift"
            self.textColor = "#ffffff"
            self.trackColor = "#ffffff"
            self.artistColor = "#ffffff"
            self.bgColor = "#050505"
            self.buttonColor = "#ffffff"
            self.buttonOnColor = "#4aff5c"
            self.buttonColor_hover = "#99ff99"
            self.buttonTextColor_hover = "#ebedec"
            self.hoverColor = "#88fcb3"
            self.sliderButtonColor = "#1ac41a"
        elif theme == "Mainframe":
            #--Fonts and Colors
            self.trackFont = "Bahnschrift Bold"
            self.artistFont = "Bahnschrift Light"
            self.textFont = "Bahnschrift"
            self.textColor = "#ffffff"
            self.trackColor = "#ffffff"
            self.artistColor = "#ffffff"
            self.bgColor = "#050505"
            self.buttonColor = "#4aff5c"
            self.buttonOnColor = "#4aff5c"
            self.buttonColor_hover = "#99ff99"
            self.buttonTextColor_hover = "#ebedec"
            self.hoverColor = "#88fcb3"
            self.sliderButtonColor = "#1ac41a"
        elif theme == "Overheat":
            #--Fonts and Colors
            self.trackFont = "Bahnschrift Bold"
            self.artistFont = "Bahnschrift Light"
            self.textFont = "Bahnschrift"
            self.textColor = "red"
            self.trackColor = "#ffffff"
            self.artistColor = "#ffffff"
            self.bgColor = "white"
            self.buttonColor = "red"
            self.buttonOnColor = "#4aff5c"
            self.buttonColor_hover = "#99ff99"
            self.buttonTextColor_hover = "#ebedec"
            self.hoverColor = "#88fcb3"
            self.sliderButtonColor = "#1ac41a"
        elif theme == "Light":
            #--Fonts and Colors
            self.trackFont = "Bahnschrift Bold"
            self.artistFont = "Bahnschrift Light"
            self.textFont = "Bahnschrift"
            self.textColor = "black"
            self.trackColor = "black"
            self.artistColor = "black"
            self.bgColor = "white"
            self.buttonColor = "gray"
            self.buttonOnColor = "#4aff5c"
            self.buttonColor_hover = "#99ff99"
            self.buttonTextColor_hover = "#ebedec"
            self.hoverColor = "#88fcb3"
            self.sliderButtonColor = "#1ac41a"

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
    
    def destroy_window(self):
        '''Destroys the app window'''
        self.destroy()

class PlayerPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        scriptDirectory = os.path.dirname(os.path.abspath(__file__))
        dataDirectory = "user_data"
        clientIDFile_Dir = "client_id.txt"
        clientSecretFile_Dir = "client_secret.txt"
        clientRememberFile_Dir = "remember.txt"

        def skip():
            sp.next_track(device_id=currentDeviceID) #Skip Forward
            update_force()
            
        def back():
            sp.previous_track(device_id=currentDeviceID) #Skip Backwards
            update_force()
            
        def play():
            sp.start_playback(device_id=currentDeviceID, position_ms=currentSongProgress) #Start/Resume
            update_force()
        
        def pause():
            sp.pause_playback(device_id=currentDeviceID) #Stop
            update_force()
        
        def shuffle():
            currentShuffleState = sp.current_playback()['shuffle_state'] #Get current shuffle state
            currentShuffleStateSet = not currentShuffleState #Set shuffle state toggle
            sp.shuffle(currentShuffleStateSet, currentDeviceID) #Set shuffle state
            if shuffleButton['bg'] == controller.buttonOnColor:
                shuffleButton['bg'] = "#ffffff"
            else:
                shuffleButton['bg'] = controller.buttonOnColor
        
        def seek(self):
            sp.seek_track(device_id=currentDeviceID, position_ms=int(seekSlider.get()))

        def volume(self):
            sp.volume(device_id=currentDeviceID, volume_percent=volumeVar.get())

        def repeat():
            currentRepeatState = sp.current_playback()['repeat_state']

            if currentRepeatState == "context":
                sp.repeat(device_id=currentDeviceID, state="track")
                repeatButton['bg'] = controller.buttonOnColor
                repeatButton.image = repeatAllImage
            elif currentRepeatState == "track": 
                sp.repeat(device_id=currentDeviceID, state="off")
                repeatButton['bg'] = "#ffffff"
                repeatButton.image = repeatImage
            elif currentRepeatState == "off":
                sp.repeat(device_id=currentDeviceID, state="context")
                repeatButton['bg'] = controller.buttonOnColor
                repeatButton.image = repeatImage

        def settings():
            controller.show_frame("SettingsPage")

        #--Update GUI/Data
        def format_time(seconds):
            raw = datetime.timedelta(seconds=seconds)
            m, s = divmod(seconds, 60)
            return f'{m:02d}:{s:02d}'

        def url_to_image(url):
            raw = urllib.request.urlopen(url).read()
            im = Image.open(io.BytesIO(raw))
            im = im.resize((120, 120))
            return im

        def update_colors():
            #--Frames
            mainFrame.configure(bg=controller.bgColor)
            leftFrame.configure(bg=controller.bgColor)
            rightFrame.configure(bg=controller.bgColor)
            controlFrame.configure(bg=controller.bgColor)
            infoFrame.configure(bg=controller.bgColor)
            sliderFrame.configure(bg=controller.bgColor)
            #--Labels
            songLabel.configure(bg=controller.bgColor, fg=controller.trackColor)
            artistLabel.configure(bg=controller.bgColor, fg=controller.artistColor)
            durationLabel.configure(bg=controller.bgColor, fg=controller.textColor)
            progressLabel.configure(bg=controller.bgColor, fg=controller.textColor)
            #--Buttons
            #playButton.configure(bg=controller.buttonColor)
            #pauseButton.configure(bg=controller.buttonColor)
            #forwardButton.configure(bg=controller.buttonColor)
            #backButton.configure(bg=controller.buttonColor)
            #shuffleButton.configure('''bg=controller.buttonColor''')
            #repeatButton.configure('''bg=controller.buttonColor''')
            #settingsButton.configure(bg=controller.buttonColor)

        def update_timer():
            '''Starts a timer that auto-updates the menu every second'''
            threading.Timer(1.0, update_timer).start() #1 sec repeating timer

            #'''
            #Update Data
            currentDeviceID = sp.current_playback()['device']['id'] #Device ID
            currentSong = sp.current_playback()['item']['name'] #Song name
            currentArtist = sp.current_playback()['item']['artists'][0]['name'] #Artist name
            currentSongDuration = sp.current_playback()['item']['duration_ms'] #Duration
            currentSongProgress = sp.current_playback()['progress_ms'] #Current Progress
            currentShuffleState = sp.current_playback()['shuffle_state'] #Shuffle State
            currentSongAlbum = sp.current_playback()['item']['album']['uri'] #Song's album
            currentSongImageURL = sp.current_playback()['item']['album']['images'][0]['url']  #sp.album(currentSongAlbum)['images'][0]['url'] #Album's image URL #<-- THE ISSUE ***********************
            currentRepeatState = sp.current_playback()['repeat_state']

            #Update Text Vars
            songVar.set(currentSong)
            artistVar.set(currentArtist)
            durationVar.set(currentSongDuration)
            progressVar.set(currentSongProgress)

            #Visible Time Text Vars
            tempDurationSeconds = int(currentSongDuration/1000)
            tempProgressSeconds = int(currentSongProgress/1000)
            durationVarVisible.set(format_time(tempDurationSeconds))
            progressVarVisible.set(format_time(tempProgressSeconds))
            
            #Slider
            seekSlider.configure(to=durationVar.get(), variable=progressVar, width=10, length=175, cursor="dot")

            #Update Image
            albumImage = ImageTk.PhotoImage(url_to_image(currentSongImageURL))
            albumLabelImage.configure(image=albumImage)
            albumLabelImage.image = albumImage
            
            #update_colors()
            #'''

            #if sp.current_playback()['item']['name'] != lastPlayedTrack:
            #    update_force()

        def update_force():
            '''Forces an update'''
            #Update Data
            lastPlayedTrack = sp.current_playback()['item']['name']
            currentDeviceID = sp.current_playback()['device']['id'] #Device ID
            currentSong = sp.current_playback()['item']['name'] #Song name
            currentArtist = sp.current_playback()['item']['artists'][0]['name'] #Artist name
            currentSongDuration = sp.current_playback()['item']['duration_ms'] #Duration
            currentSongProgress = sp.current_playback()['progress_ms'] #Current Progress
            currentShuffleState = sp.current_playback()['shuffle_state'] #Shuffle State
            currentSongAlbum = sp.current_playback()['item']['album']['uri'] #Song's album
            currentSongImageURL = sp.current_playback()['item']['album']['images'][0]['url']  #sp.album(currentSongAlbum)['images'][0]['url'] #Album's image URL #<-- THE ISSUE ***********************
            currentRepeatState = sp.current_playback()['repeat_state']

            #Update Text Vars
            songVar.set(currentSong)
            artistVar.set(currentArtist)
            durationVar.set(currentSongDuration)
            progressVar.set(currentSongProgress)

            #Visible Time Text Vars
            tempDurationSeconds = int(currentSongDuration/1000)
            tempProgressSeconds = int(currentSongProgress/1000)
            durationVarVisible.set(format_time(tempDurationSeconds))
            progressVarVisible.set(format_time(tempProgressSeconds))
            
            #Slider
            seekSlider.configure(to=durationVar.get(), variable=progressVar, width=10, length=175, cursor="dot")

            #Update Image
            albumImage = ImageTk.PhotoImage(url_to_image(currentSongImageURL))
            albumLabelImage.configure(image=albumImage)
            albumLabelImage.image = albumImage
            
            update_colors()

        lastDeviceID = open(f"{scriptDirectory}/{dataDirectory}/last_device_ID.txt", "w").close()
        lastDeviceID = open(f"{scriptDirectory}/{dataDirectory}/last_device_ID.txt", "w").write(str(sp.current_playback()['device']['id']))


        #Defaults/Initialize
        lastPlayedTrack = "Golden"
        currentDeviceID = open(f"{scriptDirectory}/{dataDirectory}/last_device_ID.txt", "r").read() #Default Device ID
        currentSong = "Golden" #Default Song name
        currentArtist = "Harry Styles" #Default Artist Name
        currentSongDuration = 0 #Default total duration
        currentSongProgress = 0 #Default progress
        currentShuffleState = False #Default shuffle state
        currentSongAlbum = "spotify:album:7xV2TzoaVc0ycW7fwBwAml" #Default album
        currentSongImageURL = sp.current_playback()['item']['album']['images'][0]['url'] #sp.album(currentSongAlbum)['images'][0]['url']; #Get current song's album cover URL #<-- THE ISSUE ***********************
        currentRepeatState = sp.current_playback()['repeat_state']
        
        firstVolumePercent = sp.current_playback()['device']['volume_percent']

        #--Tk Vars
        songVar = tk.StringVar()
        artistVar = tk.StringVar()
        durationVar = tk.IntVar()
        progressVar = tk.IntVar()
        durationVarVisible = tk.StringVar()
        progressVarVisible = tk.StringVar()
        seekToVar = tk.DoubleVar()
        volumeVar = tk.IntVar()

        #Set Init Percents
        volumeVar.set(firstVolumePercent)

        #--Frames
        mainFrame = tk.Frame(self, bg=controller.bgColor)
        leftFrame = tk.Frame(mainFrame, bg=controller.bgColor)
        rightFrame = tk.Frame(mainFrame, bg=controller.bgColor)
        controlFrame = tk.Frame(leftFrame, bg=controller.bgColor)
        infoFrame = tk.Frame(leftFrame, bg=controller.bgColor)
        sliderFrame = tk.Frame(controlFrame, bg=controller.bgColor)
        
        #--Images
        iconSize = (25, 25)
        albumImage = ImageTk.PhotoImage(url_to_image(currentSongImageURL))
        albumLabelImage = tk.Label(rightFrame, image=albumImage, bg=controller.bgColor)
        playImage_t = Image.open(f"{scriptDirectory}/icons/play.png").resize(iconSize)
        playImage = ImageTk.PhotoImage(playImage_t)
        pauseImage_t = Image.open(f"{scriptDirectory}/icons/pause.png").resize(iconSize)
        pauseImage = ImageTk.PhotoImage(pauseImage_t)
        forwardImage_t = Image.open(f"{scriptDirectory}/icons/forward.png").resize(iconSize)
        forwardImage = ImageTk.PhotoImage(forwardImage_t)
        backImage_t = Image.open(f"{scriptDirectory}/icons/back.png").resize(iconSize)
        backImage = ImageTk.PhotoImage(backImage_t)
        shuffleImage_t = Image.open(f"{scriptDirectory}/icons/shuffle.png").resize(iconSize)
        shuffleImage = ImageTk.PhotoImage(shuffleImage_t)
        repeatImage_t = Image.open(f"{scriptDirectory}/icons/repeat.png").resize(iconSize)
        repeatImage = ImageTk.PhotoImage(repeatImage_t)
        repeatAllImage_t = Image.open(f"{scriptDirectory}/icons/repeatall.png").resize(iconSize)
        repeatAllImage = ImageTk.PhotoImage(repeatAllImage_t)
        settingsImage_t = Image.open(f"{scriptDirectory}/icons/settings.png").resize((15, 15))
        settingsImage = ImageTk.PhotoImage(settingsImage_t)
        
        #--Labels
        songLabel = tk.Label(infoFrame, textvariable=songVar, font=(controller.trackFont, 15), fg=controller.trackColor, wraplength=200, bg=controller.bgColor)
        artistLabel = tk.Label(infoFrame, textvariable=artistVar, font=(controller.artistFont, 8), fg=controller.artistColor, bg=controller.bgColor)
        progressLabel = tk.Label(sliderFrame, textvariable=progressVarVisible, font=(controller.textFont, 10), fg=controller.textColor, bg=controller.bgColor, width=4)
        durationLabel = tk.Label(sliderFrame, textvariable=durationVarVisible, font=(controller.textFont, 10), fg=controller.textColor, bg=controller.bgColor, width=4)
        
        #--Buttons
        playButton = tk.Button(controlFrame, command=play, image=playImage, text="Play", activebackground=controller.buttonColor_hover, highlightcolor=controller.buttonColor_hover); playButton.image = playImage
        pauseButton = tk.Button(controlFrame, command=pause, image=pauseImage, text="Pause", activebackground=controller.buttonColor_hover); pauseButton.image = pauseImage
        forwardButton = tk.Button(controlFrame, command=skip, image=forwardImage, text="Skip", activebackground=controller.buttonColor_hover); forwardButton.image = forwardImage
        backButton = tk.Button(controlFrame, command=back, image=backImage, text="Back", activebackground=controller.buttonColor_hover); backButton.image = backImage
        shuffleButton = tk.Button(controlFrame, command=shuffle, image=shuffleImage, text="Shuffle", activebackground=controller.buttonColor_hover); shuffleButton.image = shuffleImage
        repeatButton = tk.Button(controlFrame, command=repeat, image=repeatImage, text="Repeat", activebackground=controller.buttonColor_hover); repeatButton.image = repeatImage
        settingsButton = tk.Button(leftFrame, command=settings, image=settingsImage, text="Settings", activebackground=controller.buttonColor_hover); settingsButton.image = settingsImage

        #--Slider
        seekSlider = tk.Scale(sliderFrame, showvalue=False, orient="horizontal", from_=0, to=durationVar.get(), variable=seekToVar, command=seek, sliderlength=20, bg=controller.bgColor, activebackground=controller.hoverColor, highlightbackground=controller.bgColor)
        volumeSlider = tk.Scale(rightFrame, showvalue=False, orient="horizontal", from_=0, to=100, variable=volumeVar, sliderlength=10, command=volume, width=5, bg=controller.bgColor, activebackground=controller.hoverColor, highlightbackground=controller.bgColor)

        #--Set First Color
        if currentShuffleState == True:
            shuffleButton['bg'] = controller.buttonOnColor
        else:
            shuffleButton['bg'] = "#ffffff"

        if currentRepeatState != "off":
            repeatButton['bg'] = controller.buttonOnColor
        else:
            shuffleButton['bg'] = "#ffffff"

        #--Update GUI and Data
        update_force()
        update_timer()

        #Align and Organize Layout
        """Left Side"""
        leftFrame.grid(column=0, row=0, padx=5)
        #--Controls                             
        controlFrame.grid(column=0, row=1)
        shuffleButton.grid(column=0, row=1)
        backButton.grid(column=1, row=1)
        pauseButton.grid(column=2, row=1)
        playButton.grid(column=3, row=1)
        forwardButton.grid(column=4, row=1)
        repeatButton.grid(column=5, row=1)
        #--Slider
        sliderFrame.grid(column=0, row=0, columnspan=6, pady=10)
        progressLabel.grid(column=0, row=0)
        seekSlider.grid(column=1, row=0)
        durationLabel.grid(column=2, row=0)
        #--Info Labels
        infoFrame.grid(column=0, row=0)
        songLabel.grid(column=0, row=0, columnspan=2)
        artistLabel.grid(column=0, row=1, columnspan=2)
        """Right Side"""
        rightFrame.grid(column=1, row=0, padx=5)
        #--Images
        albumLabelImage.grid(column=0, row=0)
        volumeSlider.grid(column=0, row=1)
        #--Large Frames
        mainFrame.grid(column=0, row=0)
        settingsButton.grid(column=0, row=0, sticky="nw")

class PlayerPageThin(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        scriptDirectory = os.path.dirname(os.path.abspath(__file__))
        dataDirectory = "user_data"
        clientIDFile_Dir = "client_id.txt"
        clientSecretFile_Dir = "client_secret.txt"
        clientRememberFile_Dir = "remember.txt"

        controller.grid_anchor("center")
        controller.configure(bg=controller.bgColor)
        self.grid_anchor("center")

        def skip():
            sp.next_track(device_id=currentDeviceID) #Skip Forward
            update_force()
            
        def back():
            sp.previous_track(device_id=currentDeviceID) #Skip Backwards
            update_force()
            
        def play():
            sp.start_playback(device_id=currentDeviceID, position_ms=currentSongProgress) #Start/Resume
            update_force()
        
        def pause():
            sp.pause_playback(device_id=currentDeviceID) #Stop
            update_force()
        
        def shuffle():
            currentShuffleState = sp.current_playback()['shuffle_state'] #Get current shuffle state
            currentShuffleStateSet = not currentShuffleState #Set shuffle state toggle
            sp.shuffle(currentShuffleStateSet, currentDeviceID) #Set shuffle state
            if shuffleButton['bg'] == controller.buttonOnColor:
                shuffleButton['bg'] = "#ffffff"
            else:
                shuffleButton['bg'] = controller.buttonOnColor
        
        def seek(self):
            sp.seek_track(device_id=currentDeviceID, position_ms=int(seekSlider.get()))

        def volume(self):
            sp.volume(device_id=currentDeviceID, volume_percent=volumeVar.get())

        def repeat():
            currentRepeatState = sp.current_playback()['repeat_state']

            if currentRepeatState == "context":
                sp.repeat(device_id=currentDeviceID, state="track")
                repeatButton['bg'] = controller.buttonOnColor
                repeatButton.image = repeatAllImage
            elif currentRepeatState == "track": 
                sp.repeat(device_id=currentDeviceID, state="off")
                repeatButton['bg'] = "#ffffff"
                repeatButton.image = repeatImage
            elif currentRepeatState == "off":
                sp.repeat(device_id=currentDeviceID, state="context")
                repeatButton['bg'] = controller.buttonOnColor
                repeatButton.image = repeatImage

        def settings():
            controller.show_frame("SettingsPage")

        #--Update GUI/Data
        def format_time(seconds):
            raw = datetime.timedelta(seconds=seconds)
            m, s = divmod(seconds, 60)
            return f'{m:02d}:{s:02d}'

        def url_to_image(url):
            raw = urllib.request.urlopen(url).read()
            im = Image.open(io.BytesIO(raw))
            im = im.resize((120, 120))
            return im

        def update_colors():
            #--Frames
            mainFrame.configure(bg=controller.bgColor)
            leftFrame.configure(bg=controller.bgColor)
            rightFrame.configure(bg=controller.bgColor)
            controlFrame.configure(bg=controller.bgColor)
            infoFrame.configure(bg=controller.bgColor)
            sliderFrame.configure(bg=controller.bgColor)
            #--Labels
            songLabel.configure(bg=controller.bgColor, fg=controller.trackColor)
            artistLabel.configure(bg=controller.bgColor, fg=controller.artistColor)
            durationLabel.configure(bg=controller.bgColor, fg=controller.textColor)
            progressLabel.configure(bg=controller.bgColor, fg=controller.textColor)
            #--Buttons
            #playButton.configure(bg=controller.buttonColor)
            #pauseButton.configure(bg=controller.buttonColor)
            #forwardButton.configure(bg=controller.buttonColor)
            #backButton.configure(bg=controller.buttonColor)
            #shuffleButton.configure('''bg=controller.buttonColor''')
            #repeatButton.configure('''bg=controller.buttonColor''')
            #settingsButton.configure(bg=controller.buttonColor)

        def update_timer():
            '''Starts a timer that auto-updates the menu every second'''
            threading.Timer(1.0, update_timer).start() #1 sec repeating timer
            #Update Data
            currentDeviceID = sp.current_playback()['device']['id'] #Device ID
            currentSong = sp.current_playback()['item']['name'] #Song name
            currentArtist = sp.current_playback()['item']['artists'][0]['name'] #Artist name
            currentSongDuration = sp.current_playback()['item']['duration_ms'] #Duration
            currentSongProgress = sp.current_playback()['progress_ms'] #Current Progress
            currentShuffleState = sp.current_playback()['shuffle_state'] #Shuffle State
            currentSongAlbum = sp.current_playback()['item']['album']['uri'] #Song's album
            currentSongImageURL = sp.current_playback()['item']['album']['images'][0]['url']  #sp.album(currentSongAlbum)['images'][0]['url'] #Album's image URL #<-- THE ISSUE ***********************
            currentRepeatState = sp.current_playback()['repeat_state']

            #Update Text Vars
            songVar.set(currentSong)
            artistVar.set(currentArtist)
            durationVar.set(currentSongDuration)
            progressVar.set(currentSongProgress)

            #Visible Time Text Vars
            tempDurationSeconds = int(currentSongDuration/1000)
            tempProgressSeconds = int(currentSongProgress/1000)
            durationVarVisible.set(format_time(tempDurationSeconds))
            progressVarVisible.set(format_time(tempProgressSeconds))
            
            #Slider
            seekSlider.configure(to=durationVar.get(), variable=progressVar, width=10, length=175, cursor="dot")

            #Update Image
            albumImage = ImageTk.PhotoImage(url_to_image(currentSongImageURL))
            #albumLabelImage.configure(image=albumImage)
            #albumLabelImage.image = albumImage
            
            update_colors()

        def update_force():
            '''Forces an update'''
            #Update Data
            currentDeviceID = sp.current_playback()['device']['id'] #Device ID
            currentSong = sp.current_playback()['item']['name'] #Song name
            currentArtist = sp.current_playback()['item']['artists'][0]['name'] #Artist name
            currentSongDuration = sp.current_playback()['item']['duration_ms'] #Duration
            currentSongProgress = sp.current_playback()['progress_ms'] #Current Progress
            currentShuffleState = sp.current_playback()['shuffle_state'] #Shuffle State
            currentSongAlbum = sp.current_playback()['item']['album']['uri'] #Song's album
            currentSongImageURL = sp.current_playback()['item']['album']['images'][0]['url'] #sp.album(currentSongAlbum)['images'][0]['url'] #Album's image URL #<-- THE ISSUE ***********************
            
            #Update Text Vars
            songVar.set(currentSong)
            artistVar.set(currentArtist)
            durationVar.set(currentSongDuration)
            progressVar.set(currentSongProgress)

            #Visible Time Text Vars
            tempDurationSeconds = int(currentSongDuration/1000)
            tempProgressSeconds = int(currentSongProgress/1000)
            
            durationVarVisible.set(format_time(tempDurationSeconds))
            progressVarVisible.set(format_time(tempProgressSeconds))
            
            #Slider
            seekSlider.configure(to=durationVar.get(), variable=progressVar, width=10, length=175, cursor="dot")

            #Update GUI Image
            albumImage = ImageTk.PhotoImage(url_to_image(currentSongImageURL))
            #albumLabelImage.configure(image=albumImage)
            #albumLabelImage.image = albumImage

        lastDeviceID = open(f"{scriptDirectory}/{dataDirectory}/last_device_ID.txt", "w").close()
        lastDeviceID = open(f"{scriptDirectory}/{dataDirectory}/last_device_ID.txt", "w").write(str(sp.current_playback()['device']['id']))


        #Defaults/Initialize
        currentDeviceID = open(f"{scriptDirectory}/{dataDirectory}/last_device_ID.txt", "r").read() #Default Device ID
        currentSong = "Golden" #Default Song name
        currentArtist = "Harry Styles" #Default Artist Name
        currentSongDuration = 0 #Default total duration
        currentSongProgress = 0 #Default progress
        currentShuffleState = False #Default shuffle state
        currentSongAlbum = "spotify:album:7xV2TzoaVc0ycW7fwBwAml" #Default album
        currentSongImageURL = sp.current_playback()['item']['album']['images'][0]['url'] #sp.album(currentSongAlbum)['images'][0]['url']; #Get current song's album cover URL #<-- THE ISSUE ***********************
        currentRepeatState = sp.current_playback()['repeat_state']
        
        firstVolumePercent = sp.current_playback()['device']['volume_percent']

        #--Tk Vars
        songVar = tk.StringVar()
        artistVar = tk.StringVar()
        durationVar = tk.IntVar()
        progressVar = tk.IntVar()
        durationVarVisible = tk.StringVar()
        progressVarVisible = tk.StringVar()
        seekToVar = tk.DoubleVar()
        volumeVar = tk.IntVar()

        #Set Init Percents
        volumeVar.set(firstVolumePercent)

        #--Frames
        mainFrame = tk.Frame(self, bg=controller.bgColor)
        leftFrame = tk.Frame(mainFrame, bg=controller.bgColor)
        rightFrame = tk.Frame(mainFrame, bg=controller.bgColor)
        controlFrame = tk.Frame(leftFrame, bg=controller.bgColor)
        infoFrame = tk.Frame(rightFrame, bg=controller.bgColor)
        sliderFrame = tk.Frame(controlFrame, bg=controller.bgColor)
        
        #--Images
        iconSize = (20, 20)
        albumImage = ImageTk.PhotoImage(url_to_image(currentSongImageURL))
        #albumLabelImage = tk.Label(rightFrame, image=albumImage, bg=controller.bgColor)
        playImage_t = Image.open(f"{scriptDirectory}/icons/play.png").resize(iconSize)
        playImage = ImageTk.PhotoImage(playImage_t)
        pauseImage_t = Image.open(f"{scriptDirectory}/icons/pause.png").resize(iconSize)
        pauseImage = ImageTk.PhotoImage(pauseImage_t)
        forwardImage_t = Image.open(f"{scriptDirectory}/icons/forward.png").resize(iconSize)
        forwardImage = ImageTk.PhotoImage(forwardImage_t)
        backImage_t = Image.open(f"{scriptDirectory}/icons/back.png").resize(iconSize)
        backImage = ImageTk.PhotoImage(backImage_t)
        shuffleImage_t = Image.open(f"{scriptDirectory}/icons/shuffle.png").resize(iconSize)
        shuffleImage = ImageTk.PhotoImage(shuffleImage_t)
        repeatImage_t = Image.open(f"{scriptDirectory}/icons/repeat.png").resize(iconSize)
        repeatImage = ImageTk.PhotoImage(repeatImage_t)
        repeatAllImage_t = Image.open(f"{scriptDirectory}/icons/repeatall.png").resize(iconSize)
        repeatAllImage = ImageTk.PhotoImage(repeatAllImage_t)
        settingsImage_t = Image.open(f"{scriptDirectory}/icons/settings.png").resize((15, 15))
        settingsImage = ImageTk.PhotoImage(settingsImage_t)
        
        #--Labels
        songLabel = tk.Label(infoFrame, textvariable=songVar, font=(controller.trackFont, 15), fg=controller.trackColor, wraplength=200, bg=controller.bgColor)
        artistLabel = tk.Label(infoFrame, textvariable=artistVar, font=(controller.artistFont, 8), fg=controller.artistColor, bg=controller.bgColor)
        progressLabel = tk.Label(sliderFrame, textvariable=progressVarVisible, font=(controller.textFont, 10), fg=controller.textColor, bg=controller.bgColor, width=4)
        durationLabel = tk.Label(sliderFrame, textvariable=durationVarVisible, font=(controller.textFont, 10), fg=controller.textColor, bg=controller.bgColor, width=4)
        
        #--Buttons
        playButton = tk.Button(controlFrame, command=play, image=playImage, text="Play", activebackground=controller.buttonColor_hover, highlightcolor=controller.buttonColor_hover); playButton.image = playImage
        pauseButton = tk.Button(controlFrame, command=pause, image=pauseImage, text="Pause", activebackground=controller.buttonColor_hover); pauseButton.image = pauseImage
        forwardButton = tk.Button(controlFrame, command=skip, image=forwardImage, text="Skip", activebackground=controller.buttonColor_hover); forwardButton.image = forwardImage
        backButton = tk.Button(controlFrame, command=back, image=backImage, text="Back", activebackground=controller.buttonColor_hover); backButton.image = backImage
        shuffleButton = tk.Button(controlFrame, command=shuffle, image=shuffleImage, text="Shuffle", activebackground=controller.buttonColor_hover); shuffleButton.image = shuffleImage
        repeatButton = tk.Button(controlFrame, command=repeat, image=repeatImage, text="Repeat", activebackground=controller.buttonColor_hover); repeatButton.image = repeatImage
        settingsButton = tk.Button(rightFrame, command=settings, image=settingsImage, text="Settings", activebackground=controller.buttonColor_hover); settingsButton.image = settingsImage

        #--Slider
        seekSlider = tk.Scale(sliderFrame, showvalue=False, orient="horizontal", from_=0, to=durationVar.get(), variable=seekToVar, command=seek, sliderlength=20, bg=controller.bgColor, activebackground=controller.hoverColor, highlightbackground=controller.bgColor)
        #volumeSlider = tk.Scale(rightFrame, showvalue=False, orient="horizontal", from_=0, to=100, variable=volumeVar, sliderlength=10, command=volume, width=5, bg=controller.bgColor, activebackground=controller.hoverColor, highlightbackground=controller.bgColor)

        #--Set First Color
        if currentShuffleState == True:
            shuffleButton['bg'] = controller.buttonOnColor
        else:
            shuffleButton['bg'] = "#ffffff"

        if currentRepeatState != "off":
            repeatButton['bg'] = controller.buttonOnColor
        else:
            shuffleButton['bg'] = "#ffffff"

        #--Update GUI and Data
        update_force()
        update_timer()

        #Align and Organize Layout
        """Left Side"""
        leftFrame.grid(column=0, row=0, padx=5)
        #--Controls                             
        controlFrame.grid(column=0, row=1)
        shuffleButton.grid(column=0, row=1)
        backButton.grid(column=1, row=1)
        pauseButton.grid(column=2, row=1)
        playButton.grid(column=3, row=1)
        forwardButton.grid(column=4, row=1)
        repeatButton.grid(column=5, row=1)
        #--Slider
        sliderFrame.grid(column=0, row=0, columnspan=6, pady=10)
        progressLabel.grid(column=0, row=0)
        seekSlider.grid(column=1, row=0)
        durationLabel.grid(column=2, row=0)
        #--Info Labels
        infoFrame.grid(column=0, row=0)
        songLabel.grid(column=0, row=0, columnspan=2)
        artistLabel.grid(column=0, row=1, columnspan=2)
        """Right Side"""
        rightFrame.grid(column=1, row=0, padx=5)
        #--Images
        #albumLabelImage.grid(column=0, row=0)
        #volumeSlider.grid(column=0, row=1)
        #--Large Frames
        mainFrame.grid(column=0, row=0)
        mainFrame.grid_anchor("center")
        settingsButton.grid(column=0, row=0, sticky="ne")

class SettingsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        controller.grid_anchor("center")
        self.grid_anchor("center")

        def player():
            controller.show_frame(controller.playerView)
        
        def change_colors(self):
            print(colorChosen.get())
            controller.change_color(colorChosen.get())
            print(controller.bgColor)
            #Configure Appn Window Colors
            controller.configure(bg=controller.bgColor)
            #Configure Settings Page Colors
            homeButton.configure(bg=controller.buttonColor)
            
        def recent_track(self):
            print(recentlyPlayedTracksSelected.get())
            sp.add_to_queue(uri=recentlyPlayedTracksLinks[recentlyPlayedTracks.index(recentlyPlayedTracksSelected.get())])
        
        def recent_playlist(self):
            print(userPlaylistsSelected.get())
            sp.start_playback(context_uri=userPlaylistsLinks[userPlaylists.index(userPlaylistsSelected.get())])

        def size_change(self):
            if sizeSelected.get() == "Full Player":
                controller.playerView = "PlayerPage"
                controller.geometry("450x200")
            elif sizeSelected.get() == "Thin":
                controller.playerView = "PlayerPageThin"
                controller.geometry("400x60")
        
        def toggle_fullscreen(self):
            pass

        colorOptions = ["Default", "Light", "Mainframe", "Overheat"]
        colorChosen = tk.StringVar()
        colorChosen.set(colorOptions[0])
        
        recentlyPlayedTracks = []
        recentlyPlayedTracksLinks = []
        for i in sp.current_user_recently_played(limit=10)['items']:
            recentlyPlayedTracks.append(i['track']['name'])
            recentlyPlayedTracksLinks.append(i['track']['uri'])
        recentlyPlayedTracksSelected = tk.StringVar()

        userPlaylists = []
        userPlaylistsLinks = []
        for i in sp.current_user_playlists(limit=10)['items']:
            userPlaylists.append(i['name'])
            userPlaylistsLinks.append(i['uri'])
        userPlaylistsSelected = tk.StringVar()
        
        sizeOptions = ["Full Player", "Thin"]
        sizeSelected = tk.StringVar()
        sizeSelected.set(sizeOptions[0])

        #Widgets
        self.configure(bg=controller.bgColor)
        homeButton = tk.Button(self, text="Home", command=player, bg=controller.buttonColor)
        colorDropdown = tk.OptionMenu(self, colorChosen, colorOptions[0], *colorOptions[1:], command=change_colors)
        recentlyPlayedTracksDropdown = tk.OptionMenu(self, recentlyPlayedTracksSelected, recentlyPlayedTracks[0], *recentlyPlayedTracks[1:], command=recent_track)
        userPlaylistsDropdown = tk.OptionMenu(self, userPlaylistsSelected, userPlaylists[0], *userPlaylists[1:], command=recent_playlist)
        sizeDropdown = tk.OptionMenu(self, sizeSelected, sizeOptions[0], *sizeOptions[1:], command=size_change)
        
        #Layout
        homeButton.grid(column=0, row=0)
        colorDropdown.grid(column=1, row=0)
        recentlyPlayedTracksDropdown.grid(column=2, row=0)
        userPlaylistsDropdown.grid(column=3, row=0)
        sizeDropdown.grid(column=1, row=1)