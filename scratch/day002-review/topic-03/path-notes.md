# Supplied Ethernet tabletop path
A=.10/26 forwards .75 via .1 / R-left; R forwards via its .65 interface to .75 / B.
B replies via .65 / R-right toward .10. No NAT; IP endpoints retained.
Receive sequence: NIC, driver, NAPI, IP local delivery, transport/socket, process read.
Loopback skips physical NIC/DMA; queued bytes do not prove process read.
Incorrect /24 makes .75 appear on-link; use correct /26 in this supplied model.
GCP virtual gateway is not an ordinary pingable Ethernet router; GCP=untested.
SOURCE=synthetic receive challenge; queued=yes; process read=no.
Stalled worker is a hypothesis requiring application evidence.
No packet capture, live reachability, or customer acceptance was observed.
