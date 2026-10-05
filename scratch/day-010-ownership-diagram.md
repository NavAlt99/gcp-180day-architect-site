# Day 10 Exit Evidence: Pod / Deployment / Service Ownership Diagram
**Curriculum Scope:** Kubernetes Core Objects (Pod, Deployment, Service, Ingress, ConfigMap, Secret)

## 1. Declarative Ownership & Control Hierarchy

```text
[ Developer / GitOps Manifest ]
               │
               ▼
      [ Ingress Resource ]
               │ (defines host & path routing rules)
               ▼
      [ Service Object ] ─── (selector: app=inventory-service) ───┐
               │                                                  │ matches
               │ (virtual IP & kube-proxy / NEG routing)           │
               ▼                                                  ▼
     [ EndpointSlice ] ───────────────────────────────► [ Pod Replicas ]
                                                              ▲   ▲   ▲
                                                              │   │   │ owns
                                                      [ ReplicaSet ]
                                                              ▲
                                                              │ manages rollout
                                                      [ Deployment ]
```

## 2. Configuration & Credential Injection Hierarchy

```text
  [ ConfigMap: inventory-config ]            [ Secret: inventory-secret ]
        │ (non-sensitive vars)                    │ (encrypted credentials)
        ▼                                         ▼
   [ volumeMount: /etc/config ]              [ env: DB_PASSWORD ]
        └───────────────────┬─────────────────────┘
                            ▼
               [ Container: inventory ]
```

## 3. Core Object Function & Lifecycle Matrix

| Core Object | Controlling Component | Lifecycle & Scope | Addressing / Discovery | Failure Consequence |
|---|---|---|---|---|
| **Ingress** | Ingress Controller / Cloud Load Balancer | Global / Edge HTTP routing | Public or internal VIP + DNS | Edge HTTP 404 / 502 routing failure |
| **Service** | kube-proxy / EndpointSlice Controller | Cluster-wide stable virtual IP | ClusterIP / CoreDNS name | HTTP 503 if selector has typo |
| **Deployment** | kube-controller-manager | Declarative rollout & replica count | Managed via labels & ReplicaSets | Pods crash or unplaced if misconfigured |
| **Pod** | kubelet & Container Runtime (CRI) | Ephemeral atomic container bundle | Ephemeral Pod IP in VPC | Container restart / rescheduling |
| **ConfigMap** | kube-apiserver / etcd | Decoupled configuration values | Volume mount or env variable | Pod startup failure if key missing |
| **Secret** | kube-apiserver / Cloud KMS | Decoupled sensitive tokens | Volume mount or env variable | Authentication failure if unsealed |

## 4. Key Architectural Takeaways
1. **Never Target Pod IPs Directly:** Pods are ephemeral; always route traffic through a Service virtual IP backed by EndpointSlices.
2. **Label Selector Precision:** A single-character typo in a Service selector decouples all backend Pods without failing pod health checks.
3. **Decouple Config & Code:** Use ConfigMaps and Secrets to ensure container images remain strictly immutable and environment-agnostic.
