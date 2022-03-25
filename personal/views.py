from django.shortcuts import render
from cadastro.models import Conta

def home_screen_view(request):
	context = {}

	contas = Conta.objects.all()
	context['contas'] = contas

	return render(request, "home.html", context)
