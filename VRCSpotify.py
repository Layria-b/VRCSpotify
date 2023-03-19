import vrchatapi
from vrchatapi.api import authentication_api
from vrchatapi.models.two_factor_email_code import TwoFactorEmailCode
from vrchatapi.models.two_factor_auth_code import TwoFactorAuthCode
from vrchatapi.exceptions import UnauthorizedException
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from http.cookiejar import LWPCookieJar
import schedule
import time
import os 

song=""
duration_graphic=""

# Add your spotify application stuff here ^^
client_id = "" # Enter client_id
client_secret = "" # Enter client_secret
redirect_uri = "" # Enter redirect_url

# Enter VRC login details, Will only be used if cookie expired or first time running!
username = "" # Enter VRC username
password = "" # Enter VRC password

# Go to line 147 and enter what you would like your bio to be (
# Write "{song}" without the quotation marks to put the song there. Looks Like: Example Song by Example Artist
# Write "\n" without the quotation marks to make a new line in your bio. Looks like: Example Text
#                                                                                    Example Text  
# Write "{duration_graphic}" without the quotation marks to put the duration of the song in ur bio. Looks like: 01:58 〼〼〼〼〼〼~~~~~~~ 03:59 )

filename = "cookie.txt"
delay = 45
scope = 'user-read-playback-state'
os.environ['last_song'] = ""

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
        redirect_uri=redirect_uri)
    )

    spotify_song_resp = sp.current_user_playing_track()
    if spotify_song_resp == None or spotify_song_resp['is_playing'] == False:
        song = 'Nothing'
        duration_graphic = "00˸00 ~~~~~~~~~~~~~ 00˸00"
        return song, duration_graphic
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

        return song, duration_graphic, 
    

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
    save_cookies(filename=filename)

def vrc_bio_change():
    song_info_ = song_info(scope, client_id, client_secret, redirect_uri)
    song = song_info_[0]
    status_song = song
    duration_graphic = song_info_[1]

    if song != os.environ['last_song']:
        if len(status_song) > 28:
            shorten_by_status = len(status_song[:-25])
            status_song = f"{song[:-shorten_by_status]}..."
        
        if len(song) > 50:
            shorten_by = len(song[:-50])
            song = f"{song[:-shorten_by]}..."
        if len(status_song) > 28:
            shorten_by_status = len(status_song[:-28])
            status_song = f"{song[:-shorten_by_status]}..."
        status_description = f"|>: {status_song}"
                                                                                                                                                #
        bio=f"Hello welcome to my Example bio! \n I am listening to {song} right now! \n This is the duration of the song {duration_graphic}!"   # Enter bio here   
                                                                                                                                                #
        print('Updating Bio! >:3')
        print(bio)
        print("Also status! ^^")
        print(status_description)

        update_user_request = vrchatapi.UpdateUserRequest(
        bio=bio,
        status_description=status_description
        )
        bio_request = user_api.update_user(current_user.id, update_user_request=update_user_request)
        os.environ['last_song'] = song

schedule.every(delay).seconds.do(vrc_bio_change)
while 1:
   schedule.run_pending()
   time.sleep(1)




