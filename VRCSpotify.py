import vrchatapi
from vrchatapi.api import authentication_api
from vrchatapi.models.two_factor_email_code import TwoFactorEmailCode
from vrchatapi.models.two_factor_auth_code import TwoFactorAuthCode
from vrchatapi.exceptions import UnauthorizedException
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from http.cookiejar import LWPCookieJar
import sched
import time
import configparser
from datetime import datetime
import ctypes
import subprocess

ctypes.windll.kernel32.SetConsoleTitleW("VRchatSpotify")
config = configparser.ConfigParser()
config.read("info/details.ini")
sc = sched.scheduler(time.time, time.sleep)

client_id = config["SPOTIFYAUTH"]["client_id"]
client_secret = config["SPOTIFYAUTH"]["client_secret"]
redirect_uri = config["SPOTIFYAUTH"]["redirect_uri"]
scope = 'user-read-playback-state'
username = config["VRCLOGIN"]["username"]
password = config["VRCLOGIN"]["password"]
song=""
duration_graphic=""
filename = "info/cookie.txt"
delay = 3

call = 'TASKLIST', '/FI', 'imagename eq %s' % "VRChat.exe"
output = subprocess.check_output(call).decode()
last_line = output.strip().split('\r\n')[-1]
while last_line.lower().startswith("VRChat.exe".lower()) == False:
    output = subprocess.check_output(call).decode()
    last_line = output.strip().split('\r\n')[-1]
    print("Waiting for VRC to open...")
    time.sleep(60)

def MStoMin(ms):
    minutes, seconds = divmod(ms / 1000, 60)
    return f'{minutes:0>2.0f}:{seconds:0>2.0f}'

def save_cookies(filename: str):
    cookie_jar = LWPCookieJar(filename=filename)
    
    for cookie in api_client.rest_client.cookie_jar:
        cookie_jar.set_cookie(cookie)
        
    cookie_jar.save()
        
def load_cookies(filename: str):
    cookie_jar = LWPCookieJar(filename=filename)

    try:
        cookie_jar.load()
    except FileNotFoundError:
        cookie_jar.save()
        return
    
    for cookie in cookie_jar:
        api_client.rest_client.cookie_jar.set_cookie(cookie)


def song_info(scope, client_id, client_secret, redirect_uri):
    
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        scope=scope,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        cache_path="info/.cache")
    )

    spotify_song_resp = sp.current_user_playing_track()
    if spotify_song_resp == None or spotify_song_resp['is_playing'] == False:
        song = 'Nothing'
        duration_graphic = "00˸00 ~~~~~~~~~~~~~ 00˸00"
        seconds_remaining = 70.0
        return song, duration_graphic, seconds_remaining
    else:
        track_name = spotify_song_resp['item']['name']
        artists = [artist for artist in spotify_song_resp['item']['artists']]
        artist_names = ', '.join([artist['name'] for artist in artists])
        song = f'{track_name} by {artist_names}'
        song = song.translate({ord(c): '`' for c in "\'\""})

        song_timestamp = spotify_song_resp['progress_ms']
        song_duration = spotify_song_resp['item']['duration_ms']

        section_array = []
        section_length=song_duration/13
        duration_graphic = "~~~~~~~~~~~~~"
        for i in range(14):
            section_array.append(int(section_length)*i)
        section_array.pop(0)
        for section_num in range(13):
            if song_timestamp < section_array[section_num] and song_duration > section_array[section_num-1]:
                duration_graphic = duration_graphic.replace("~", "〼", section_num)
                break
        duration_graphic = f"{str(MStoMin(song_timestamp))} {duration_graphic} {str(MStoMin(song_duration))}"

        seconds_remaining = ((song_duration-song_timestamp)/1000)+5
        
        return song, duration_graphic, seconds_remaining
    

try: 
    with vrchatapi.ApiClient() as api_client:
        load_cookies(filename=filename)
        
        auth_api = authentication_api.AuthenticationApi(api_client)
        current_user = auth_api.get_current_user()
        print("Found Valid Cookies!")
        print("logged in as", current_user.display_name, "! :3")
        user_api = vrchatapi.UsersApi(api_client)
except UnauthorizedException:

    print("No Cookie Found, Using username/password to login!")
    configuration = vrchatapi.Configuration(
    username = username,
    password = password
    )

    with vrchatapi.ApiClient(configuration) as api_client:
        auth_api = authentication_api.AuthenticationApi(api_client)
        try:
            current_user = auth_api.get_current_user()
        except ValueError:
            auth_api.verify2_fa_email_code(two_factor_email_code=TwoFactorEmailCode(input("Enter the code sent to your email: ")))
            current_user = auth_api.get_current_user()
            user_api = vrchatapi.UsersApi(api_client)
        except UnauthorizedException as e:
            if UnauthorizedException.status == 200:
                auth_api.verify2_fa(two_factor_auth_code=TwoFactorAuthCode(input("Enter your 2fa code: ")))
                current_user = auth_api.get_current_user()
            else:
                print("Exception when calling API: %s\n", e)
        except vrchatapi.ApiException as e:
            print("Exception when calling API: %s\n", e)
    print("logged in as", current_user.display_name, "! :3")
    save_cookies(filename=filename)

def vrc_bio_change():
    call = 'TASKLIST', '/FI', 'imagename eq %s' % "VRChat.exe"
    output = subprocess.check_output(call).decode()
    last_line = output.strip().split('\r\n')[-1]
    if last_line.lower().startswith("VRChat.exe".lower()) == False:
        print("VRChat closed exiting...")
        exit()

    song_info_ = song_info(scope, client_id, client_secret, redirect_uri)
    song = song_info_[0]
    duration_graphic = song_info_[1]
    seconds_remaining = song_info_[2]

    status_description = config['BIO']['status'].format(song = song, duration_graphic = duration_graphic)
    if len(status_description) > 28:
        shorten_by_status = len(status_description[:-28])
        status_description = f"{status_description[:-shorten_by_status]}..."
    bio=config["BIO"]["bio"].format(song = song, duration_graphic = duration_graphic)
    print(f'Updating Bio! >:3 At {datetime.now()}')
    print(bio)
    print("Also status! ^^")
    print(status_description)

    update_user_request = vrchatapi.UpdateUserRequest(
    bio=bio,
    status_description=status_description
    )
    bio_request = user_api.update_user(current_user.id, update_user_request=update_user_request)

    if seconds_remaining<70.0:
        sc.enter(seconds_remaining, 1, vrc_bio_change)
    else:
        sc.enter(70.0, 1, vrc_bio_change)

sc.enter(1.0, 1, vrc_bio_change)
sc.run()
