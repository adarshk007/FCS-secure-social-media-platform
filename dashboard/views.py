from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from dashboard.forms import EditProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
from account.models import Account
from dashboard.models import Friend, Wallet, Transaction, feed, Message, Page
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.utils import timezone
# from dashboard.models import Friends

def dashboard_view(request):
	if not request.user.is_authenticated:
		return redirect('login')


	p = Page.objects.all()
	print(p)
	args = {
		"text" : "This is the dashboard",
		'pages' : p
	}

	accounts = Account.objects.all()
	args['accounts'] = accounts 

	if request.user.is_authenticated:
		return render(request, 'dashboard.html', args)
	else : return redirect('login')

def profile_view(request, u_id=None):
	if not request.user.is_authenticated:
		return redirect('login')

	user_data = Account.objects.filter(id=u_id)[0]

	posts = feed.objects.filter(post_to = user_data).order_by('-date_posted')

	is_friend = False

	if int(u_id) == int(request.user.id):
		is_friend = True

	if Friend.objects.filter(user_1 = user_data, user_2 = request.user).exists() | Friend.objects.filter(user_2 = user_data, user_1 = request.user).exists():
		is_friend = True
	print(is_friend)

	args = {
		'user': user_data,
		'u_id' : int(u_id),
		'posts' : posts,
		'is_friend' : is_friend
	}
	return render(request, 'profile.html', args)

def edit_profile_info_view(request):
	if not request.user.is_authenticated:
		return redirect('login')

	args = {}

	if request.method == "POST":
		form = EditProfileForm(request.POST, instance=request.user)

		if form.is_valid():
			form.save()
			return redirect('/profile/'+str(request.user.id)+'/')
	
	else:
		form = EditProfileForm(instance=request.user)
		args = {'edit_profile_info_form': form}
		return render(request, 'edit_profile_info.html', args)

def change_password_view(request):
	if not request.user.is_authenticated:
		return redirect('login')

	args = {}

	if request.method == "POST":
		form = PasswordChangeForm(data=request.POST, user=request.user)

		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			return redirect('/profile/'+str(request.user.id)+'/')
		else: return redirect('change_password')
	else: 
		form = PasswordChangeForm(user=request.user)
		args = {'change_password_form': form}
		return render(request, 'change_password.html', args)


def search_view(request):
	if not request.user.is_authenticated:
		return redirect('login')
	
	search_content = request.GET.get('q')
	# print(request.user.id)


	if search_content:
		results = Account.objects.filter(
			Q(username__icontains=search_content)
			| Q (email__icontains=search_content)
			| Q (first_name=search_content)
			)
		results = results.exclude(id=request.user.id)


		if results:
			args = {
				'result' : results,
				'status' : 200,
				'error' : '' 
			}
			return render(request, 'search.html', args)
		else:
			args = {
				'result' : '',
				'status' : 0,
				'error' : {
					1 : 'No results found'
				}

			}
			return render(request, 'search.html', args)
	return render(request, 'search.html')


def friends_view(request):
	if not request.user.is_authenticated:
		return redirect('login')

	user_1 = request.user
	friends = (Friend.objects.filter(user_1 = user_1) | Friend.objects.filter(user_2 = user_1) ) & Friend.objects.filter(status = True)

	args = {
		'friends' : friends,
		'status' : 200,
		'errors' : ''
	}

	return render(request, 'friends.html', args)

def friend_requests_view(request):
	if not request.user.is_authenticated:
		return redirect('login')

	user_1 = request.user
	friend_requests = Friend.objects.filter(user_2 = user_1) & Friend.objects.filter(status = False)

	args = {

		'friend_requests' : friend_requests,
		'status' : 200,
		'errors' : ''
	}

	return render(request, 'friend_request.html', args)

def send_request_view(request, u_id):
	if not request.user.is_authenticated:
		return redirect('login')

	args = {

	}
	user_1 = request.user
	user_2 = Account.objects.filter(id=u_id)[0]

	if Friend.objects.filter(user_1 = user_1, user_2 = user_2).exists() | Friend.objects.filter(user_1 = user_2, user_2 = user_1).exists():
		return redirect('friends')
	else : 
		friend_request = Friend(user_1 = user_1, user_2 = user_2, status = False)
		friend_request.save()

	return redirect('friends')
	
def accept_request_view(request, u_id):
	if not request.user.is_authenticated:
		return redirect('login')

	user_2 = request.user
	user_1 = Account.objects.filter(id=u_id)[0]

	accept_request = Friend.objects.get(user_1 = user_1, user_2 = user_2, status = False)
	accept_request.status = True
	accept_request.save()	
	return redirect('friends')

def delete_request_view(request, u_id):
	if not request.user.is_authenticated:
		return redirect('login')

	user_1 = Account.objects.filter(id=u_id)[0]
	user_2 = request.user

	if Friend.objects.filter(user_1 = user_1, user_2 = user_2).exists():
		Friend.objects.filter(user_1 = user_1, user_2 = user_2).delete()

	if Friend.objects.filter(user_1 = user_2, user_2 = user_1).exists():
		Friend.objects.filter(user_1 = user_2, user_2 = user_1).delete()
	# delete_request.save()

	return redirect('friend_requests')

def unfriend_view(request, u_id):
	if not request.user.is_authenticated:
		return redirect('login')

	user_1 = request.user
	user_2 = Account.objects.filter(id=u_id)[0]
	print(user_1)
	print(user_2)
	print("inside here ----------")
	# remove_friend_2 = Friend.objects.filter(user_1 = user_2, user_2 = user_1)[0] |  Friend.objects.filter(user_1 = user_1, user_2 = user_2)[0] 

	if Friend.objects.filter(user_1 = user_2, user_2 = user_1).exists():
		Friend.objects.filter(user_1 = user_2, user_2 = user_1)[0].delete()
	

	if Friend.objects.filter(user_1 = user_1, user_2 = user_2).exists():
		Friend.objects.filter(user_1 = user_1, user_2 = user_2)[0].delete()


	return redirect('friends')


def wallet_view(request):
	if not request.user.is_authenticated:
		return redirect('login')
	# print(Wallet.objects.filter(user = request.user))
	balance = Wallet.objects.filter(user = request.user)[0].balance
	transactions = Transaction.objects.filter(user_1 = request.user, status = True) | Transaction.objects.filter(user_2 = request.user, status = True)

	transactions_count = len(transactions)
	args = {
		'balance' : balance,
		'transactions' : transactions,
		'transactions_count' : transactions_count

	}
	return render(request, 'wallet.html', args)


def transactions_view(request):
	if not request.user.is_authenticated:
		return redirect('login')

	transactions = Transaction.objects.filter(user_1 = request.user, status = True) | Transaction.objects.filter(user_2 = request.user, status = True)

	transactions_count = len(transactions)
	args = {
		# 'balance' : balance,
		'transactions' : transactions,
		'transactions_count' : transactions_count
	}
	return render(request, 'transactions.html', args)

def add_money_view(request):
	if not request.user.is_authenticated:
		return redirect('login')

	args = {
	
	}

	if request.method == "POST":
		amount = request.POST.get('amount')
		
		if(amount==''):
			return redirect('wallet')
		if(len(amount)>7):
			return redirect('/wallet/add_money/')
		if int(amount) > 0 :
			wallet_instance = Wallet.objects.filter(user = request.user)[0]
			if(len(str(int(wallet_instance.balance)+int(amount)))>12):
				return redirect( 'wallet' )
			wallet_instance.balance = str(int(wallet_instance.balance) + int(amount))
			wallet_instance.save()

			return redirect('wallet')

	return render(request, 'add_money.html', args)

	
def transfer_money_view(request):
	if not request.user.is_authenticated:
		return redirect('login')


	friends = (Friend.objects.filter(user_1 = request.user) | Friend.objects.filter(user_2 = request.user) ) & Friend.objects.filter(status = True)

	if request.method == "POST":
		receiver_id = request.POST.get('u_id')
		amount = request.POST.get('amount')
		if(amount==''):
			return redirect('wallet')
		if(len(amount)>7):
			return redirect('/wallet/transfer_money/')
		if(int(amount)<0):
			return redirect('/wallet/transfer_money/')
		account_balance = Wallet.objects.filter(user = request.user)[0]

		transactions = Transaction.objects.filter(user_1 = request.user, status = True) | Transaction.objects.filter(user_2 = request.user, status = True)

		transactions_count = len(transactions)

		if request.user.is_casual_user and not request.user.is_premium_user and not request.user.is_commercial_user and transactions_count>15:
			return redirect('wallet')

		if request.user.is_premium_user and not request.user.is_commercial_user and transactions_count>30:
			return redirect('wallet')


		if  int(account_balance.balance) - int(amount) >= 0 : 

			account_balance.balance = int(account_balance.balance) - int(amount)
			account_balance.save()

			user_2 = Account.objects.filter(id = receiver_id)[0]
			t = Transaction(user_1 = request.user, user_2 = user_2, status = False, payment_method = 'paytm', amount = amount)
			
			t.save()
	
		return redirect('wallet')


	args = {
		'friends' : friends
	}
	return render(request, 'transfer_money.html', args)

def accept_decline_transaction_view(request):
	if not request.user.is_authenticated:
		return redirect('login')

	transaction_requests = Transaction.objects.filter(user_2 = request.user, status = False)

	transaction_requests_count = len(transaction_requests)

	args = {
		# 'balance' : balance,
		'transactions' : transaction_requests,
		'transactions_count' : transaction_requests_count
	}

	return render(request, 'accept_decline.html', args)

def accept_transaction_view(request, t_id):
	if not request.user.is_authenticated:
		return redirect('login')

	transaction = Transaction.objects.filter(id = t_id)[0]
	print(transaction.user_1)
	user_wallet = Wallet.objects.filter(user = request.user)[0]
	print(user_wallet)
	sender_wallet = Wallet.objects.filter(user = transaction.user_1)[0]
	print(sender_wallet.balance)
	transaction_amount = transaction.amount

	user_wallet.balance = user_wallet.balance + transaction_amount
	
	user_wallet.save()

	transaction.status = True
	transaction.save()

	return redirect('accept_decline')

def decline_transaction_view(request, t_id):
	if not request.user.is_authenticated:
		return redirect('login')

	transaction = Transaction.objects.filter(id = t_id)[0]
	sender_wallet = Wallet.objects.filter(user = transaction.user_1)[0]
	sender_wallet.balance = int(sender_wallet.balance) + int(transaction.amount)
	sender_wallet.save()
	transaction.delete()

	return redirect('accept_decline')



def create_group_view(request):

	if not request.user.is_authenticated:
		return redirect('login')

	args = {
	
	}	
	return render(request, 'messenger.html', args)

def create_post_view(request, u_id):
	if not request.user.is_authenticated:
		return redirect('login')
	
	args = {
		'u_id' : u_id
	}

	if request.method == "POST":
		content = request.POST.get('post_content')
		post_to = Account.objects.filter(id = u_id)[0]
		author = request.user
		print(content)
		print(post_to)
		print(author)
		f = feed(content = content, post_to = post_to, author = author)
		f.save()

		return redirect('/profile/'+str(u_id))


	return render(request, 'create_post.html', args)

def upgrade_view(request):
	if not request.user.is_authenticated:
		return redirect('login')

	if request.user.is_commercial_user:
		user_type =  2
	elif request.user.is_premium_user:
		user_type = 1
	else: user_type = 0


	args = {
		'user_type' : user_type,
	}

	return render(request, 'upgrade.html', args)


def upgrade_payment_view(request, type):

	args = {
		'type' : int(type)
	}

	# if int(type) == 1:
		# args['payment']['2_groups'] = 50
		# args['payment']['4_groups'] = 100
		# args['payment']['any_groups'] = 150
		 
	if int(type) == 2:
		if request.user.is_verified:
			args['payment_amount'] = 5000 


	if request.method == "POST":
		print("inside")

		account = Account.objects.filter(id = request.user.id)[0]
		if(request.POST.get('amount')):
			amount = request.POST.get('amount')
			wallet = Wallet.objects.filter(user = request.user)[0]
			if(wallet.balance - int(amount) >=0):
				wallet.balance = int(wallet.balance) - int(amount)
				wallet.save()
			
				account.is_premium_user = True
				if int(amount) == 50:
					account.premium_type = 1
				if int(amount) == 100:
					account.premium_type = 2
				if int(amount) == 150:
					account.premium_type = 3
				account.save()

			return redirect('dashboard')
		
		print("very inside")
		amount = 5000
		wallet = Wallet.objects.filter(user = request.user)[0]
		print(wallet.balance)
		if(wallet.balance - int(amount) >=0):
			wallet.balance = int(wallet.balance) - amount
			print(wallet.balance)	
			wallet.save()
			account.is_commercial_user = True
			account.save()
		return redirect('dashboard')

	return render(request, 'upgrade_payment.html', args)

# adarsh

def messenger_view(request):
	if not request.user.is_authenticated:
    		return redirect('login')
	user_1 = request.user
	friends = (Friend.objects.filter(user_1 = user_1) | Friend.objects.filter(user_2 = user_1) ) & Friend.objects.filter(status = True)

	args = {
		'friends' : friends,
		'status' : 200,
		'errors' : ''
	}

	# args = {
	
	# }	
	return render(request, 'messenger.html', args)


		
def messenge_view(request,user_1,user_2):
	if not request.user.is_authenticated:
		return redirect('login')
	val=False
	mes=[]
	is_friend=False

	u_1 = Account.objects.filter(id = int(user_1))
	u_2 = Account.objects.filter(id = int(user_2))

	if u_1.count() == 0 or u_2.count() == 0:
		return redirect('home')

	u_1 = u_1[0]
	u_2 = u_2[0]

	if u_1 == None or u_2 == None:
		return redirect('home')

	if (Friend.objects.filter(user_1 = u_1, user_2=u_2)).exists() | (Friend.objects.filter(user_1 = u_2, user_2=u_1)).exists():
    		is_friend=True
	if(not is_friend):
		return redirect('home')		
	accounts = Account.objects.all()

	if u_1 == request.user:
		val = u_1.is_commercial_user | u_1.is_premium_user

	if u_2 == request.user:
		val = u_2.is_commercial_user | u_2.is_premium_user
	print(val)

	value =Message.objects.all().order_by('message_sent')
	for i in range(len(value)):
		if((int(value[i].user_1.id)==int(user_1) and int(value[i].user_2.id)==int(user_2) and is_friend) or (int(value[i].user_2.id)==int(user_1) and int(value[i].user_1.id)==int(user_2) and is_friend)):
			mes.append(value[i])
			
    					
	args1={
		'visibile' :val,
		'message' : mes,
	}

	if(request.method == 'POST'):
		mm = request.POST.get('post_area')

		if mm == '':
			return redirect('/messenger/'+user_1+'/'+user_2+'/')

		u11 = Account.objects.filter(id = int(user_1))[0]
		u21 = Account.objects.filter(id = int(user_2))[0]
		tme = timezone.now()
		var = Message(user_1 = u11,user_2 = u21,message = mm,message_sent=tme)
		print(var.message_sent)
		var.save()
		return redirect('/messenger/'+user_1+'/'+user_2+'/')
	return render(request, 'chatapp.html', args1)

def create_page_view(request):
	if not request.user.is_authenticated:
		return redirect('login')

	if not request.user.is_commercial_user:
		return redirect('dashboard')


	args = {

	}

	if request.method == "POST":
		page_title = request.POST.get('page_name')
		content = request.POST.get('content')

		p = Page(page_title = page_title, content = content, user  = request.user)
		p.save()

		print(page_title)
		print(content)



	return render(request, 'create_page.html', args)

def page_view(request, id):
	if not request.user.is_authenticated:
		return redirect('login')

	if(Page.objects.filter(id = int(id)).count() == 0):
		return redirect('dashboard')

	p_data = Page.objects.filter(id = int(id))[0]

	print(p_data.page_title)

	args = {
		'page_data' : p_data
	}

	return render(request, 'page.html', args)
