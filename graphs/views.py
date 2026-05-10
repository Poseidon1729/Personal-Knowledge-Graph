from django.shortcuts import render, redirect
from neo4j import GraphDatabase
from django.conf import settings
from .forms import GraphFormSet, GraphNameForm
from ui.models import Folder
from django.http import HttpResponse, JsonResponse
from .models import GraphPosition
from django.views.decorators.csrf import csrf_exempt
import json

driver = GraphDatabase.driver(
    settings.NEO4J_URI,
    auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD),
)

def create_map_view(request):

    if request.method == "POST":

        graph_form = GraphNameForm(request.POST)
        formset = GraphFormSet(request.POST)

        if graph_form.is_valid() and formset.is_valid():

            graph_name = graph_form.cleaned_data["graph_name"]

            with driver.session() as session:

                for form in formset:

                    source = form.cleaned_data.get("source")
                    relation = form.cleaned_data.get("relation")
                    target = form.cleaned_data.get("target")

                    if not source or not relation or not target:
                        continue

                    session.run(
                        """
                        MERGE (a:File {id:$sid})
                        SET a.name = $sname,
                            a.graph = $graph

                        MERGE (b:File {id:$tid})
                        SET b.name = $tname,
                            b.graph = $graph

                        MERGE (a)-[r:RELATED {type:$rel}]->(b)
                        """,
                        sid=source.id,
                        sname=source.name,
                        tid=target.id,
                        tname=target.name,
                        rel=relation,
                        graph=graph_name
                    )


            return redirect("home")

    else:
        graph_form = GraphNameForm()
        formset = GraphFormSet()

    folders = Folder.objects.all()

    return render(
        request,
        "create_map.html",
        {
            "graph_form": graph_form,
            "formset": formset,
            "folders": folders
        }
    )

def map_detail_view(request):
    graph_name = request.GET.get("graph")
    if not graph_name:
        return HttpResponse("Graph not specified")

    query = """
    MATCH (a:File {graph:$graph})-[r:RELATED]->(b:File {graph:$graph})
    RETURN a.name AS source, r.type AS relation, b.name AS target
    """

    nodes_set = set()
    edges = []

    with driver.session() as session:
        result = session.run(query, graph=graph_name)
        for record in result:
            src = record["source"]
            tgt = record["target"]
            rel = record["relation"]
            nodes_set.add(src)
            nodes_set.add(tgt)
            edges.append({"from": src, "to": tgt, "label": rel})

    nodes = [{"id": n, "label": n} for n in nodes_set]

    # Load saved positions
    saved_positions = GraphPosition.objects.filter(graph_name=graph_name)
    position_dict = {pos.node_id: {'x': pos.x, 'y': pos.y} for pos in saved_positions}

    # Apply saved positions to nodes
    for node in nodes:
        if node['id'] in position_dict:
            node.update(position_dict[node['id']])

    return render(request, "map_detail.html", {
        "nodes": nodes,
        "edges": edges,
        "graph_name": graph_name
    })

@csrf_exempt
def save_graph_positions(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            graph_name = data.get('graph_name')
            positions = data.get('positions', [])

            if not graph_name:
                return JsonResponse({'error': 'Graph name required'}, status=400)

            # Update or create positions for each node
            for pos in positions:
                GraphPosition.objects.update_or_create(
                    graph_name=graph_name,
                    node_id=pos['id'],
                    defaults={
                        'x': pos['x'],
                        'y': pos['y']
                    }
                )

            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)