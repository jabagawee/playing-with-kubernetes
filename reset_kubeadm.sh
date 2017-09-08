#! /bin/bash

set -e
set -o pipefail

CHOWN_USER=($id -u)
CHOWN_GROUP=($id -g)

function main() {
    cleanup
    setup_kubelet
    setup_flannel
    allow_jobs_to_schedule_on_master
    setup_nginx_forward_proxy
    setup_lego_acme_client
}

function cleanup() {
    sudo kubeadm reset
    rm -r $HOME/.kube
}

function setup_kubelet() {
    # pod network cidr for flannel
    sudo kubeadm init --apiserver-cert-extra-sans=kube.doombagoomba.com --pod-network-cidr=10.244.0.0/16

    mkdir -p $HOME/.kube
    sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
    sudo chown $CHOWN_USER:$CHOWN_GROUP $HOME/.kube/config
}

function setup_flannel() {
    kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
    kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel-rbac.yml
}

function allow_jobs_to_schedule_on_master() {
    kubectl taint nodes --all node-role.kubernetes.io/master-
}

function setup_nginx_forward_proxy() {
    kubectl create serviceaccount --namespace kube-system nginx-ingress-controller
    kubectl create clusterrolebinding nginx-ingress-controller-cluster-rule --clusterrole=cluster-admin --serviceaccount=kube-system:nginx-ingress-controller
    kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress/master/examples/deployment/nginx/kubeadm/nginx-ingress-controller.yaml
    kubectl patch deploy --namespace kube-system nginx-ingress-controller -p '{"spec":{"template":{"spec":{"serviceAccountName":"nginx-ingress-controller"}}}}'
}

function setup_lego_acme_client() {
    kubectl apply -f https://raw.githubusercontent.com/jetstack/kube-lego/master/examples/nginx/lego/00-namespace.yaml
    kubectl create serviceaccount --namespace kube-lego kube-lego
    kubectl create clusterrolebinding kube-lego-cluster-rule --clusterrole=cluster-admin --serviceaccount=kube-lego:kube-lego
    kubectl apply -f https://raw.githubusercontent.com/jetstack/kube-lego/master/examples/nginx/lego/configmap.yaml
    kubectl patch configmap --namespace kube-lego kube-lego -p '{"data":{"lego.email":"andrew@jabagawee.com"}}'
    kubectl apply -f https://raw.githubusercontent.com/jetstack/kube-lego/master/examples/nginx/lego/deployment.yaml
    kubectl patch deploy --namespace kube-lego kube-lego -p '{"spec":{"template":{"spec":{"serviceAccountName":"kube-lego"}}}}'
}

main
