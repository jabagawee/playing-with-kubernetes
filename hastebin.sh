#! /bin/bash

set -e
set -o pipefail

function main() {
    check_for_yaml
    kubectl apply -f hastebin.yaml
}

function check_for_yaml() {
    if [ ! -f hastebin.yaml ]; then
        echo "Could not find hastebin.yaml!"
        exit 1
    fi
}

main
