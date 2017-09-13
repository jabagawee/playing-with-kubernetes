# Fresh Start

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
