from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from rest_framework_jwt.settings import api_settings




@login_required
def home(request):

	context = RequestContext(request, {'user': request.user})
	return render_to_response('home.html', context_instance=context)

@csrf_exempt
def create_auth(request):
	if request.POST.get('email') and request.POST.get('password'):
		try:
			user = User.objects.get(username=request.POST.get('email').replace(' ',''))
		except User.DoesNotExist:
			user = None
		if user:
			return HttpResponse('{"error":"username already exists"}', content_type="application/json")
		else:
			user = User.objects.create_user(
				request.POST.get('email'),
				request.POST.get('email'),
				request.POST.get('password')
			)
			jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
			jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
			payload = jwt_payload_handler(user)
			token = jwt_encode_handler(payload)
			return HttpResponse(token, content_type="application/json")
	else:
		return HttpResponse('{"error":"missing parameters, could not create user"}', content_type="application/json")

