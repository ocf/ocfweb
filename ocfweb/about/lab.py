from django.shortcuts import render


def lab_open_source(request):
    return render(
        request,
        'about/lab-open-source.html',
        {
            'title': 'Open Source in our Computer Lab',
        },
    )

def lab_vote(request):
    return render(
        request,
        'about/lab-vote.html',
        {
            'title': 'OCF: Register to vote',
        },
    )
