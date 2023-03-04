from django.shortcuts import render,get_object_or_404,redirect

from core.models import *

from django.db.models import Q

from django.contrib.auth.decorators import login_required
# Create your views here.

from .forms import NewItemForm,EditItemForm

def items(request):
    query  = request.GET.get('query' ,'')
    item = Item.objects.filter(is_sold = False)
    categories = Category.objects.all()

    if query:
        item = item.filter(Q(name__icontains = query) | Q(description__icontains=query) )

    param = {

        'items':item,
        'query':query,
        'categories': categories,

    }

    return render(request, 'item/items.html', param)

def detail(request, pk):

    item = get_object_or_404(Item, pk = pk)

    related_items  =Item.objects.filter( Category = item.Category,is_sold = False ).exclude(pk = pk)[0:3]



    param = {

        'item' :item,
        'related_items':related_items,

    }
    
    return render(request,'item/detail.html' ,param)

@login_required
def new(request):

    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if (form.is_valid()):
            item = form.save(commit = False)
            item.created_by = request.user

            item.save()

            return redirect('item:detail',pk=item.id ) # the pk is added because the url at item:detail take the pk by default.
    else:
        form = NewItemForm()

    param = {

        "form": form,
        "title": "add new"

    }

    return render(request, 'item/form.html',param)


@login_required
def delete(request,pk):
    item = get_object_or_404(Item, pk = pk, created_by=request.user  )

    item.delete()

    return redirect('dashboard:index')

@login_required
def edit(request,pk):

    item = get_object_or_404(Item, pk = pk, created_by=request.user)


    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance = item ) # the instace is used to specify the previous entries.

        if (form.is_valid()):
            # item = form.save(commit = False)
            # item.created_by = request.user

            item.save()

            return redirect('item:detail',pk=item.id ) # the pk is added because the url at item:detail take the pk by default.
    else:
        form = EditItemForm( instance=item ) # the instace is used to specify the previous entries.

    param = {

        "form": form,
        "title": "Edit"

    }

    return render(request, 'item/form.html',param)