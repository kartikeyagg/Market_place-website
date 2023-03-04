from django.shortcuts import render,redirect

# Create your views here.

# from item.models import 

from .models import Category, Item

from .forms import SignupForm

def index(request):

    # items = Item.objects.filter()

    items = Item.objects.filter(is_sold = False)[0:6]
    categories = Category.objects.all()
    params = {

        'items': items,
        'categories':categories

    }
    return render(request, 'core/index.html',params)

def contact(request):

    return render(request, 'core/contact.html')


def signup(request):

    if request.method == 'POST':
        form = SignupForm(request.POST)


        if form.is_valid():
            form.save()


            return redirect('/login/')
    else:
        form = SignupForm()
    param = {

        'form':form,

    }
    return render(request,'core/signup.html', param)