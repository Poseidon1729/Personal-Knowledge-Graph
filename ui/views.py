from django.shortcuts import redirect, render
from ingest.models import File
from ui.models import Folder
from users.models import Users
from django.contrib.auth.decorators import login_required
from graphs.views import driver

@login_required
def home(request):
    documents = File.objects.all()
    user = Users.objects.get(id=request.user.id)
    folders = Folder.objects.filter(owner=user)

    query = """
    MATCH (a)-[r]->(b)
    RETURN DISTINCT a.graph AS graph_name
    ORDER BY graph_name
    """

    with driver.session() as session:
        result = session.run(query)
        maps = [record.data() for record in result]

    # ------------------
    # RENDER
    # ------------------
    return render(request, 'home.html', {'documents': documents, "user": user, "folders":folders, "maps":maps})



def create_folder(request):
    users = Users.objects.all()
    
    if request.method == 'POST':
        folder_name = request.POST.get('folder_name')
        parent_id = request.POST.get('parent_id')  # <-- important!
        allowed_user_ids = request.POST.getlist('allowed_users')

        parent = Folder.objects.get(id=parent_id) if parent_id else None

        folder = Folder.objects.create(
            folder_name=folder_name,
            owner=request.user,
            parent=parent
        )
        folder.allowed_users.set(allowed_user_ids)
        folder.save()

        return redirect('home')

    return render(request, "create_folder.html", {"users": users})

def folder_list(request):
    if request.method == "POST":
        name = request.POST.get("name")
        parent_id = request.POST.get("parent_id")
        parent = Folder.objects.get(id=parent_id) if parent_id else None
        
        Folder.objects.create(name=name, parent=parent)

        return redirect("folder_tree")

    # top level folders only
    root_folders = Folder.objects.filter(parent__isnull=True)
    return render(request, "folders.html", {"root_folders": root_folders})


def folder_detail(request, folder_id):
    folder = Folder.objects.get(id=folder_id)

    # THIS is the correct line:
    files = folder.files.all()

    subfolders = folder.subfolders.all()

    return render(request, 'folder_detail.html', {
        'folder': folder,
        'files': files,
        'subfolders': subfolders
    })

def create_file(request):
    pass

def map_detail_view(request):

    source = request.GET.get("source")
    target = request.GET.get("target")

    query = """
    MATCH (a {name:$source})-[r]->(b {name:$target})
    RETURN a.name AS source,
           type(r) AS relation,
           b.name AS target
    """

    nodes = set()
    edges = []

    with driver.session() as session:
        result = session.run(query, source=source, target=target)

        for record in result:
            s = record["source"]
            t = record["target"]
            rel = record["relation"]

            nodes.add(s)
            nodes.add(t)

            edges.append({
                "from": s,
                "to": t,
                "label": rel
            })

    nodes_list = [{"id": n, "label": n} for n in nodes]
    folders = Folder.objects.all()

    context = {
        "nodes": nodes_list,
        "edges": edges,
        "folders":folders
    }

    return render(request, "map_detail.html", context)