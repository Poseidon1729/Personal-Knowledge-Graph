from django.http import JsonResponse
from .intent_generator import process_user_query


def query_view(request):
    user_input = request.GET.get("q")

    if not user_input:
        return JsonResponse({"error": "Missing query"}, status=400)

    try:
        result = process_user_query(user_input)
        return JsonResponse(result, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)