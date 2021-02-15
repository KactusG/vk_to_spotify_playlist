import requests
import json
import spotipy
import math

vk_token = ""
spotify_token = ""
user_id = ""
playlist_name = ""

if vk_token == "":
	vk_token = input("Введите токен вк с доступом к аудиозаписям данного пользователя: ")
if spotify_token == "":
	spotify_token = input("Введите токен Spotify с доступом к плейлистам, получить вы можете его на сайте http://easygame.website/get_spotify_token.php: ")
if user_id == "":
	user_id = input("Введите id пользователя с аудиозаписями: ")
if playlist_name == "":
	playlist_name = input("Введите название плейлиста в Spotify: ")

sort = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]

track = []
non_added_track = []
tracks_sp = []
req = json.loads(requests.get(f"https://api.vk.com/method/audio.get?v=5.107&access_token={vk_token}&owner_id={user_id}").text)
try:
	count_full = req["response"]["count"]
except KeyError:
	error = req["error"]["error_code"]
	if error == 201:
		print(f"Доступ к музыки пользователя id{user_id} запрещён")
	if error == 7:
		print("Нет прав у токена для выполнения этого действия")
	if error == 18:
		print("Страница удалена или заблокированна")
	exit()
a = math.ceil(count_full/200)
b = 0
n = 0

while b < a:
	offset = b * 200 
	response = json.loads(requests.get(f"https://api.vk.com/method/audio.get?offset={offset}&v=5.107&access_token={vk_token}&owner_id={user_id}").text)["response"]
	i = 0
	
	items = response["items"]
	if (count_full/200 - b) >= 1:
		count = 200
	else:
		count = (count_full/200 - b) * 200

	while i < count:
		artist = items[i]["artist"] + " "
		title = items[i]["title"]
		track.append(artist + title)
		i += 1
	b += 1

#Spotify
sp = spotipy.Spotify(spotify_token)
sp_id = sp.current_user()['id']
sp.user_playlist_create(user=sp_id,name=playlist_name, public=False)
playlist_id = sp.user_playlists(sp_id)['items'][0]['id']

for x in range(len(track)):
	try:
		url = sp.search(q=track[x])['tracks']['items'][0]['id']
		tracks_sp.append(url)
	except:
		non_added_track.append(track[x])
if len(tracks_sp) > 100:
	count_tr = math.ceil(len(tracks_sp) / 100)
	group_tracks = sort(tracks_sp, count_tr)
	while n < len(group_tracks):
		sp.user_playlist_add_tracks(sp_id, playlist_id=playlist_id, tracks=group_tracks[n])
		n += 1

print("Не удалось переместить данные треки: " + str(non_added_track))