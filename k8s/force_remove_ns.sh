# Force remove the namespace
# Usage: ./force_remove_ns.sh <namespace>

namespace=$1

(
echo "Force remove the namespace $namespace"
kubectl proxy &
kubectl get namespace $namespace -o json |jq '.spec = {"finalizers":[]}' >temp.json
curl -k -H "Content-Type: application/json" -X PUT --data-binary @temp.json 127.0.0.1:8001/api/v1/namespaces/$namespace/finalize
echo "Namespace $namespace removed"
)