from transpire.resources import Deployment, Ingress, Secret, Service
from transpire.utils import get_revision

name = "ocfweb"


def objects():
    yield Secret(
        name="ocfweb",
        string_data={
            "metrics.htpasswd": "",
            "ocfweb.conf": "",
            "puppet-ca.pem": "",
            "puppet-cert.pem": "",
            "puppet-private.pem": "",
            "puppet-public.pem": "",
            "puppet-signed.pem": "",
        },
    ).build()

    dep = Deployment(
        name="hedgedoc",
        image="docker.ocf.berkeley.edu/ocfweb-web-deployment:latest",
        ports=[8000],
    )

    dep.obj.spec.template.spec.volumes = [
        {"name": "etc", "emptyDir": {}},
        {"name": "secrets", "secret": {"secretName": "ocfweb"}},
    ]

    dep.obj.spec.template.spec.dnsPolicy = "ClusterFirst"
    dep.obj.spec.template.spec.dnsConfig = {"searches": ["ocf.berkeley.edu"]}

    dep.obj.spec.template.spec.containers.append(
        {
            "name": "sync-etc",
            "image": "harbor.ocf.berkeley.edu/ocf/etc/sync:4c3eb1f6ba456ec30a2fbf21423364eaf0ae40bd",
            "args": ["/etc/ocf"],
            "volumeMounts": [{"name": "etc", "mountPath": "/etc/ocf"}],
        }
    )

    dep.obj.spec.template.spec.containers[0].volume_mounts.append(
        {"name": "etc", "mountPath": "/etc/ocf"},
        {"name": "secrets", "mountPath": "/etc/ocfweb"},
    )

    dep.obj.spec.template.spec.containers[0].readiness_probe = {
        "httpGet": {
            "path": "/",
            "port": 8000,
            "scheme": "HTTP",
            "httpHeaders": [{"name": "Host", "value": "www.ocf.berkeley.edu"}],
        },
        "initialDelaySeconds": 5,
        "periodSeconds": 5,
    }

    dep.obj.spec.template.spec.containers[0].liveness_probe = {
        "httpGet": {
            "path": "/",
            "port": 8000,
            "scheme": "HTTP",
            "httpHeaders": [{"name": "Host", "value": "www.ocf.berkeley.edu"}],
        },
        "initialDelaySeconds": 10,
        "timeoutSeconds": 3,
        "failureThreshold": 6,
    }

    dep.obj.spec.template.spec.containers[0].env = [
        {"name": "PUPPET_CERT_DIR", "value": "/etc/ocfweb"},
        {"name": "OCFWEB_TESTING", "value": "0"},
        {"name": "OCFWEB_PROD_VERSION", "value": get_revision()},
    ]

    yield dep.build()

    svc = Service(
        name="ocfweb",
        selector=dep.get_selector(),
        port_on_pod=8000,
        port_on_svc=80,
    )

    yield svc.build()

    ing = Ingress.from_svc(
        svc=svc,
        host="www.ocf.berkeley.edu",
        path_prefix="/",
    )

    yield ing.build()
