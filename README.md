# FCS-secure-social-media-platform
Django based secure social media platform with functionality of Payment, dashboard, friend list, message, transaction history , group making wall post etc.  

**Commands**

	- To run the Project : 
		"python manage.py runserver" 

	- to create new app :
		"python manage.py startapp app-name"

	- to migrate tables :
		"python manage.py makemigrations"
		"python manage.py migrate"

	- to push on github :
		"git init"
		"git add ."
		"git commit -m 'first commit'"
		"git remote add origin url_of_git_repo"
		"git remote -v"
		"git push origin master"

**Apps in Project**

	- Account :
		For user signup and signin using customforms.

	- FCS :
		settings and url app.

	- home :
		website landing page.

	- dashboard :
		website dashboard after authentication.

	- templates :
		UI for the website.

**Libraries needed**
	
	- Django
		pip3 install Django


**Databases: sqlite**
	
	- User model (in account app)
		Attributes : 
		{ email, username, first_name, last_name, phone_no, date_joined, last_login, is_active, is_casual_user, is_premium_user, is_commercial_user, is_admin, is_staff }

	- FriendList model (in dashboard app)
		Attributes :
		{ user_1, user_2, status, date_requested, date_confirmed }

	- Transaction model (in dashboard app)
		Attributes :
		{
			to be done
		}

**Template Pages**

	-login.html
	-register.html
	-add_money.html
	-change_password.html
	-create_group.html
	-dashboard.html
	-edit_profile.html
	-friends.html
	-messenger.html
	-profile.html
	-transactions.html
	-transfer_money.html
	-wallet.html
