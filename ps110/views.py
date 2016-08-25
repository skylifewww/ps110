from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
import facebook

from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from rest_framework_jwt.settings import api_settings

from event.models import Classroom

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

"""
Home - Currently a test page
"""
@login_required
def home(request):
	context = RequestContext(request, {'user': request.user})
	return render_to_response('home.html', context_instance=context)

"""
API Create new user
"""
@csrf_exempt
def create_auth(request):

	if request.POST.get('email') and request.POST.get('password'):

		try:
			validate_email(request.POST.get('email'))
		except ValidationError as e:
			return HttpResponse('{"error":"email address is not valid"}', content_type="application/json")
		else:
			print "email check passed", request.POST.get('email')


		try:
			user = User.objects.get(username=request.POST.get('email').replace(' ',''))
		except User.DoesNotExist:
			user = None
		if user:
			print user
			return HttpResponse('{"error":"username already exists"}', content_type="application/json")
		else:
			user = User.objects.create_user(
				request.POST.get('email'),
				request.POST.get('email'),
				request.POST.get('password')
			)
			# subscribe the user to the first classroom (EVERYONE)
			classroom = Classroom.objects.get(id=1)
			if classroom:
				classroom.subscribers.add(user)
			else:
				pass

			jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
			jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
			payload = jwt_payload_handler(user)
			token = jwt_encode_handler(payload)
			return HttpResponse('{"token":"'+token+'"}', content_type="application/json")
	else:
		return HttpResponse('{"error":"missing parameters, could not create user"}', content_type="application/json")

"""
API Create new user via facebook
"""
@csrf_exempt
def facebook_auth(request):
	if request.POST.get('email') and request.POST.get('id') and request.POST.get('token'):
		try:
			user = User.objects.get(username=request.POST.get('email').replace(' ',''))
		except User.DoesNotExist:
			user = None
		if user:
			jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
			jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
			payload = jwt_payload_handler(user)
			token = jwt_encode_handler(payload)
			return HttpResponse('{"token":"'+token+'"}', content_type="application/json")
		else:
			graph = facebook.GraphAPI(request.POST.get('token'))
			data = graph.get_object(request.POST.get('id')+'?fields=id,name,gender,email')
			if request.POST.get('email') == data['email'] and request.POST.get('id') == data['id']:
				user = User.objects.create_user(
					request.POST.get('email'),
					request.POST.get('email'),
					request.POST.get('password')
				)
				# subscribe the user to the first classroom (EVERYONE)
				classroom = Classroom.objects.get(id=1)
				if classroom:
					print "Adding"
					classroom.subscribers.add(user)
				else:
					print "couldnt find first classroom (everyone)"
				jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
				jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
				payload = jwt_payload_handler(user)
				token = jwt_encode_handler(payload)
				return HttpResponse('{"token":"'+token+'"}', content_type="application/json")
			else:
				return HttpResponse('{"error":"could not verify facebook auth"}', content_type="application/json")
	else:
		return HttpResponse('{"error":"missing parameters, could not create user"}', content_type="application/json")