from django.http import JsonResponse
from rdflib import Graph
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
import os

g = Graph()
g.parse(os.path.join(os.path.dirname(__file__), '../../../NLP/knowledge_graph/knowledge_graph.ttl'), format='turtle')

@csrf_exempt
@require_GET
def search_triples(request):
    q = request.GET.get("q", "").lower()
    if not q:
        return JsonResponse([], safe=False)

    query = f"""
    SELECT ?s ?p ?o WHERE {{
        ?s ?p ?o .
        FILTER(CONTAINS(LCASE(STR(?s)), "{q}") || CONTAINS(LCASE(STR(?o)), "{q}"))
    }} LIMIT 100
    """

    results = g.query(query)
    triples = [
        {
            "subject": {"value": str(row.s)},
            "predicate": {"value": str(row.p)},
            "object": {"value": str(row.o)}
        }
        for row in results
    ]

    return JsonResponse(triples, safe=False)
