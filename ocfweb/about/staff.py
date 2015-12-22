from django.shortcuts import render


def about_staff(request):
    return render(
        request,
        'staff.html',
        {
            'title': 'Join the Staff Team',
        },
    )
