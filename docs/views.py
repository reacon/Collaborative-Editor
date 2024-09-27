from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Documents
from .forms import DocumentForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden



@login_required 
def documents_list(request):
    documents = Documents.objects.filter(users=request.user)
    return render(request,'collab/documents_list.html', {'documents': documents})

@login_required
@csrf_exempt
def document_view(request,slug):
    document = Documents.objects.get(slug=slug)
    user_permissions = document.user_permissions.get(str(request.user.id), {})
    can_edit = user_permissions.get('can_edit')
    can_delete = user_permissions.get('can_delete')
    return render(request, 'collab/document_view.html',{'document': document,'can_edit':can_edit,'can_delete':can_delete})

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
    user_permissions = document.user_permissions.get(str(request.user.id),{})
    can_delete = user_permissions.get('can_delete')

    if not can_delete:
        return HttpResponseForbidden("You don't have permission to delete this document.")
    
    if request.method == 'POST':
        document.delete()
        return redirect('documents_list')
    
    return render(request, 'collab/confirm_delete.html', {'document': document,'can_delete':can_delete})


@login_required
def manage_permissions(request,slug):
    document = Documents.objects.get(slug=slug)
    
    if request.user != document.creator:
        return redirect('document_view', slug=slug)
    lst = []
    if request.method == "POST":
        user_permissions = {}
        
        for user in document.users.all():
            can_edit = 'can_edit_{}'.format(user.id) in request.POST
            can_delete = 'can_delete_{}'.format(user.id) in request.POST
            lst.append(can_edit)
            

            user_permissions[str(user.id)] = {'can_edit': can_edit,
                'can_delete': can_delete}
            
            document.user_permissions = user_permissions
            document.save()
    permissions = document.user_permissions
    return render(request, 'collab/manage_permissions.html', {'document': document, 'permissions': permissions})    

