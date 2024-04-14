import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

client_id = "0b3f7d28e3e04736b81137e7bdff789c"
client_secret = "9a6523871e784000be6c442f43277b42"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
print(user_id)

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

billboard_url = f"https://www.billboard.com/charts/hot-100/{date}/"

response = requests.get(billboard_url)
# print(response.text)

soup = BeautifulSoup(response.text, "html.parser")
song_name = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_name]
# print(song_names)

song_uris = []
year = date.split("-")[0]

for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # pprint(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
        # pprint(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
