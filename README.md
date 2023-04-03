Hello! :3 This is a little project I made that updates your bio with the song your currently listening to on spotify! ≧◡≦
I dont think its coded that good, However it was fun to make. Im am also looking into possibly adding a way to use soundcloud
songs! ₊·*◟(˶╹̆ꇴ╹̆˵)◜‧*･

How to guide:
All you need is a spotify application and a VRchat account.
For making a spotify application read https://developer.spotify.com/documentation/web-api/concepts/apps.
Make name/discription anything you like, Set the redirect uri to "http://localhost:7777/callback" without quotation marks
You may need to login to your spotify account on the website. ^^

Go to info/details.ini and open it in notepad:
Under the [VRCLOGIN] line where it says 
username =  Enter your VRchat username
password =  Enter your VRchat password

Under the [SPOTIFYAUTH] line where it says 
client_id =  Enter your spotify client ID
client_secret =  Enter your spotify client secret
redirect_uri =  Enter the redirect url for your spotify application

Under the [BIO] line where it says
bio =  Enter what youd like your bio to be(Read below for how to format bio)
status = Enter what youd like your status to be(Read below for how to format status)

An example of a status and what the status would look like in game is,
status = |>: {song}
Would look like:
|>: Example song by example...
Cuts off last part of song because statuses can only be 32 characters long

An example of a bio and what the bio would look like in game is,
bio = Hello! ^.^ Welcome to my bio!
      Professional Nyaher
      |> {song} ||
      {duration_graphic}
Would look like:
Hello! ^.^ Welcome to my bio!
Professional Nyaher
|> Example song by Example artist ||
00˸00 ~~~~~~~~~~~~~ 00˸00

For taking a new line you can simple just take new line, Example:
bio = Hello!
      Goodbye!
Would look like:
Hello!
Goodbye!

Writing "{song}" without the quotation marks to put the song there, Example:
bio={song}
Would look like:
Example song by Example artist

Writing "{duration_grahic}" without the quotation marks to put the song duration there, Example:
bio={duration_graphic}
Would look like:
00˸00 ~~~~~~~~~~~~~ 00˸00

After doing that you can run VRchatSpotify.exe and it should ask you for your 2fa code/gmail code, Enter it then it should start working!
