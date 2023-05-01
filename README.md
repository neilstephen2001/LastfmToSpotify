# last.fm data to Spotify Playlist
A web app that generates a Spotify playlist of a user's most listened tracks, obtained from their last.fm profile.

## To run
TBD

## How it works:
- When the application is first run, you will see the homepage where you will enter the details for the data to be extracted from last.fm.
<img src="/screenshots/homepage.png" alt= “homepage” width="700">
<br>

- Enter the information, then click 'Submit'. The data will then be displayed. 
<img src="/screenshots/display-results.png" alt= “results” width="700">
<br>

- If you choose to export the data to a playlist, you will be redirected to the Spotify login page.
<img src="/screenshots/spotify-login.png" alt= “spotify-login” width="700">
<br>

- Once you have logged in, you will be prompted to enter a playlist name and description.
<img src="/screenshots/create-playlist.png" alt= “create-playlist” width="700">
<br>

- A public playlist will be generated on your Spotify profile, and this will also be embedded into the web page. 
<img src="/screenshots/display-playlist.png" alt= “display-playlist” width="700">
<br>

## To-do:
- Implement Spotify authorisation
- Need to work out how to handle input errors (e.g. if last.fm username does not exist)
- Add option to choose theme of embedded playlist
- Might add an option to upload a custom photo when creating the playlist

