<div align="center">
<h1 align="center">Auto twitter banner</h1>

<img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-blue.svg" /><br>
<br>
Automatically updates the twitter banner every few seconds with follower profile pics on it

### Installation
```
git clone https://github.com/philippe-heitzmann/realtime_twitter_banner.git
cd realtime_twitter_banner
pip install -r requirements.txt
```

### Usage

First, you need your developer tokens from twitter:
- Go to https://developer.twitter.com/en/portal/
- Create an app, and get your keys and tokens 
- Make a `.env` file 
- Go to your app settings -> User authentication settings -> Toggle on OAuth 1.0a, and in the OAuth 1.0a Settings section, select Read and write

You might need to make your own banner and figure out the position where you need to paste the images and just change the `FIRST_IMAGE_COORDS` and `IMAGE_DIA` constants

```
python main.py --minutes=10
```

### Contributing
All contributors are welcome!
- Open an issue
- Assign yourself
- fork and send a PR

### License
This project is licensed under the mit license
### Show your support
Leave a ⭐ if you like this project

***
