from django.shortcuts import render


def docs_index(request):
    return render(
        request,
        'docs/index.html',
        {
            'title': 'Documentation',
        },
    )


def staffdocs_index(request):
    return render(
        request,
        'docs/staff_index.html',
        {
            'title': 'Staff Documentation',
            'howto_groups': [
                (
                    'User Services', [
                        'vhost',
                        'approve',
                        'paper',
                        'alumni-reset',
                    ],
                ),
                (
                    'Account Management', [
                        'check',
                        'checkacct',
                        'chpass',
                        'note',
                        'signat',
                        'sorry',
                        'unsorry',
                        'association',
                        'process-accounting',
                        'user-quotas',
                    ],
                ),
                (
                    'Maintenance', [
                        'printing',
                        'economode',
                        # TODO: restoring from backups
                        'lab-wakeup',
                    ],
                ),
                (
                    'Infrastructure', [
                        'new-host',
                        'restarting-services',
                        'migrate-vm',
                        'ssh-list',
                        'installing-updates',
                        # TODO: move kvm/libvirt here
                        'setting-up-lacp',
                        'setting-up-mdraid',
                        'ssl',
                    ],
                ),
                (
                    'Staff Admin', [
                        'granting-privileges',
                        'gapps',
                    ],
                ),
                (
                    'Development', [
                        'backporting-packages',
                        'editing-docs',
                        # TODO: move git here
                    ],
                ),
                (
                    'Other', [
                        'dmca',
                        'ocf-tv',
                        # TODO: move i3 here
                        'how',  # TODO: delete?
                        'pdf-open',  # TODO: delete or move to explainers
                    ],
                ),
            ],
        },
    )
