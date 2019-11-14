import pickle
import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User, Tweet, DB
from .twitter import basilica_client

def predict_user(username1, username2, text, cache=None):
	user_set = pickle.dumps((username1, username2))
	if cache and cache.exists(user_set):
		log_reg = pickle.loads(cache.get(user_set))
	else:
		user1 = User.query.filter(User.screen_name == username1).one()
		user2 = User.query.filter(User.screen_name == username2).one()

		user1_tweets = Tweet.query.filter(user1.user_id == Tweet.author_id).all()
		user2_tweets = Tweet.query.filter(user2.user_id == Tweet.author_id).all()

		user1_embed = np.array([tweet.embedding for tweet in user1_tweets])
		user2_embed = np.array([tweet.embedding for tweet in user2_tweets])

		embeds = np.vstack([user1_embed, user2_embed])
		labels = np.concatenate([np.ones(len(user1_tweets)),
								 np.zeros(len(user2_tweets))])
		log_reg = LogisticRegression().fit(embeds, labels)

	cache and cache.set(user_set, pickle.dumps(log_reg))
	tweet_embed = basilica_client.embed_sentence(text, model="twitter")
	return log_reg.predict(np.array(tweet_embed).reshape(1, -1))