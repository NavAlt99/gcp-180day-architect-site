# Local calculation / supplied address plan
web=10.240.0.0/26
app=10.240.0.64/26
database=10.240.0.128/26
management=10.240.0.192/26
Evidence: subnet-ranges.csv, subnet-ranges.json, subnet-check.txt, alignment-check.txt
10.240.0.75 belongs to app; use the supplied route trace for next-hop evidence.
GCP primary IPv4 comparison only: first two and last two reserved; source reviewed 2026-10-03.
GCP=untested; no deployed network or packet capture.
