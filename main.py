import requests
from os import environ as env
import io
import time

import click
import dotenv
import tweepy
from PIL import Image, ImageDraw
import PIL

dotenv.load_dotenv()


class ProfileBanner:
    def __init__(self):
        self.client = self.__login()
        self.FIRST_IMAGE_COORDS = (600, 400)
        self.IMAGE_DIA = 75
        self.follower_len = len(self.client.get_followers(user_id=env.get("USER_ID")))

    def __login(self):
        """Logins and sets access tokens"""
        auth = tweepy.OAuthHandler(env["CONSUMER_KEY"], env["CONSUMER_SECRET"])
        auth.set_access_token(env["ACCESS_TOKEN"], env["ACCESS_TOKEN_SECRET"])
        api = tweepy.API(auth)
        print(api)
        return api

    def __get_latest_followers_images(self) -> list[io.BytesIO]:
        """Gets all the latest follower images"""
        latest_followers = self.client.get_followers(
            user_id=env.get("USER_ID"), count=5
        )
        images = []

        for follower in latest_followers:
            response = requests.get(follower.profile_image_url)
            images.append(io.BytesIO(response.content))
        return images

    def __image_factory(self, filename = "twitter_banner.jpg", savepath: str = None) -> Image:
        """
        Pastes the image onto the template
        """
        template = Image.open(filename)
        images = self.__get_latest_followers_images()
        for i, image in enumerate(images):
            try:
                image = Image.open(image)
            except PIL.UnidentifiedImageError:
                continue
            image = image.resize((self.IMAGE_DIA, self.IMAGE_DIA))

            # Make image circle
            mask = Image.new("L", (self.IMAGE_DIA, self.IMAGE_DIA), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, self.IMAGE_DIA, self.IMAGE_DIA), fill=255)
            image.putalpha(mask)

            # Paste the image onto the template
            template.paste(
                image,
                (
                    self.FIRST_IMAGE_COORDS[0] + (i * self.IMAGE_DIA),
                    self.FIRST_IMAGE_COORDS[1],
                ),
                image,
            )

        if savepath:
            template.save(savepath)
        return template

    def make_tweet(self, tweet: str) -> None:
        """Simply makes a tweet"""
        self.client.update_status(tweet)

    def __update_banner(self) -> None:
        """Updates the banner"""
        self.__image_factory(savepath="banner.png")
        self.client.update_profile_banner("banner.png")
        print("Updated banner")

    def update_every_few_minutes(self, minutes:int = 5):
        """Starts the update loop"""
        while True:
            self.__update_banner()
            time.sleep(60*minutes)

@click.command()
@click.option('--minutes', default=5, help='Repeat every x minutes')
def main(minutes):
    banner = ProfileBanner()
    banner.update_every_few_minutes(minutes)

if __name__ == "__main__":
    main()
