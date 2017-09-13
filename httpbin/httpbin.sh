#! /bin/bash

set -e
set -o pipefail

function main() {
    check_for_yaml
    kubectl apply -f httpbin.yaml
}

function check_for_yaml() {
    if [ ! -f httpbin.yaml ]; then
        echo "Could not find httpbin.yaml!"
        exit 1
    fi
}

main
