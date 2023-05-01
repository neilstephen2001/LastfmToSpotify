# last.fm data to Spotify Playlist
A web app that generates a Spotify playlist of a user's most listened tracks, obtained from their last.fm profile.

## To run the app:

### Install dependencies
Run on terminal:
>pip3 install -r requirements.txt

### Get Spotify client secrets 
- Create a Spotify developer account
- Create a new application on https://developer.spotify.com/dashboard/applications
- Make note of the Spotify client ID, client secret and redirect URL
- Create a .env file, where you store these using the variable names: SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET and SPOTIFY_REDIRECT_URL

### Get last.fm API
- Create an API account on https://www.last.fm/api/account/create
- Store the API key in the local .env file, under the variable name: LASTFM_API

### To run
Run the following on terminal then click the link shown:
> set FLASK_APP = app
> 
> flask run
<br>

## How it works:
- When the application is first run, you will see this page where you will be prompted to login to your Spotify account 
<img src="/screenshots/spotify-login.png" alt= “spotify-login” width="700">
<br>

- Once you have logged in, you willsee the homepage where you will enter the details for the data to be extracted from last.fm.
<img src="/screenshots/homepage.png" alt= “homepage” width="700">
<br>

- Enter the information, then click 'Submit'. The data will then be displayed.
- Note: the sample data below was obtained from [my own last.fm profile](https://www.last.fm/user/stvn127/library/tracks?date_preset=LAST_90_DAYS).
<img src="/screenshots/display-results.png" alt= “results” width="700">
<br>

- If you choose to export the data to a playlist, you will then be prompted to enter a playlist name and description.
<img src="/screenshots/create-playlist.png" alt= “create-playlist” width="700">
<br>

- A public playlist will be generated on your Spotify profile, and this will also be embedded into the web page. 
<img src="/screenshots/display-playlist.png" alt= “display-playlist” width="700">
<br>

## Notes/to-do:
- Currently only works if user is included as one of the app's developers on the Spotify Developer website
- Need to work out how to handle input errors (e.g. if last.fm username does not exist)
- Add option to choose theme of embedded playlist
- Might add an option to upload a custom photo when creating the playlist