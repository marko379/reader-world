from django.shortcuts import render,redirect, HttpResponseRedirect



def homito(request):
	return render(request,'homito.html')