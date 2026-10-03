# Supplied design review
A UDS is local to its OS; a moved helper needs a reachable network interface and authentication/message-contract design.
Loopback refers to the caller network namespace.
Local application-to-proxy and remote proxy-to-database are different boundaries.
Cloud SQL Auth Proxy socket choice requires documented platform/client compatibility and authentication/connection prerequisites.
GCP=untested; latency and throughput=unmeasured; source review=2026-10-03.
