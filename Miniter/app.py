from flask import Flask, jsonify, request

app = Flask(__name__)

app.users = {}
app.id_count = 1

app.tweets = []


@app.route("/ping", methods=["GET"])
def ping():
    return "pong"


@app.route("/sign-up", methods=["POST"])
def sign_up():
    new_user = request.json
    new_user["id"] = app.id_count
    app.users[app.id_count] = new_user
    app.id_count = app.id_count + 1

    return jsonify(new_user)


@app.route("/tweet", methods=["POST"])
def tweet():
    # 요청 데이터 => { id: 1, tweet: "ABC" }
    payload = request.json
    
	user_id = int(payload["id"])
    tweet_data = payload["tweet"]

    if user_id not in app.users:
        return "존재하지 않는 유저입니다.", 400

    if len(tweet_data) > 300:
        return "300자를 초과했습니다.", 400

    # app.tweets["user_id"] = tweet_data
    app.tweets.append({"user_id": user_id, "tweet": tweet})

    return "", 200


@app.route('/follow', methods=["POST"])
def follow():
	# 요청 데이터 => { id: 1, follow: 2 }
	payload = request.json
	
	user_id = int(payload["id"])
	user_id_to_follow = int(payload["follow"])

	if user_id not in app.users or user_id_to_follow not in app.users:
		return '존재하지 않는 유저입니다.', 400

	user = app.users[user_id]
	user.setdefault('follow', set()).add(user_id_to_follow)

	return jsonify(user)

@app.route('/unfollow', methods=["POST"])
def method_name():
   pass