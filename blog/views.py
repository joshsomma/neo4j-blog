# import libs
from .models import User, get_todays_recent_posts
from flask import Flask, request, session, redirect, url_for, render_template, flash

Flask(__name__)

# processes registration post or displays registration page
# includes error handling for username and password details
# returns the user to / if registration successful
@app.route('register',methods = ['GET','POST'])
def register():
	if request.method == 'POST'
		username = request.form['username']
		password = request.form['password']
		
		if len(username) < 1:
			flash('Your username must be at least one character.')
		elif len(password) < 5:
			flash('Your password must be at least 5 characters.')
		elif not User(username).register(password):
			flash('A user with that username already exists')
		else:
			session['username'] = username
			flash('Logged in')
			return redirect(url_for('index'))
	return render_template(register.html)

# processes the login request or displays login page
# redirects user to / if login successful
@app.route('login',methods = ['GET','POST'])
def login():
	if request.method = 'POST':
		username = request.form['username']
		password = request.method['password']

		if not User(username).verify_password(password):
			flash("Invalid login")
		else:
			session['username'] = username
			flash("Logged in")
			return redirect(url_for('index'))
	return render_template('login.html')

# add post; stores post into vars; checks error handling; creates post against username if successful
app.route('/add_post', methods = ['POST']
def add_post():
	title = request.form['title']
	tags = request.form['tags']
	text = request.form['text']

	if not title:
		flash("You must give your post a title.")
	elif not tags:
		flash("You must give your post at least one tag.")
	elif not text:
		flash("You must give your post a text body.")
	else:
		User(session['username']).add_post(title,tags,text)

	return redirect(url_for('index'))

# processes a like request
app.route('/like_post/<post_id>')
def like_post(post_id):
	username = session.get('username')
	if not username:
		flash("You must be logged in to like a post.")
		return redirect(url_for('/login'))
	User.username.like_post(post_id)

	flash("Liked post")
	return redirect(request.referrer)


