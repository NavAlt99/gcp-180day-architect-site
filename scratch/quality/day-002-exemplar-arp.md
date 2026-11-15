# Exemplar: Topic 02, subtopic 3 (ARP and NDP) and dossiers 15-17

Plain text. Adapt to the spec's markup and keep the R3 discovery-link conventions.
Before using any GCP statement, re-open
https://docs.cloud.google.com/vpc/docs/compute-instance-netmasks and confirm it.

## Subtopic: ARP and NDP: resolve the local neighbor

**What it is in general:**

An IP address says where a packet is headed overall. A MAC address (the hardware
address of a network card) says which device on the current link should take the
frame next. A host needs both: the IP for the whole journey, the MAC for the next
step only.

ARP (Address Resolution Protocol, RFC 826) finds the MAC for an IPv4 address. The
host asks its local network "who has 10.240.0.1?", the owner replies with its MAC,
and the host caches the answer.

Whom does ARP ask about? If the destination is inside the host's own subnet, it
asks for the destination. If not, it asks for the gateway. It is like posting a
letter: for a neighbor you look for their door, but for another town you only need
the door of the local post office.

IPv6 does this job with NDP (Neighbor Discovery Protocol, RFC 4861), which Day 3
covers.

**Relevance to a cloud architect:**

The first debugging question is "which address did the sender try to resolve?" The
answer separates a wrong host configuration from a broken router.

Host A (10.240.0.10/26) sends to 10.240.0.75, which is in .64/26, so A must resolve
its gateway, 10.240.0.1. If A is mistakenly set to /24, it asks for .75 directly
and nobody on its link owns that address. Traffic fails even though both IPs are
valid and the router is healthy.

So check the mask and gateway before touching the router or firewall. Smaller
subnets give clear ownership, but every host then depends on a correct gateway.

**Relevance to GCP:**

The model above is the reasoning to learn, but Google Cloud's defaults differ.
Linux instances get a /32 netmask from DHCP, and broadcast traffic is not supported.

With that mask every destination looks off-link, so instances talk only to the
gateway's MAC address, even inside the same subnet.

Windows instances get the subnet's own netmask by default, and Google Cloud
intercepts ARP requests instead of delivering them to other instances (verify this
wording against the page).

A subnet can use larger netmasks only if this is set when the subnet is created
(--resolve-subnet-mask). Google calls it an advanced setting most use cases do not
need.

Inference from the facts above: the "wrong /24 mask" failure belongs to the
supplied Ethernet model, not to a default Linux VM.

**Further study:** keep the existing RFC 826 and RFC 4861 section 3.1 links. Add
"Google Cloud VPC documentation: Compute instance netmasks (accessed <actual date>)"
with the URL above.

*Simulated or predicted: what Host A would show for the supplied model (not
captured on a live system):*

    $ ip route get 10.240.0.75
    10.240.0.75 via 10.240.0.1 dev eth0 src 10.240.0.10
    $ ip neigh show 10.240.0.1
    10.240.0.1 dev eth0 lladdr 02:aa:00:00:00:01 REACHABLE
    $ ip neigh show 10.240.0.75
    (no entry: A never asks for .75 itself)

Legend line above the hop table: R is the router. R-left is its interface on A's
side (10.240.0.1). R-right is its interface on B's side (10.240.0.65). In the Frame
destination column, A and B mean those hosts' MAC addresses.

Hop table (IP addresses stay the same; the frame destination changes):

| Hop | IP source -> destination | Frame destination | Why |
| --- | --- | --- | --- |
| A -> R | .10 -> .75 | R-left | .75 is outside A's /26, so A resolved the gateway |
| R -> B | .10 -> .75 | B | .75 is on R's right-hand network .64/26, so R resolved B |
| B -> R (reply) | .75 -> .10 | R-right | .10 is outside B's /26, so B resolved its own gateway (.65) |

**Concrete example:** Read the table top to bottom. A asks for the gateway, never
for B. The router builds a new frame toward B, and B's reply goes back through the
other gateway, .65.

**Evidence limit:** The trace is calculated from the supplied addresses and masks,
with no capture. It does not show what a default Compute Engine VM does (see the
GCP row), that the router has a route back, or that firewall rules permit the
traffic.

**Architectural evaluation question:** Host A (10.240.0.10/26) sends to
10.240.0.75. Which IP address does it ARP for, and why?
Answer: 10.240.0.1, the gateway, because .75 is outside A's 10.240.0.0/26.

## Worked dossier 15: Select the ARP target for off-link traffic

**Worked starting point:** Host A (10.240.0.10/26) sends to 10.240.0.75. Its routing
table has the connected route 10.240.0.0/26 and a default route via 10.240.0.1.

| | |
| --- | --- |
| Mechanism | A compares .75 with its own network (.0 to .63) and finds it outside. A sends to the default gateway, runs ARP for 10.240.0.1 (not .75), and puts the gateway's MAC in the frame while the IP destination stays .75. |
| Ownership and boundary | Host A owns the route decision and its neighbor cache. The router owns everything after it receives the frame, so a wrong mask on A means the router never sees the traffic. |
| Failure reasoning | With a wrong /24 mask, A believes .75 is on its own link and ARPs for it. Nobody answers, so `ip neigh show 10.240.0.75` would show FAILED while the router is fine. |
| Trade-off or limit | Caching the gateway's MAC avoids an ARP exchange per packet, but a replaced gateway is not noticed until the old entry goes stale or is flushed. |
| Verification checkpoint | Run `ip route get 10.240.0.75` and confirm the "via" address is the gateway. Run `ip neigh show` and confirm an entry for the gateway and none for .75. |
| Evidence limit | This predicts A's behavior from addresses and masks alone. It does not prove the gateway answers or forwards, and a default Compute Engine Linux VM changes the first step (see the GCP row). |

## Worked dossier 16: Rewrite the frame at the router

**Worked starting point:** Router R receives a frame addressed to R-left. Inside is
an IP packet from 10.240.0.10 to 10.240.0.75. R's connected networks are
10.240.0.0/26 on R-left (.1) and 10.240.0.64/26 on R-right (.65).

| | |
| --- | --- |
| Mechanism | R strips the incoming frame header and looks up .75 in its route table. It matches the connected 10.240.0.64/26 on R-right, ARPs for .75 on that link, and builds a new frame from R-right to B. The IP addresses stay the same, and the TTL (hop counter) drops by one. |
| Ownership and boundary | The router owns forwarding and both link headers. A and B own the end-to-end conversation and never see each other's MAC address. |
| Failure reasoning | If R reused A's original frame destination, the frame would carry R-left's MAC on the wrong link and B would never accept it. |
| Trade-off or limit | Rewriting the frame at every hop lets routing scale past one link, but each link needs its own neighbor entries. A missing entry on the outgoing side delays the first packet while R asks. |
| Verification checkpoint | Write the incoming and outgoing frames side by side. Pass: the IP destination reads .75 in both, the frame destination changes from R-left to B, and the TTL is one lower. |
| Evidence limit | Predicted textbook behavior on the supplied model, with no capture. Do not expect to reproduce these two frames on GCP; the GCP row explains why its defaults differ. |

## Worked dossier 17: Check the return gateway

**Worked starting point:** B (10.240.0.75/26) replies to A (10.240.0.10/26). B's
route table has the connected 10.240.0.64/26 and a default route via 10.240.0.65.

| | |
| --- | --- |
| Mechanism | .10 is outside B's /26 (.64 to .127), so B sends the reply to its gateway, .65, and ARPs for that address. The frame goes to R-right while the IP destination stays .10. |
| Ownership and boundary | B owns its own default route. R owns forwarding back toward A. A working forward path says nothing about B's configuration. |
| Failure reasoning | If B's default gateway is missing, B cannot resolve it and never sends the reply. B's logs show the request, A sees a timeout, and the forward path looks fine. |
| Trade-off or limit | Sending both directions through the same router keeps the reasoning simple. Real networks can route returns differently on purpose, and then each direction needs its own check. |
| Verification checkpoint | On B, run `ip route get 10.240.0.10`. Pass: the "via" address is .65, as in the predicted `10.240.0.10 via 10.240.0.65 dev eth0 src 10.240.0.75` (simulated or predicted, not captured). |
| Evidence limit | Predicted from B's supplied route table. It does not show that R permits the reply or that firewall rules allow it. |
