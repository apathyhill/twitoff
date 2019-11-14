import basilica
from twython import Twython
from decouple import config
from .models import DB, User, Tweet
from sqlalchemy import exists

twitter_client = Twython(config("API_KEY"),
                         config("API_SECRET"), 
                         config("CONSUMER_KEY"),
                         config("CONSUMER_SECRET"))

basilica_client = basilica.Connection(config("BASILICA_KEY"))

def update_user(screen_name):
    try:
        if DB.session.query(exists().where(User.screen_name==screen_name)).scalar():
            return "User {} already exists.".format(screen_name)
        tweets = twitter_client.get_user_timeline(count=200, screen_name=screen_name, exclude_replies=True, include_rts=False, mode="extended")
        user_data = twitter_client.show_user(screen_name=screen_name)

        db_user = User(user_id=user_data["id"], 
                       screen_name=user_data["screen_name"], 
                       display_name=user_data["name"],
                       pfp_url = user_data["profile_image_url"].replace("_normal", ""),
                       color = user_data["profile_link_color"])

        for tweet in tweets:
            embed = basilica_client.embed_sentence(tweet["text"], model="twitter")
            db_tweet = Tweet(tweet_id=tweet["id"], text=tweet["text"], author_id=user_data["id"], embedding=embed)
            DB.session.add(db_tweet)

        DB.session.add(db_user)
    except Exception as e:
        print("Error: Cannot Process {}. {}".format(screen_name, e))
        return "ERROR"
    else:
        DB.session.commit()
        return "Users added!"