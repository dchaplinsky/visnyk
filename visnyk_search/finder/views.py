from django.shortcuts import render

from finder.paginator import paginated_search
from finder.elastic_models import VisnykDocument


def search(request):
    query = request.GET.get("q", "")

    docs = None
    if query:
        docs = VisnykDocument.search().query(
            "multi_match", query=query,
            operator="and",
            fields=["plain_content", "goods_name", "cust_name"])

        if docs.count() == 0:
            # PLAN B, PLAN B

            docs = VisnykDocument.search().query(
                "multi_match", query=query,
                operator="or",
                minimum_should_match="2",
                fields=["plain_content", "goods_name", "cust_name"])

        docs = paginated_search(
            request,
            docs.highlight('plain_content', order="score")
        )

    return render(request, "search.html", {
        "docs": docs,
        "query": query
    })
