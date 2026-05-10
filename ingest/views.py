from .models import File, Folder
from django.shortcuts import render,redirect
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from users.models import Users

#posting documents

def post_document(request):

    users = Users.objects.all()
    
    if request.method == 'POST':
        name = request.POST.get('name')
        file = request.FILES.get('file')
        folder_ids = request.POST.getlist('folders')
        notes = request.POST.get('notes')

        if not file:
            return render(request, "upload_document.html", {
                "error": "No file selected.",
                "documents": File.objects.all(),
                "users": users,
                "folders": Folder.objects.filter(owner=request.user),
            })

        # Create the document
        document = File.objects.create(name=name, file=file, notes=notes)

        # Attach selected folders
        selected_folders = Folder.objects.filter(
            id__in=folder_ids,
            owner=request.user
        )
        document.folder.set(selected_folders)

        return redirect('home')

    # GET request → show upload page
    documents = File.objects.all()

    return render(request, "upload_document.html", {
        "documents": documents,
        "users": users,
        "folders": Folder.objects.filter(owner=request.user)
    })

#deleting documents

def create_file(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        folder_id = request.POST.get('folder_id')
        uploaded_file = request.FILES.get('file')

        folder = Folder.objects.get(id=folder_id)

        File.objects.create(
            folder=folder,
            name=name or uploaded_file.name,
            file=uploaded_file
        )

        return redirect('folder_detail', folder_id=folder.id)

    folder_id = request.GET.get('folder')
    folder = Folder.objects.get(id=folder_id)
    return render(request, 'create_file.html', {'folder': folder})

class DocDeleteView(DeleteView):
    model=File
    template_name="doc_delete.html"
    fields=["name",
            "uploaded_at",
            "file"]
    success_url=reverse_lazy("home")



