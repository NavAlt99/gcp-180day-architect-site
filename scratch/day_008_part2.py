"""Technical discussion for Topic 2: Diagnostic command-line utilities."""

TOPIC_02_TECH = '''<p><strong class="side-heading">Subtopics in this discussion:</strong></p>
<ul>
<li>Stream text filtering with grep and sed: patterns, word boundaries, and limits</li>
<li>Field processing with awk: columnar aggregation, record splitting, and reporting</li>
<li>Structured data parsing with jq: JSON filters, nested traversal, and numeric selections</li>
<li>Network endpoint diagnostics: curl and dig for DNS and application layer probing</li>
<li>Kernel socket and packet analysis: ss socket states and tcpdump packet captures</li>
</ul>

<h4>Stream text filtering with grep and sed: patterns, word boundaries, and limits</h4>
<p><strong class="side-heading">What it is in general:</strong> Text stream inspection tools process unstructured log streams line-by-line using regular expressions. The <strong class="keyword">grep</strong> utility evaluates input streams against Basic Regular Expressions (BRE) or Extended Regular Expressions (ERE with <code>-E</code>), returning matching records based on exact literal substrings, character classes, or word boundaries (<code>\b</code>). Options such as <code>-i</code> (case-insensitivity), <code>-v</code> (inverting matches), <code>-c</code> (counting occurrences), and <code>-C</code> (emitting surrounding context lines) allow operators to quickly narrow down unstructured syslogs. The <strong class="keyword">sed</strong> (stream editor) utility performs non-interactive text transformations, deletions, and substitutions on piped streams using programmable addressing scripts (e.g. <code>s/regex/replacement/g</code>). Crucially, stream text tools evaluate records as flat string sequences: they lack schema awareness, syntactic data validation, and multiline field boundary understanding.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Relying on naive text grepping across semi-structured or JSON application logs introduces severe false-negative and false-positive diagnostic errors: searching for the substring <code>"error"</code> misses structured numeric failure codes (such as HTTP 500 or gRPC status 14), while returning false positives for informational logs stating <code>"error_count=0"</code> or customer addresses containing "Terrace". Architects mandate structured logging schemas and establish standardized log parsing rules for observability pipelines.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> While Google Cloud CLI commands support local piping to grep (e.g. <kbd>gcloud compute instances list | grep RUNNING</kbd>), enterprise cloud operations utilize Cloud Logging log filters (written in Cloud Logging Query Language) on the backend to filter structured JSON payload fields server-side before egressing data over networks. Primary documentation: <a href="https://man7.org/linux/man-pages/man1/grep.1.html#DESCRIPTION">grep(1) pattern search utility description (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://man7.org/linux/man-pages/man1/grep.1.html#DESCRIPTION">grep(1) regular expression syntax and matching modes (accessed 2026-10-04)</a>; <a href="https://man7.org/linux/man-pages/man1/sed.1.html#DESCRIPTION">sed(1) stream editor command language (accessed 2026-10-04)</a>.</p>

<h4>Field processing with awk: columnar aggregation, record splitting, and reporting</h4>
<p><strong class="side-heading">What it is in general:</strong> When log streams or system command outputs follow tabular, columnar formatting (such as space-delimited Web server access logs, <code>vmstat</code>, or <code>ps</code> outputs), the <strong class="keyword">awk</strong> pattern scanning and processing language provides powerful field-based extraction and statistical computation. The tool automatically splits each incoming line into positional field variables (<code>$1</code>, <code>$2</code>, ... <code>$NF</code>) based on a configurable field separator (<code>-F</code>). In addition to printing specific columns, awk supports associative arrays, arithmetic aggregations, conditional branching, and pattern action blocks (<code>BEGIN</code>, pattern matching, <code>END</code>). This allows operators to compute average latency, calculate response code percentiles, or identify top talker IP addresses from access log streams in a single one-line command without writing full Python or shell scripts.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Field extraction tools allow operators to extract actionable quantitative metrics from legacy flat log files during real-time incident triage without requiring external log aggregation databases to be functional. However, column-positional parsing breaks immediately if upstream log formats introduce unquoted spaces within fields or alter column ordering.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Compute Engine serial console logs, Linux startup script logs (<code>/var/log/messages</code>), and Google Cloud Ops Agent local configuration files frequently require column-based extraction during bare-metal instance debugging. Architects standardize log formats on structured JSON to replace brittle positional awk scripts with schema-validated parsers. Primary documentation: <a href="https://man7.org/linux/man-pages/man1/gawk.1.html#DESCRIPTION">gawk(1) pattern scanning and processing language description (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://man7.org/linux/man-pages/man1/gawk.1.html#DESCRIPTION">gawk(1) field splitting, patterns, and actions (accessed 2026-10-04)</a>; <a href="https://man7.org/linux/man-pages/man1/grep.1.html#DESCRIPTION">grep(1) matching options and context control (accessed 2026-10-04)</a>.</p>

<h4>Structured data parsing with jq: JSON filters, nested traversal, and numeric selections</h4>
<p><strong class="side-heading">What it is in general:</strong> Modern cloud telemetry, API payloads, and container runtime logs are formatted as JavaScript Object Notation (JSON). The <strong class="keyword">jq</strong> command-line processor provides a complete, type-aware query language for slicing, filtering, mapping, and transforming structured JSON documents. Unlike text stream filters, jq parses JSON text into an in-memory Document Object Model (DOM), validating syntax and supporting hierarchical path traversals (e.g. <code>.user.credentials[0].id</code>). It supports exact type comparisons, boolean filtering (e.g. <code>select(.http.status_code &gt;= 500)</code>), array projections, field restructuring, and raw text output (<code>-r</code>). If an input stream contains corrupted or non-JSON text, jq fails explicitly with a syntax parse error rather than silently returning erroneous empty output.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> JSON-aware parsing is mandatory for automated continuous deployment gates, incident triage scripts, and cloud telemetry evaluation. Parsing JSON with grep or sed is a severe anti-pattern that leads to false conclusions during production outages: key ordering in JSON objects is non-deterministic, whitespace is arbitrary, and numeric values cannot be filtered by relational inequalities without a true JSON engine.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> The Google Cloud CLI (<kbd>gcloud</kbd>) returns structured JSON for all administrative resource queries via the global flag <code>--format=json</code>. Cloud architects pair gcloud JSON output with jq to extract project IDs, VPC subnet allocations, firewall rule configurations, and instance status fields reliably across automated deployment pipelines. Primary documentation: <a href="https://man7.org/linux/man-pages/man1/grep.1.html#DESCRIPTION">grep(1) pattern search utility description (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://man7.org/linux/man-pages/man1/grep.1.html#DESCRIPTION">grep(1) comparison with structured filtering (accessed 2026-10-04)</a>; <a href="https://man7.org/linux/man-pages/man1/gawk.1.html#DESCRIPTION">gawk(1) structured field processing (accessed 2026-10-04)</a>.</p>

<h4>Network endpoint diagnostics: curl and dig for DNS and application layer probing</h4>
<p><strong class="side-heading">What it is in general:</strong> Probing service availability across network boundaries requires tools that isolate name resolution from application protocol transactions. The <strong class="keyword">dig</strong> (domain information groper) utility performs flexible DNS lookups directly against designated nameservers (<code>@nameserver</code>), querying specific record types (A, AAAA, CNAME, SRV), tracing delegation hierarchies from root servers (<code>+trace</code>), and displaying authoritative DNS flags, return codes (NOERROR, NXDOMAIN, SERVFAIL), and Time-To-Live (TTL) expiration counters. The <strong class="keyword">curl</strong> command-line tool transfers data across network protocols (HTTP, HTTPS, FTP), allowing operators to inspect raw HTTP status headers (<code>-I</code>), view TLS handshakes and cipher negotiation (<code>-v</code>), override DNS resolution locally without changing <code>/etc/hosts</code> (<code>--resolve</code>), and extract detailed network timing breakdowns using write-out format variables (<code>-w "%{time_namelookup} %{time_connect} %{time_appconnect} %{time_total}\n"</code>).</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Testing network connectivity requires isolating the failure boundary: an API call failure can originate from DNS misconfiguration, firewall blockages, TLS certificate expiration, or backend service application crashes. Probing with dig isolates whether the domain name maps to the correct IP address; probing with curl isolates whether TCP transport, TLS negotiation, and HTTP routing succeed independently.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Cloud architects utilize dig to verify Google Cloud DNS private zones, Split-Horizon DNS configurations, and DNS forwarding rules. They utilize curl to probe Google Cloud Internal Application Load Balancers, Cloud Run endpoints, and Cloud Storage signed URLs, verifying IAM authentication headers and inspecting latency metrics along the Google Cloud network path. Primary documentation: <a href="https://man7.org/linux/man-pages/man1/curl.1.html#DESCRIPTION">curl(1) command-line URL transfer tool description (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://man7.org/linux/man-pages/man1/curl.1.html#DESCRIPTION">curl(1) HTTP transfer options and timing variables (accessed 2026-10-04)</a>; <a href="https://man7.org/linux/man-pages/man1/grep.1.html#DESCRIPTION">grep(1) searching command output (accessed 2026-10-04)</a>.</p>

<h4>Kernel socket and packet analysis: ss socket states and tcpdump packet captures</h4>
<p><strong class="side-heading">What it is in general:</strong> When higher-level HTTP or application diagnostic tools report connectivity failures, operators drop to the transport and network layers to observe kernel socket tables and interface packet streams. The <strong class="keyword">ss</strong> (socket statistics) utility dumps live kernel socket tables directly from the Linux <code>inet_diag</code> netlink subsystem, replacing the legacy <code>netstat</code> command. It displays active listening ports (<code>-l</code>), established TCP connections (<code>-t</code>), UDP sockets (<code>-u</code>), associated process PIDs (<code>-p</code>), and socket buffer queue depths (<code>Recv-Q</code> and <code>Send-Q</code>). Sockets with high <code>Recv-Q</code> indicate that the application process is backlogged and failing to consume incoming TCP payload bytes from the kernel buffer. The <strong class="keyword">tcpdump</strong> utility captures raw network packets directly from the network interface using the <code>libpcap</code> library and kernel Berkeley Packet Filters (BPF). Filtering packets by protocol, IP address, port, and TCP flags (e.g. SYN, ACK, RST), tcpdump proves whether packets are physically arriving at the network interface or being dropped before reaching the host.</p>
<p><strong class="side-heading">Relevance to a cloud architect:</strong> Transport-level tools provide ground truth during perimeter connectivity failures: an operator can definitively prove whether a packet reached the virtual machine or was dropped by upstream VPC firewall rules by capturing packets on the VM network interface. Socket queue inspection with ss separates application deadlocks (zero socket reads) from external network routing failures.</p>
<p><strong class="side-heading">Relevance to GCP:</strong> Compute Engine virtual interfaces (virtio-net or gVNIC) process traffic encapsulated within Andromeda virtual networking. Running tcpdump inside a Compute Engine VM captures traffic only after it has traversed VPC firewall evaluation. To observe packets blocked by VPC firewalls before reaching the instance, architects enable Google Cloud VPC Flow Logs and Packet Mirroring rather than relying exclusively on VM-local tcpdump. Primary documentation: <a href="https://man7.org/linux/man-pages/man8/ss.8.html#DESCRIPTION">ss(8) socket statistics utility description (accessed 2026-10-04)</a>.</p>
<p><strong class="side-heading">Further study:</strong> <a href="https://man7.org/linux/man-pages/man8/ss.8.html#DESCRIPTION">ss(8) TCP connection states and socket memory (accessed 2026-10-04)</a>; <a href="https://man7.org/linux/man-pages/man8/tcpdump.8.html#DESCRIPTION">tcpdump(8) network traffic capture and filter syntax (accessed 2026-10-04)</a>.</p>

<div class="table-responsive">
<table class="table">
<caption>Tool-to-boundary map: selecting appropriate diagnostic instruments based on failure hypothesis.</caption>
<thead>
<tr>
<th>Diagnostic Question</th>
<th>Tool</th>
<th>Evidence Produced</th>
<th>Visibility Limit</th>
</tr>
</thead>
<tbody>
<tr>
<td>Which structured records failed?</td>
<td><code>jq</code> or JSON parser</td>
<td>Extracted numeric status codes and error payloads</td>
<td>Valid only for supplied structured records; cannot prove live network health</td>
</tr>
<tr>
<td>Which IP address is resolved?</td>
<td><code>dig</code></td>
<td>Authoritative DNS record, TTL, and return code</td>
<td>Proves name resolution only; does not prove network reachability or open ports</td>
</tr>
<tr>
<td>Is a local socket listening?</td>
<td><code>ss</code></td>
<td>Kernel socket table state, PID, and buffer depths</td>
<td>Shows local host state only; does not prove upstream VPC firewall rules permit traffic</td>
</tr>
<tr>
<td>What HTTP response was returned?</td>
<td><code>curl</code></td>
<td>Status code, response headers, and handshake timings</td>
<td>Valid for tested URL path and client identity; does not prove health of other routes</td>
</tr>
<tr>
<td>Are packets arriving at the interface?</td>
<td><code>tcpdump</code></td>
<td>Raw packet headers, timestamps, and TCP flags</td>
<td>Constrained by interface visibility; cannot inspect traffic dropped upstream by VPC firewalls</td>
</tr>
</tbody>
</table>
</div>

{FIG_8_2_HTML}

<p><strong class="side-heading">Concrete example:</strong> An incident responder investigates elevated error rates on an authentication service. Inspecting <code>/var/log/auth.jsonl</code> with a naive string search <kbd>grep "error" auth.jsonl</kbd> returns zero lines because the microservice emits structured JSON records where failures are logged as <code>{"status": 503, "code": "upstream_timeout"}</code> without textual error keywords. By running structured JSON filtering <kbd>python3 -c "import sys, json; [print(r['order_id']) for r in map(json.loads, sys.stdin) if r.get('status', 0) >= 500]" &lt; auth.jsonl</kbd>, the responder extracts 100% of the failed transactions, correlating failure timestamps with socket pool exhaustion observed via <kbd>ss -s</kbd>.</p>

<p><strong class="side-heading">Evidence limit:</strong> Command-line diagnostic tools yield evidence specific to the isolated boundary they inspect; a successful DNS lookup or local socket state does not prove end-to-end transport reachability or distributed application health without end-to-end transaction tracing.</p>
'''
