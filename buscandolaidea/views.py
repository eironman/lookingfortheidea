from django.shortcuts import render


# Homepage
def home(request):
    return render(request, 'buscandolaidea/base_template.html')
