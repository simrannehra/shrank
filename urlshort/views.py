from django.http import Http404,HttpResponseRedirect,HttpResponse
from .forms import addurl,UserForm,loginForm
from django.contrib.auth import authenticate ,login,logout
from django.views.generic import View 
from .models import Sam
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required

class UserFormView(View):
	form_class = UserForm
	template_name = 'urlshort/registration.html'

	def get(self,request):
		form = self.form_class(None)
		return render(request,self.template_name,{'form':form})
	def post(self,request):
		form = self.form_class(request.POST)

		if form.is_valid():

			user = form.save(commit=False)
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user.set_password(password)
			user.save()
			user = authenticate(username=username ,password =password)

			if user is not None:
				if user.is_active:
					login(request,user)
					return redirect('urlshort:suceess')
		return render(request,self.template_name,{'form':form})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/account/login/')


class LoginFormView(View):
	form_class = loginForm
	template_name = 'urlshort/login.html'

	def get(self,request):
		if request.user.is_authenticated():
			return redirect('urlshort:suceess')
		form = self.form_class(None)
		return render(request,self.template_name,{'form':form})
	def post(self,request):
		if request.method == 'POST':
			form = self.form_class(None)
			username = request.POST.get('username')
			password = request.POST.get('password')
			user = authenticate(username=username, password= password)
			if user:
				if user.is_active:
					login(request,user)
					return HttpResponseRedirect('/')
				else:
					return HttpResponse("Your Rango is disabled .")
			else:
				return render(request,self.template_name,{'form':form,'error_message':"Login details are not correct !!!"})




def record(request):
	if not request.user.is_authenticated():
			return redirect('urlshort:suceess')
	instance=Sam.objects.filter(user=request.user)
	return render(request,'urlshort/record.html',{'instance':instance})



def test(request,url_id):
	sam =get_object_or_404(Sam,shorten=url_id) 
	sam.clicks=int(sam.clicks)+1
	sam.save()
	return redirect(sam.originalurl)

def index(request):
	if request.method=='GET':
		return render(request, 'suceess.html',{})
	if request.user.is_authenticated():
		user=request.user
	else:
		obj=Sam.objects.get(pk=1)
		user=obj.user
		print (obj.user)
	Original=request.POST.get('Original')
	Custom=request.POST.get('Custom')
	if not Custom:
		Custom=create()
	try:
		objectx=Sam.objects.get(shorten=Custom)
		return render(request, 'suceess.html',{"error":"Custom url is not available"})
	except Sam.DoesNotExist:
		instance=Sam.objects.create(originalurl=Original,shorten=Custom,user=user)
		instance.save()
		string="http://127.0.0.1:8000/"+Custom
		return render(request, 'suceess.html',{"custom":string})

def create():
	counts=Sam.objects.all().count()
	arr=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
	string=''
	for _ in range(4):
		string=arr[int(counts%26)]+string
		counts/=26
	string=string+str(int(counts))
	return string


def index2(request):
	
	user=request.user
	form = addurl(request.POST or None)
	form2=addurl(None)
	context ={
		"form": form2,
	}
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user=user
		try:
			objectx=Sam.objects.get(shorten=instance.shorten)
			return render(request, 'suceess2.html',context)
		except Sam.DoesNotExist:
			instance.save()
			return render(request, 'suceess.html',context)
	else:
		return render(request, 'suceess.html',context)
