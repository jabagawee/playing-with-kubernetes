#! /bin/bash

set -e
set -o pipefail

# this script will be unnecessary once
# https://github.com/kubernetes/kubernetes/issues/43962
# gets released in kubernetes
function main() {
    case $1 in
        "on")
            enable_dashboard
            ;;
        "off")
            disable_dashboard
            ;;
        *)
            echo "Usage: $0 {on|off}"
            return 1
            ;;
    esac
}

function enable_dashboard() {
    check_for_yaml
    kubectl apply -f dashboard-insecure.yaml
}

function check_for_yaml() {
    if [ ! -f dashboard-insecure.yaml ]; then
        echo "Could not find dashboard-insecure.yaml!"
        exit 1
    fi
}

function disable_dashboard() {
    kubectl delete service -n kube-system kubernetes-dashboard-insecure
}

main $@
