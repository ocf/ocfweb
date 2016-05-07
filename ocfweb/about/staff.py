from django.shortcuts import render


def about_staff(request):
    return render(
        request,
        'about/staff.html',
        {
            'title': 'Join the Staff Team',
        },
    )
