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
	
# extra_content consists of the ENTIRE footer html

To improve:
	Change html forms to django.forms.py?

To fix:

To do:		
	High Priority:		
		GPS coordinates to search restaurants
		Make eatery page dynamic
		View eatery profile (specials, menu, review)
	
	Medium Priority:
		Enable user to edit profile, upload_photo, etc
		Create browse app, search app, inbox + message app
		Design Admin Page	
		
	Low Priority:
		Ajax scroll

Done:
	Custom user model
	Error labels when logging in
	Username doesn't log in when entered email
	Signing up if username/email clashes
	Error labels when signing up
	Sign up success alert
	Create Browse, search for eateries