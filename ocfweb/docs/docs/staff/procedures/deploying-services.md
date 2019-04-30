[[!meta title="Deploying Kubernetes Services"]]

## Overview 
Are you looking to deploy a new service to the OCF Kubernetes cluster or port
an existing service from [[Marathon|doc staff/backend/mesos#h2_marathon]]? This
document will cover the steps required to do so. Do note that this is not a
substitute for a Kubernetes tutorial or a Docker tutorial (there are many
resources online for that) but a guide for getting your service running on the
OCF.

## Getting started 
This `HOWTO` will focus on one of the OCF's simplest services:
[templates][templates]. Templates is service used internally by OCF staff
serving 'copy-pasteable' email templates. Right now you should use [[git|doc
staff/backend/git]] to `clone` your repo. Now let's get the templates repo.

```
git clone git@github.com:ocf/templates.git
```

In the root of your project create a `kubernetes` folder. This is where all
your Kubernetes configuration files will live. Templates, a relatively simple
service, is a single `nginx` server serving static content. Because this
application is self-contained we need to create one file,
`kubernetes/templates.yaml`.

## Service
Since templates is a web service we will first create a `Service` object.  The
first step to make your Kubernetes service internet-facing is to make your
application accessible within the Kubernetes cluster. In most cases you can
simply fill in this template. 

```
apiVersion: v1
kind: Service
metadata:
  name: <myapp>-service
spec:
  selector:
    app: <myapp> 
  ports:
    - port: 80
      targetPort: <docker-port>
```

The `name` field under `metadata` resource is the name Kubernetes uses to
identify your `Service` object when, for example, you run `kubectl get
services`. The `selector` resource is the name you will use to bind `Pods` to
this `Service` object. Fill in the `targetPort` with the port that your
application uses _inside_ of the docker container. In the case of templates we
bind to port `8000`. Here is the `Service` configuration for templates with all
the fields filled in.

```
apiVersion: v1
kind: Service
metadata:
  name: templates-service
spec:
  selector:
    app: templates
  ports:
    - port: 80
      targetPort: 8000
```

## Creating the deployment

Great! Now let's move onto creating our pods! To do this we'll create a
`Deployment` object. Deployments can get become complicated with application
specific configuration, but the simplicity of Templates elucidates the
bare-bones requirements for any Deployment. 

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: <myapp>-deployment
  labels:
    app: <myapp>
spec:
  replicas: <#pods> 
  selector:
    matchLabels:
      app: <myapp> 
  template:
    metadata:
      labels:
        app: <myapp>
    spec:
      containers:
        - name: <container-name> 
          image: "docker.ocf.berkeley.edu/<your-repo-name>:<%= version %>"
          resources:
            limits:
              memory: <#Mi> 
              cpu: <cpus-in-millicores>m
          ports:
            - containerPort: <docker-port>
```

This section can be a bit daunting, but we'll go through it step-by-step. Fill
in `<app-name>` and `<docker-port>` with the same name you used in your
`Service`. This will ensure your Pods are bound to the `Service` we previously
created. `replicas` is the number of instances we want. Because Templates is
used internally by OCF staff, we aren't super concerned with uptime and create
only 1 instance. For a service like `ocfweb`, where uptime is crucial, we would
opt for 3 instances to handle failover.

The `containers` resource is where Kubernetes looks to obtain `docker` images
to deploy. For production services this will _always_ be the OCF docker server:
`docker.ocf.berkeley.edu`. `<your-repo-name>` is the name of the repository on
the OCF GitHub, and version will be filled in automatically by [[Jenkins|doc
staff/backend/jenkins]]. For testing, it is recommended you push your image to
[DockerHub][dockerhub] or to `docker.ocf.berkeley.edu` (talk to a root staffer
in the latter case) and use a hardcoded image name.

Lastly, we set our resource limits. Templates is a low-resource service so
we'll give it 1 megabyte of memory and `50/1000` of a CPU core (Kubernetes uses
millicores for CPU units, so 1 core = 1000m). Do note that every instance of
the application gets these resources, so with _N_ instances you are using _N *
limits_.

WARNING: On low-resource development cluster, asking for too much CPU or RAM
can put your application in an infinite `Pending` loop since the cluster will
never have enough resources to schedule your service (yes, this has happened to
us).

With all the fields filled in we have this Deployment object for Templates.

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: templates-deployment
  labels:
    app: templates
spec:
  replicas: 1
  selector:
    matchLabels:
      app: templates
  template:
    metadata:
      labels:
        app: templates
    spec:
      containers:
        - name: templates-static-content
          image: "docker.ocf.berkeley.edu/templates:<%= version %>"
          resources:
            limits:
              memory: 128Mi
              cpu: 50m
          ports:
            - containerPort: 8000
```

The last object we need to create for the Templates service is `Ingress`. We
want to expose our service to the world with the fully-qualified-domain-name
templates.ocf.berkeley.edu. Ingress, like Service objects, are similar for
most services.

```
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: virtual-host-ingress
spec:
  rules:
    - host: <myapp>.ocf.berkeley.edu
      http:
        paths:
          - backend:
              serviceName: <myapp>-service
              servicePort: 80
```

Note that `serviceName` _must_ be the same as that used in the `Service`
object. Now that we have ingress, all requests with the `Host` header
`templates.ocf.berkeley.edu` will be directed to a Templates Pod!


## Deployment extras

### OCF DNS

If your application at any point uses OCF-specific DNS, like using the hostname
`mysql` as opposed to `mysql.ocf.berkeley.edu` to access `MariaDB`, then you
need to add this under your deployment `spec`.

```
      dnsPolicy: ClusterFirst
      dnsConfig:
        searches:
          - "ocf.berkeley.edu"
```

### NFS 

If your application does not need access to the filesystem then you can skip
this section. If your application needs to keep state, try to explore `MariaDB`
as a much simpler option before making use of `NFS`.

For Kubernetes to access the file system we need two objects: a
`PersistentVolume` and a `PersistentVolumeClaim`. The former maps a filesystem
to the cluster, and the latter is how a service asks to access that filesystem.
You will need to create the `PersistentVolume` in [Puppet][puppet] as
<app-nfs-pv.yaml>. In this example we'll create 30 gigabytes of readable and
writeable storage.

```
apiVersion: v1
kind: PersistentVolume
metadata:
  name: <myapp>-nfs-pv
spec:
  capacity:
    storage: 30Gi
  accessModes:
    - ReadWriteMany
  nfs:
    path: /opt/homes/services/<myapp>
    server: filehost.ocf.berkeley.edu
    readOnly: false
```

That's all you need to add to Puppet. Now you need to add the
`PersistentVolumeClaim` object to your service. Here we will claim all 30
gigabytes of the volume we added in Puppet.

```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: <myapp>-pvc
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 30Gi
  volumeName: "<myapp>-pv"
```

Under our `deployment` we add a `volumes` sequence under `spec`. Use the
`volumeName` you chose in the `PVC`.

```
      volumes:
        - name: <myapp-data>
          persistentVolumeClaim:
            claimName: <myapp>-pvc
```

Now we've set up the volume claim. Finally, we need to tell Kubernetes to mount
this `PVC` into our docker container. Under the `container` resource add:

```
          volumeMounts:
            - mountPath: /target/path/in/my/container
              name: <myapp-data>
```


## Wrapping up

Now we have all the necessary configuration to deploy our service.  To see if
everything works, we will deploy the service manually.  On `supernova`, first
run `kinit`. This will obtain a [[kerberos|doc staff/backend/kerberos]] ticket
giving us access to the Kubernetes cluster. Now run

```
kubectl create namespace <myapp> 
kubectl apply -n <myapp> -f <myapp>.yaml 
``` 

You can run `kubectl -n <myapp> get all` to Kubernetes create your `Service`
and `Deployment` objects.

### Production Services: Setting up DNS

If you are testing your deployment, use
`<myapp>.dev-kubernetes.ocf.berkeley.edu` as your Ingress host and that will
work immediately. When you deploy your service to production, make sure to
follow the instructions below.

The final step to make your service live is to create a DNS entry for your
Kubernetes service.  You will need to clone the OCF dns repo.

```
git clone git@github.com:ocf/dns.git
```

Since we are adding DNS for a Kubernetes service, we run `ldapvi
cn=lb-kubernetes`. Add a `dnsCname` entry for your application. Run `make` and
commit your changes to GitHub. Once the DNS propagates and Puppet runs on all
the Kubernetes masters (wait about 30 minutes) your service will be accessible,
with TLS, at `<myapp>.ocf.berkeley.edu`. Congratulations!


[templates]: https://templates.ocf.berkeley.edu
[dockerhub]: https://hub.docker.com
[puppet]: https://github.com/ocf/puppet/tree/master/modules/ocf_kubernetes/files/persistent-volume-nfs
