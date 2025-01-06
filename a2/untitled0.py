import requests #Importing requests mdule to make http requests
import base64 #Importing base64 to encode or decode data
import tkinter as tk #Importing tkinter module
from tkinter import messagebox #Importing tkinter module
from PIL import Image, ImageTk #Importing modules from PIL library to generate images
from io import BytesIO #Importing BytesIO to work with binary data
from tkinter import ttk #Importing tkinter module

# Spotify api credentials
CLIENT_ID = '15b7295fa22a4ee1ae8340c3d2506cb6'
CLIENT_SECRET = '9d7ed2fde08b404eb41ed5e4141a7006'

# Function to get Spotify access token
def get_access_token():
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    }
    data = {"grant_type": "client_credentials"}
    response = requests.post(url, headers=headers, data=data)
    response_data = response.json()
    return response_data.get("access_token")

ACCESS_TOKEN = get_access_token() # Calling the access token function

def clear_frame(frame): # To clear the widget of the frame
    for widget in frame.winfo_children():
        widget.destroy()

# Creating function to add background image
def add_background_image(frame, image_path):
    """Adds a background image to the given frame."""
    try:
        bg_image = Image.open(image_path).resize((800, 600))
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(frame, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except FileNotFoundError:
        messagebox.showerror("Error", "Background image not found. Please check the file path.")

# Welcome Page
def welcome_page():
    clear_frame(main_frame)
    add_background_image(main_frame, "aura2.jpg")  

    welcome_label = tk.Label(main_frame, 
                             text="WELCOME TO SPOTIFY APP", 
                             font=("Helvetica", 35, "bold"), 
                             bg="#b2aaa5", 
                             fg="white")
    welcome_label.place(relx=0.5, rely=0.3, anchor="center")

    sub_label = tk.Label(main_frame, 
                         text="Discover albums, top tracks, and lyrics!", 
                         font=("Helvetica", 14), 
                         bg="#b2aaa5", 
                         fg="white")
    sub_label.place(relx=0.5, rely=0.4, anchor="center")

    # Adding "Get Started" Button
    start_button = tk.Button(main_frame, 
                              text="Get Started", 
                              command=album_search_page, 
                              font=("Helvetica", 14), 
                              bg="#566779", 
                              fg="white", 
                              padx=15, 
                              pady=10)
    start_button.place(relx=0.5, rely=0.6, anchor="center")

# 1st page (album search)
def album_search_page():
    clear_frame(main_frame)
    add_background_image(main_frame, "aura2.jpg")  #adding the background image

    tk.Label(main_frame, text="Album Search", font=("Helvetica", 16, "bold"), bg="#b2aaa5", fg="white").pack(pady=10)
    tk.Label(main_frame, text="Enter Album Name:", font=("Helvetica", 12), bg="#b2aaa5", fg="white").pack(pady=5)

    album_entry = tk.Entry(main_frame, width=40)
    album_entry.pack(pady=5)

    def search_album():
        album_name = album_entry.get()
        if not album_name:
            messagebox.showerror("Error", "Please enter an album name.")
            return

        url = f"https://api.spotify.com/v1/search?q={album_name}&type=album&limit=1"
        headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            messagebox.showerror("Error", "Failed to fetch album data. Check your API token.")
            return

        data = response.json()
        if 'albums' in data and data['albums']['items']:
            album = data['albums']['items'][0]
            album_name = album['name']
            artist_name = album['artists'][0]['name']
            release_date = album['release_date']
            cover_url = album['images'][0]['url']

            # Display album information
            tk.Label(main_frame, text=f"Album: {album_name}", font=("Arial", 11, 'bold'), bg="#b2aaa5", fg="white").pack(pady=5)
            tk.Label(main_frame, text=f"Artist: {artist_name}", font=("Arial", 11, 'bold'), bg="#b2aaa5", fg="white").pack(pady=5)
            tk.Label(main_frame, text=f"Release Date: {release_date}", font=("Arial", 11, 'bold'), bg="#b2aaa5", fg="white").pack(pady=5)

            # Display album cover image
            img_data = requests.get(cover_url).content
            img = Image.open(BytesIO(img_data)).resize((200, 200))
            img_tk = ImageTk.PhotoImage(img)
            img_label = tk.Label(main_frame, image=img_tk, bg="white")
            img_label.image = img_tk  # Prevent garbage collection
            img_label.pack(pady=10)
        else:
            messagebox.showerror("Error", "Album not found.")
            
# search button
    tk.Button(main_frame, text="Search", command=search_album, bg="#566779", fg="white").pack(pady=10)

# 2nd page(artist top tracks)
def artist_top_tracks_page(): #main function
    clear_frame(main_frame)
    add_background_image(main_frame, "aura2.jpg")  # setting backgroung img

    #creating label for the frame
    tk.Label(main_frame, text="Artist Top Tracks", font=("Helvetica", 16, "bold"), bg="#b2aaa5", fg="white").pack(pady=10)
    tk.Label(main_frame, text="Enter Artist Name:", font=("Helvetica", 12), bg="#b2aaa5", fg="white").pack(pady=5)

    artist_entry = tk.Entry(main_frame, width=40) #entry label
    artist_entry.pack(pady=5)

    def search_tracks():
        artist_name = artist_entry.get()
        if not artist_name.strip():
            messagebox.showerror("Error", "Please enter an artist name.")
            return

        url = f"https://api.spotify.com/v1/search?q={artist_name}&type=artist" #api url for artist
        headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
        response = requests.get(url, headers=headers)
        data = response.json()
        if "artists" not in data or not data["artists"]["items"]:
            messagebox.showerror("Error", "No artist found.")
            return

        artist_id = data["artists"]["items"][0]["id"]
        tracks_url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=US" #api url to get tracks
        tracks_response = requests.get(tracks_url, headers=headers)
        tracks_data = tracks_response.json()

        if "tracks" not in tracks_data or not tracks_data["tracks"]:
            messagebox.showinfo("No Tracks", "No top tracks found for this artist.")
            return

        # Creating canvas and scrollbar when tracks are found
        canvas = tk.Canvas(main_frame, width=410, height=400)  # Setting width and height
        canvas.pack(side="left", fill="both", expand=False)

        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        # Creating a frame to store all the track information 
        track_frame = tk.Frame(canvas, bg="#D3D3D3")
        canvas.create_window((0, 0), window=track_frame, anchor="nw")

        for track in tracks_data["tracks"]:
            track_name = track["name"]
            album_name = track["album"]["name"]
            duration_ms = track["duration_ms"]
            album_cover_url = track["album"]["images"][0]["url"]  # Get the album cover URL
            duration = f"{duration_ms // 60000}:{(duration_ms // 1000) % 60:02}"

            # Fetch album cover image
            img_data = requests.get(album_cover_url).content
            img = Image.open(BytesIO(img_data)).resize((50, 50))  # setting size for the img
            img_tk = ImageTk.PhotoImage(img)

            # Creating a frame for album cover and its information side by side
            track_detail_frame = tk.Frame(track_frame, bg="#9d9fa1", width=410, relief="solid", bd=1)  #adding borders
            track_detail_frame.pack(pady=5, fill="x", padx=20)  

            # display the album cover on the left side
            img_label = tk.Label(track_detail_frame, image=img_tk, bg="#9d9fa1")  
            img_label.image = img_tk  # Prevent garbage collection
            img_label.grid(row=0, column=0, padx=10, pady=5)

            # Creating a frame to hold the text vertically
            text_frame = tk.Frame(track_detail_frame, bg="#9d9fa1", width=300)  #setting the width 
            text_frame.grid(row=0, column=1, padx=10, pady=5, sticky="w")  # placing it beside the image

            # Displaying the information vertically
            track_label = tk.Label(text_frame, text=f"Track: {track_name}",
                                   font=("Helvetica", 10, 'bold'), bg="#9d9fa1", fg="black")  
            track_label.grid(row=0, column=0, sticky="w", pady=2)

            album_label = tk.Label(text_frame, text=f"Album: {album_name}",
                                   font=("Helvetica", 10), bg="#9d9fa1", fg="black")  
            album_label.grid(row=1, column=0, sticky="w", pady=2)

            duration_label = tk.Label(text_frame, text=f"Duration: {duration}",
                                      font=("Helvetica", 10), bg="#9d9fa1", fg="black") 
            duration_label.grid(row=2, column=0, sticky="w", pady=2)

        # Update the scrollarea
        track_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    # Search button
    tk.Button(main_frame, text="Get Top Tracks", command=search_tracks, bg="#566779", fg="white").pack(pady=10)

# 3rd page (search lyrics)
def lyrics_search_page():
    clear_frame(main_frame) #main function
    add_background_image(main_frame, "aura2.jpg")  #setting background img

    # Creating widgets to overlay on the background
    tk.Label(main_frame, text="Search for Song Lyrics", font=("Helvetica", 16, "bold"), bg="#b2aaa5", fg="white").pack(pady=10)

    tk.Label(main_frame, text="Song Name:", bg="#b2aaa5", fg="white").pack(pady=5)
    song_entry = tk.Entry(main_frame, width=40)
    song_entry.pack(pady=5)

    tk.Label(main_frame, text="Artist Name:", bg="#b2aaa5", fg="white").pack(pady=5)
    artist_entry = tk.Entry(main_frame, width=40)
    artist_entry.pack(pady=5)

    def search_lyrics():
        song_name = song_entry.get()
        artist_name = artist_entry.get()
        if not song_name or not artist_name:
            messagebox.showerror("Error", "Please enter both song and artist names.")
            return

        url = f"https://api.lyrics.ovh/v1/{artist_name}/{song_name}" #using api link to get lyrics
        response = requests.get(url)
        data = response.json()

        if 'lyrics' in data:
            lyrics = data['lyrics']
            tk.Label(main_frame, text="Lyrics:", font=("Helvetica", 14), bg="#b2aaa5", fg="white").pack()  #creating a text frame "lyrics" 
            text_frame = tk.Frame(main_frame, bg="#191414")
            text_frame.pack(pady=10)

            scrollbar = tk.Scrollbar(text_frame)
            scrollbar.pack(side="right", fill="y") #keeping the scrollbar on the right side

            text_widget = tk.Text(text_frame, wrap="word", height=20, width=60, yscrollcommand=scrollbar.set, bg="#f0f0f0", fg="black")
            text_widget.insert("1.0", lyrics)
            text_widget.config(state="disabled")
            text_widget.pack(side="left")

            scrollbar.config(command=text_widget.yview)
        else:
            messagebox.showerror("Error", "Lyrics not found.")

 #search button
    tk.Button(main_frame, text="Search Lyrics", command=search_lyrics, bg="#566779", fg="white").pack(pady=10)
  
 # 4th page(Spotify search page)
def spotify_search_page(): #creating the main function
    def search_spotify():
        for widget in results_frame.winfo_children():
            widget.destroy()

        search_type = search_type_combobox.get() #using a combobox for dropdown
        query = search_entry.get()

        if not query:
            messagebox.showerror("Error", "Please enter a search query.")
            return

        url = f"https://api.spotify.com/v1/search?q={query}&type={search_type}&limit=5" #api link 
        headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

        response = requests.get(url, headers=headers)
        data = response.json()

        if search_type == "artist" and "artists" in data:
            items = data["artists"]["items"]
        elif search_type == "track" and "tracks" in data:
            items = data["tracks"]["items"]
        elif search_type == "album" and "albums" in data:
            items = data["albums"]["items"]
        elif search_type == "playlist" and "playlists" in data:
            items = data["playlists"]["items"]
        else:
            items = []

        if not items:
            messagebox.showinfo("No Results", "No results found for your search.")
            return

        for item in items:
            result_frame = tk.Frame(results_frame, bg="#9d9fa1", padx=10, pady=10)
            result_frame.pack(fill="x", pady=5, padx=5)
#using if else elif function for the drop down 
           #artist
            if search_type == "artist":
                name = item.get("name", "Unknown Artist")
                genres = ", ".join(item.get("genres", [])) or "No genres available"
                image_url = item["images"][0]["url"] if item["images"] else None

                tk.Label(result_frame, text=f"Artist: {name}", font=("Helvetica", 12, "bold"), fg="black", bg="#9d9fa1").pack(anchor="w") #setting a frame for each text 
                tk.Label(result_frame, text=f"Genres: {genres}", fg="black", bg="#9d9fa1").pack(anchor="w") #setting a frame for each text

                if image_url:
                    img_data = requests.get(image_url).content
                    img = Image.open(BytesIO(img_data)).resize((80, 80)) #setting size for the image
                    img_tk = ImageTk.PhotoImage(img)
                    img_label = tk.Label(result_frame, image=img_tk, bg="#333333")
                    img_label.image = img_tk
                    img_label.pack(side="right", padx=10) 
            #track
            elif search_type == "track":
                name = item.get("name", "Unknown Track")
                album = item.get("album", {}).get("name", "Unknown Album")
                image_url = item.get("album", {}).get("images", [{}])[0].get("url")

                tk.Label(result_frame, text=f"Track: {name}", font=("Helvetica", 12, "bold"), fg="black", bg="#9d9fa1").pack(anchor="w")
                tk.Label(result_frame, text=f"Album: {album}", fg="black", bg="#9d9fa1").pack(anchor="w")

                if image_url:
                    img_data = requests.get(image_url).content
                    img = Image.open(BytesIO(img_data)).resize((80, 80)) #setting size for the image
                    img_tk = ImageTk.PhotoImage(img)
                    img_label = tk.Label(result_frame, image=img_tk, bg="#9d9fa1")
                    img_label.image = img_tk
                    img_label.pack(side="right", padx=10)
           #album
            elif search_type == "album":
                name = item.get("name", "Unknown Album")
                artist = ", ".join(artist["name"] for artist in item.get("artists", [])) or "Unknown Artist"
                image_url = item.get("images", [{}])[0].get("url")

                tk.Label(result_frame, text=f"Album: {name}", font=("Helvetica", 12, "bold"), fg="black", bg="#9d9fa1").pack(anchor="w") #using anchor to place items
                tk.Label(result_frame, text=f"Artist: {artist}", fg="black", bg="#9d9fa1").pack(anchor="w")

                if image_url:
                    img_data = requests.get(image_url).content
                    img = Image.open(BytesIO(img_data)).resize((80, 80))
                    img_tk = ImageTk.PhotoImage(img)
                    img_label = tk.Label(result_frame, image=img_tk, bg="white")
                    img_label.image = img_tk
                    img_label.pack(side="right", padx=10)
         #playlist
            elif search_type == "playlist":
                name = item.get("name", "Unknown Playlist")
                owner = item.get("owner", {}).get("display_name", "Unknown Owner")
                image_url = item.get("images", [{}])[0].get("url")

                tk.Label(result_frame, text=f"Playlist: {name}", font=("Helvetica", 12, "bold"), fg="black", bg="#9d9fa1").pack(anchor="w")
                tk.Label(result_frame, text=f"Owner: {owner}", fg="black", bg="#9d9fa1").pack(anchor="w")

                if image_url:
                    img_data = requests.get(image_url).content
                    img = Image.open(BytesIO(img_data)).resize((80, 80)) #keeping the size same for all the images
                    img_tk = ImageTk.PhotoImage(img)
                    img_label = tk.Label(result_frame, image=img_tk, bg="#333333")
                    img_label.image = img_tk
                    img_label.pack(side="right", padx=10)

    clear_frame(main_frame)

    add_background_image(main_frame, "aura2.jpg")  #setting the background image

    tk.Label(main_frame, text="Spotify Search", font=("Helvetica", 16, "bold"), bg="#b2aaa5", fg="white").pack(pady=10)

    search_bar_frame = tk.Frame(main_frame, bg="#b2aaa5")
    search_bar_frame.pack(pady=10)

    tk.Label(search_bar_frame, text="Search for:", bg="#b2aaa5", fg="white").pack(side="left", padx=5)
    search_type_combobox = ttk.Combobox(search_bar_frame, values=["artist", "track", "album", "playlist"], state="readonly", width=10)
    search_type_combobox.current(0)
    search_type_combobox.pack(side="left", padx=5)

    search_entry = tk.Entry(search_bar_frame, width=30)
    search_entry.pack(side="left", padx=5)

    #search button
    search_button = tk.Button(search_bar_frame, text="Search", command=search_spotify, bg="#566779", fg="white")
    search_button.pack(side="left", padx=5)

    
    results_canvas = tk.Canvas(main_frame, bg="#D3D3D3", highlightthickness=0, width=420) #reducing the canvas size to 420 so it doesnt cover the entire frame
    results_scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=results_canvas.yview) #keeping the scroll bar vertical
    results_frame = tk.Frame(results_canvas, bg="#D3D3D3") #result frame

    results_frame.bind("<Configure>", lambda e: results_canvas.configure(scrollregion=results_canvas.bbox("all")))

    results_canvas.create_window((0, 0), window=results_frame, anchor="n")
    results_canvas.configure(yscrollcommand=results_scrollbar.set)

    results_canvas.pack(side="left", fill="both", expand=False, pady=10, padx=10) #result on the left
    results_scrollbar.pack(side="right", fill="y") #scroll bar on the right side
    
    
# Creating the main page
root = tk.Tk()
root.title("Spotify App")
root.geometry("800x600")
root.configure(bg="#191414")

# Creating navigation Frame
navigation_frame = tk.Frame(root, bg="#9d9fa1")
navigation_frame.pack(side="top", fill="x")

# Calling out call the function in the navigation bar
tk.Button(navigation_frame, text="Album Search", command=album_search_page, bg="#566779", fg="white").pack(side="left", padx=5, pady=5)
tk.Button(navigation_frame, text="Top Tracks", command=artist_top_tracks_page, bg="#566779", fg="white").pack(side="left", padx=5, pady=5)
tk.Button(navigation_frame, text="Lyrics Search", command=lyrics_search_page, bg="#566779", fg="white").pack(side="left", padx=5, pady=5)
tk.Button(navigation_frame, text="Spotify Search", command=spotify_search_page, bg="#566779", fg="white").pack(side="left", padx=5, pady=5)

# Main Frame
main_frame = tk.Frame(root, bg="#191414")
main_frame.pack(fill="both", expand=True)

# Setting Album search page as Default
welcome_page()

root.mainloop() 


