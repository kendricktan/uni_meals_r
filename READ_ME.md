# Uni Meals revamped

# user_profile consists of the ENTIRE user profile
	- Sign up
	- Log in
	- Log out
	- View profile Wall
	- View profile Timeline (food hearted, reviewed etc)
	- View profile Message
	- View profile Inbox 
	
# eatery_profile consists of the ENTIRE eatery profile, as well as the calculation for Geo Coordiantes (maybe stick with postcodes atm)
	- Browse
	- Search
	- View eatery profile
	- View eatery review
	- View eatery
	- Tags		

To improve:	

To fix:

To do:		
	High Priority:		
		Fix eatery logic error (1 downvote still 100% upvote)
		GPS coordinates to search restaurants
		Check if user has reviewed
		'I find this review useful'
		If user is not logged in and tries to do stuff that requires them to log in (e.g. heart food), sign them up
	
	Medium Priority:
		Create browse app, search app, inbox + message app
		User delete image function
		Merge heart/unheart js
		
	Low Priority:
		Ajax auto update when scroll for search, browse, reviews + timeline
		Resize user image/crop to suit layout needs

Done:
	Custom user model
	Error labels when logging in
	Username doesn't log in when entered email
	Signing up if username/email clashes
	Error labels when signing up
	Sign up success alert
	Create Browse, search for eateries
	Change html forms to django.forms.py?
	Design Admin Page	
	View eatery profile (specials, menu, review)
	Make eatery page dynamic	
	Eatery Page links to respective eateries	
	Add create and associate wall and timeline with user_creation
	Enable user to edit profile, upload_photo, etc
	User enable to heart food
	Heart will heart/empty heart based on users specials set hearts
	Do food for what you did for specials hearts