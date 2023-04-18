Hello! :3 This is a little project I made that updates your bio with the song your currently listening to on spotify! ≧◡≦ It uses VRCs api as well as spotipy. ₊·*◟(˶╹̆ꇴ╹̆˵)◜‧*･

### Installation:
**Note: You need a spotify application, Click [here](https://developer.spotify.com/documentation/web-api/concepts/apps) for how to make one.**<br />
**Make name/discription anything you like, Set the redirect uri to "http://localhost:7777/callback" without quotation marks**

Download latest release, unzip and put files in C:\Program Files (x86)\Steam\steamapps\common\VRChat.<br />
Go on VRchats homepage on steam and hover over the gear icon on the rightside of the screen, Click on propertys, under the launch options section in the text box copy "run.bat %COMMAND%" into it (if you have any other launch options put them after it).<br />

### Configuring:
Go to info/details.ini and open it in notepad enter appropriate info: <br />
```
[VRCLOGIN]
username =  Enter your VRchat username
password =  Enter your VRchat password

[SPOTIFYAUTH]
client_id =  Enter your spotify client ID
client_secret =  Enter your spotify client secret
redirect_uri =  Enter the redirect url for your spotify application

[BIO]
bio =  Enter what youd like your bio to be
status = Enter what youd like your status to be
```

### Formating bio/status:
```
bio = Hello! 
      This is my bio! ^^
      {song}
      || {duration_graphic} |>
```
**Note: All lines must be indented.**<br />
Looks like:
```
Hello!
This is my bio! ^^
Example song by example artist
|| 0:00 ~~~~~~~~~~~~ 0:00 |>
```

Taking a new line makes a new line, {song} adds the song name puts the song name, {duration_graphic} puts a duration bar, timestamp and length.
