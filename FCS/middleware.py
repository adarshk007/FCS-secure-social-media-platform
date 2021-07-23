# from django.conf import settings
# from django.shortcuts import redirect

# class LoginRequiredMIddleware:

# 	def __init__(self, get_response):
# 		self.get_response = get_response

# 	def __call__(self, request):
# 		response = self.get_response(request)
# 		return response

# 	def process_view(self, request, view_function, view_args, view_kwargs):
# 		assert hasattr(request, 'user')

# 		if not request.user.is_authenticated():
# 			if True:
# 				return redirect('login')