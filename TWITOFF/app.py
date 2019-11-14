from decouple import config
from flask import Flask, render_template, request
from .models import DB, User, Tweet
from .twitter import twitter_client, basilica_client, update_user
from .predict import predict_user

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = config("DATABASE_URL")
    print(config("DATABASE_URL"))

    DB.init_app(app)

    @app.route("/")
    def root():
        users = User.query.all()
        return render_template("home.html", title="Home", users=users)

    @app.route("/reset")
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template("base.html", title="Reset", h1="Reset")

    @app.route("/user", methods=["POST"])
    @app.route("/user/<screen_name>")
    def show_user_tweets(screen_name=None):
        screen_name = screen_name or request.values["screen_name"]
        try:
            if request.method == "POST":
                message = update_user(screen_name)
                print(message)
            user = User.query.filter(User.screen_name == screen_name).one()
            tweets = Tweet.query.filter(user.user_id == Tweet.author_id)
            tweets = [[tweet.text, tweet.tweet_id] for tweet in tweets]
            pfp_url = user.pfp_url
            color = user.color
            print("test")
        except Exception as e:
            print(str(e))
            tweets = []
            pfp_url = ""
            color = "000000"

        return render_template("user.html", screen_name=screen_name, tweets=tweets, pfp_url=pfp_url, user_color=color)

    @app.route("/compare", methods=["POST"])
    def compare(message=""):
        user1, user2 = sorted([request.values["user1"],
                               request.values["user2"]])
        tweet_text = request.values["tweet_text"]
        if user1 == user2:
            message = "Cannot compare a user to themselves!"
        else:
            prediction = predict_user(user1, user2, tweet_text)
            print(prediction)
            message = """"{}" is more likely to be said by {} than {}""".format(
                tweet_text, user1 if prediction else user2,
                user2 if prediction else user1)
        return render_template("prediction.html", title="Prediction", message=message)


    return app