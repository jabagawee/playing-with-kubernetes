#! /bin/bash

set -e
set -o pipefail

function main() {
    check_for_ingress_yaml
    kubectl create namespace guestbook-example
    kubectl apply -f https://raw.githubusercontent.com/kubernetes/examples/master/guestbook/all-in-one/guestbook-all-in-one.yaml -n guestbook-example
    kubectl apply -f guestbook-ingress.yaml -n guestbook-example
}

function check_for_ingress_yaml() {
    if [ ! -f guestbook-ingress.yaml ]; then
        echo "Could not find guestbook-ingress.yaml!"
        exit 1
    fi
}

main
