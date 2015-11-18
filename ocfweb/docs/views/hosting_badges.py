from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext


def hosting_badges(doc, request):
    badges = [
        (name, request.build_absolute_uri(reverse('hosting-logo', args=(name,))))
        for name in [
            'ocfbadge_mini8.png',
            'ocfbadge_mini8dark.png',
            'ocfbadge_mini8darkglow.png',
            'ocfbadge_platinum.png',
            'ocfbadge_silver8.png',
            'ocfbadge_blue8.png',
        ]
    ]

    return render_to_response(
        'hosting_badges.html',
        {
            'title': doc.title,
            'badges': badges,
        },
        context_instance=RequestContext(request),
    )
