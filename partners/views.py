from django.shortcuts import render
from partners.models import Partner

# === Views for partners app ===


def partners_list(request):
    """
    Generates site containing all the partners.
    If there is no image associated with the partner, the name will be displayed
    """

    partners = Partner.objects.all().order_by('name')

    context = {
        'partners': partners,
    }

    return render(request, 'partners_index.html', context)
