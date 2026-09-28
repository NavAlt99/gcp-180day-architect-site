**Goal:** Read and classify IPv6 addresses, then trace a supplied dual-stack lookup. **Mode:** local Linux terminal with Python 3 plus a Markdown diagram. The example addresses are documentation fixtures; do not try to contact them. Bring Day 2's IPv4 next-hop worksheet.

### Step 1 — Confirm Python

Open a Linux terminal and run:

```sh
python3 --version
```

Expected: a Python 3 version. Open the Day 1 evidence repository and create a note named `day-003-ipv6.md` with your editor. Record the version you observed.

### Step 2 — Parse addresses and a prefix

Copy and run this offline Python script:

```sh
python3 - <<'PY'
from ipaddress import IPv6Address, IPv6Network

address = IPv6Address('2001:0db8:0000:0000:0000:0000:0000:0010')
network = IPv6Network('2001:db8:abcd:1200::/64')
print('compressed:', address.compressed)
print('network:', network.network_address, 'prefix:', network.prefixlen)
print('loopback:', IPv6Address('::1').is_loopback)
print('link-local:', IPv6Address('fe80::1').is_link_local)
PY
```

Expected output:

```text
compressed: 2001:db8::10
network: 2001:db8:abcd:1200:: prefix: 64
loopback: True
link-local: True
```

The script shows zero compression, a `/64` network prefix and two special address scopes. If parsing fails, check the number of colons and the placement of `::`. Save the actual output in the note; do not replace it with the expected text.

### Step 3 — Trace supplied resolver answers

Use these fixture records, not a live DNS query:

```text
orders.example.test A    192.0.2.25
orders.example.test AAAA 2001:db8:abcd:1200::25
```

Draw two paths. The IPv4 path ends at address `192.0.2.25`, TCP port `443`. The IPv6 path ends at address `2001:db8:abcd:1200::25`, TCP port `443`. Mark the A and AAAA lookups as name resolution only. Both addresses are from documentation ranges ([RFC 5737](https://datatracker.ietf.org/doc/html/rfc5737), [RFC 3849](https://datatracker.ietf.org/doc/html/rfc3849)).

### Step 4 — Inject and diagnose one failure

Add these observations to the diagram:

```text
IPv4: A answer returned; route present; TCP handshake established.
IPv6: AAAA answer returned; client has no route to the IPv6 destination.
```

Predict the result: the IPv6 name lookup succeeds, but its TCP handshake cannot start successfully. Note the next evidence you would seek: the selected IPv6 source address and route. A working IPv4 response does not repair the IPv6 path.

### Step 5 — Verify and keep the artifact

Under the diagram, answer separately what the DNS reply proves, what a completed TCP handshake proves, and what an HTTP response would prove. The note passes when it contains the four actual Python results, both socket endpoints and the first failing IPv6 boundary. Link it into Day 3's combined DNS/transport artifact.

No cloud or network resource was created. Keep the note and script output; there is nothing to delete.
