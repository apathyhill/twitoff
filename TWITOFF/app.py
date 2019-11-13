from decouple import config
from flask import Flask, render_template, request
from .models import DB, User, Tweet
from .twitter import twitter_client, basilica_client

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = config("DATABASE_URL")
    print(config("DATABASE_URL"))

    DB.init_app(app)

    @app.route("/")
    def root():
        users = User.query.all()
        return render_template("base.html", title="Home", users=users)

    @app.route("/setup")
    def setup():
        users = ["ElonMusk", "MichaelReeves08", "CrabsandScience", "GavinFree", "TomScott", "AH_Michael"]

        DB.drop_all()
        DB.create_all()

        for user in users:
            print(user)
            tweets = twitter_client.get_user_timeline(count=20, screen_name=user, exclude_replies=True, include_rts=False, mode="extended")
            user_data = twitter_client.show_user(screen_name=user)
            
            db_user = User(user_id=user_data["id"], screen_name=user_data["screen_name"], display_name=user_data["name"])

            for tweet in tweets:
                embed = basilica_client.embed_sentence(tweet["text"], model="twitter")
                db_tweet = Tweet(tweet_id=tweet["id"], text=tweet["text"], author_id=user_data["id"], embedding = embed)
                DB.session.add(db_tweet)

            DB.session.add(db_user)
        DB.session.commit()

        return "Users added!"



    @app.route("/reset")
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template("base.html", title="Reset", users=[])

    @app.route("/user/<username>")
    def show_user_tweets(username):
        tweets = twitter_client.get_user_timeline(count=200, screen_name=username, exclude_replies=True, include_rts=False)
        user = twitter_client.show_user(screen_name=username)
        pfp = user["profile_image_url"].replace("_normal", "")
        color = user["profile_link_color"]
        tweets = [[tweet["text"], tweet["id"]] for tweet in tweets]
        return render_template("user.html", screen_name=username, tweets=tweets, pfp_url=pfp, user_color=color)

    return app