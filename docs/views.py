from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Documents
from .forms import DocumentForm
from django.views.decorators.csrf import csrf_exempt


@login_required 
def documents_list(request):
    documents = Documents.objects.filter(users=request.user)
    return render(request,'collab/documents_list.html', {'documents': documents})

@login_required
@csrf_exempt
def document_view(request,slug):
    document = Documents.objects.get(slug=slug)
    return render(request, 'collab/document_view.html',{'document': document})

@login_required
def add_document(request):
    form = None
    if request.method == "POST":
        form = DocumentForm(request.POST)
        if form.is_valid():
            document = form.save(commit=False)
            document.creator = request.user
            document.save()
            document.users.add(request.user)
            return redirect('documents_list')       
        else:
            form = DocumentForm()
    
    return render(request, 'collab/add_document.html', {'form': form})

@login_required
def delete_document(request, slug):
    document = get_object_or_404(Documents, slug=slug)
    
    if request.method == 'POST':
        document.delete()
        return redirect('documents_list')
    
    return render(request, 'collab/confirm_delete.html', {'document': document})

#   if request.method == 'POST':
#         document.name = request.POST.get('name')
#         document.content = request.POST.get('content')
#         document.save() 

@login_required
def edit_permissions(request,slug):
    document = Documents.objects.get(slug=slug)
    
    # if request.user != document.creator:
    #     return HttpResponseForbidden()