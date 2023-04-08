Hello! :3 This is a little project I made that updates your bio with the song your currently listening to on spotify! ≧◡≦
I dont think its coded that good, However it was fun to make. Im am also looking into possibly adding a way to use soundcloud
songs! ₊·*◟(˶╹̆ꇴ╹̆˵)◜‧*･

### How to guide:
On steam, On VRchats page press the gear icon on the right side, Click on propertys, under the launch options section in the text box copy "run.bat %COMMAND%" into it (if you have any other launch options put them after it).<br />

Download latest realease from release section, Move zip file to VRchats directory("C:\Program Files (x86)\Steam\steamapps\common\VRChat") and unzip it.<br />

For making a spotify application read https://developer.spotify.com/documentation/web-api/concepts/apps.<br />
Make name/discription anything you like, Set the redirect uri to "http://localhost:7777/callback" without quotation marks
You may need to login to your spotify account when you first run the program.

Go to info/details.ini and open it in notepad: <br />
Under the [VRCLOGIN] line where it says <br />
username =  Enter your VRchat username<br />
password =  Enter your VRchat password<br />

Under the [SPOTIFYAUTH] line where it says <br />
client_id =  Enter your spotify client ID<br />
client_secret =  Enter your spotify client secret<br />
redirect_uri =  Enter the redirect url for your spotify application<br />

Under the [BIO] line where it says<br />
bio =  Enter what youd like your bio to be(Read below)<br />
status = Enter what youd like your status to be(Read below)<br />

### Formating bio/status:
An example of a status and what the status would look like in game is,<br />
status = |>: {song}<br />
Would look like:<br />
|>: Example song by example...<br />
Cuts off last part of song because statuses can only be 32 characters long<br />

An example of a bio and what the bio would look like in game is,<br />
bio = Hello! ^.^ Welcome to my bio!<br />
      Professional Nyaher<br />
      |> {song} ||<br />
      {duration_graphic}<br />
Would look like:<br />
Hello! ^.^ Welcome to my bio!<br />
Professional Nyaher<br />
|> Example song by Example artist ||<br />
00˸00 ~~~~~~~~~~~~~ 00˸00<br />

For taking a new line you can simple just take new line, Example:<br />
bio = Hello!<br />
Goodbye!<br />
Would look like:<br />
Hello!<br />
Goodbye!<br />

Writing "{song}" without the quotation marks to put the song there, Example:<br />
bio={song}<br />
Would look like:<br />
Example song by Example artist<br />

Writing "{duration_grahic}" without the quotation marks to put the song duration there, Example:<br />
bio={duration_graphic}<br />
Would look like:<br />
00˸00 ~~~~~~~~~~~~~ 00˸00<br />

After doing that you can run VRchatSpotify.exe and it should ask you for your 2fa code/gmail code, Enter it then it should start working!
