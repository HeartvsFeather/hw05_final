from datetime import date


def year(request):
    """Add temp with year"""
    return {
        'year': date.today().year,
    }
