from django.shortcuts import render

# === Views for partners app ===


def partners_list(request):
    """

    Generates site containing all the partners.
    """

    return render(request, 'partners_index.html')
