from django.shortcuts import render
from .models import Commission


def commissions_list(request):
    """
    Display a list of all commissions.
    Uses the 'commission_list.html' template.
    """
    commissions = Commission.objects.all()
    return render(request, 'commission_list.html', {'commissions': commissions})


def commission(request, id):
    """
    Display the details of a specific commission.
    Uses the 'commission.html' template.
    """
    commission = Commission.objects.get(id=id) 
    return render(request, 'commission.html', {'commission': commission})
