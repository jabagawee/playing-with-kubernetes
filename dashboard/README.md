# Dashboard (super insecure!!!)

This is the [web UI to the API
server](https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/),
but it doesn't work by default with kubeadm. Instead of figuring out how to set
up authentication, I just created an exposed service of type NodePort that
allowed me to access the dashboard without any authentication. After we're
done, be sure to turn it off.
