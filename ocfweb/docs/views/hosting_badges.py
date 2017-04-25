from django.core.urlresolvers import reverse
from django.shortcuts import render


def hosting_badges(doc, request):
    badges = [
        (name, request.build_absolute_uri(reverse('hosting-logo', args=(name,))))
        for name in [
            'ocf-hosted-penguin.svg',
            'ocf-hosted-penguin-dark.svg',
            'ocfbadge_silver8.png',
            'ocfbadge_blue8.png',
        ]
    ]

    return render(
        request,
        'docs/hosting_badges.html',
        {
            'title': doc.title,
            'badges': badges,
        },
    )
