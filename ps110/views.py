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