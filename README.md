# My personal Kubernetes configs

This is a collection of scripts that I found helpful when starting my own
Kubernetes server.

Shout out to [@garybernhardt](https://github.com/garybernhardt) for his style
tricks that influenced how I wrote this bash scripts.

## Fresh Start

If you ever needed a script to just repeatedly teardown and bring back up
a full Kubernetes cluster, check out [reset_kubeadm.sh](reset_kubeadm.sh),
which turns up a Kubernetes cluster via the instructions on [Using kubeadm to
Create
a Cluster](https://kubernetes.io/docs/setup/independent/create-cluster-kubeadm/).

I chose Flannel as the pod network and set up Let's Encrypt + nginx as an
[Ingress
controller](https://kubernetes.io/docs/concepts/services-networking/ingress/#ingress-controllers)
to back all future ingress resources. You might note that I have hardcoded
cluster-admin role service accounts for them which is probably a security
problem, but this is for my personal/fun box at home so I'm not too worried.

There's also a bunch of hardcoded values specific to me, like my email address
for [Let's Encrypt](https://letsencrypt.org) or a reference to
doombagoomba.com, my domain.

## Examples

### Dashboard (super insecure!!!)

This is the [web UI to the API
server](https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/),
but it doesn't work by default with kubeadm. Instead of figuring out how to set
up authentication, I just created an exposed service of type NodePort that
allowed me to access the dashboard without any authentication. After we're
done, be sure to turn it off.

### Guestbook

This is the [sample guestbook
application](https://kubernetes.io/docs/tutorials/stateless-application/guestbook/)
on the Kubernetes documentation. i used it quite a bit to debug the ingress
setup, and I added a handwritten ingress resource at
[guestbook-ingress.yaml](guestbook-ingress.yaml).

### Httpbin

This was put in because I wanted to try learning to write my own yaml instead
of using one that someone else wrote. It's a simple Kubernetes deployment
around [httpbin](http://httpbin.org/) by
[@kennethreitz](https://github.com/kennethreitz), along with exposure as
a service and an ingress resource, all tucked safely away in its own namespace.
