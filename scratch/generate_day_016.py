"""Day 16 Overview and SVG Diagram Definitions."""

ACCESS_DATE = '2026-10-04'

SOURCES = {
    'topic-01': (
        'PostgreSQL Documentation: Chapter 2.6: Joins Between Tables (accessed 2026-10-04)',
        'https://www.postgresql.org/docs/current/tutorial-join.html#TUTORIAL-JOIN'
    ),
    'topic-02': (
        'PostgreSQL Documentation: Chapter 13.2: Transaction Isolation (accessed 2026-10-04)',
        'https://www.postgresql.org/docs/current/transaction-iso.html#TRANSACTION-ISO'
    )
}

PART1_HTML = '''<article class="topic-card overview" id="topic-01-overview">
<h3>Relational tables, primary/foreign keys, normalization, SELECT/JOIN/GROUP BY and…</h3>
<p><strong class="keyword">Relational database systems</strong> represent the transactional core of enterprise computing, organizing structured data into mathematical relations with strict typing and schema integrity. Relational normalization (from First to Third Normal Form) decomposes redundant entities, eliminating data anomalies while foreign key constraints guarantee referential integrity across customer and order lifecycles. Composing multi-table relational joins (<kbd>INNER</kbd>, <kbd>LEFT</kbd>) and analytical aggregations (<kbd>GROUP BY</kbd>, <kbd>HAVING</kbd>) allows systems to transform raw normalized transactional records into authoritative business outcomes.</p>
<p><strong class="side-heading">Why today:</strong> Denormalized schemas and missing foreign key constraints frequently lead to orphaned records, duplicated storage, and inconsistent inventory numbers that silently corrupt enterprise financial ledgers.</p>
<p><strong class="side-heading">Where it sits:</strong> Forms the stateful foundation of the application stack, powering Google Cloud SQL, AlloyDB, and transactional Cloud Spanner instances across production workloads.</p>
<p class="problem-preview">Problem preview: An un-normalized order database stores customer billing addresses as redundant strings directly in the orders table, resulting in data desynchronization when customers update profile details. Downstream warehouse fulfillment dispatches 1,200 orders to obsolete addresses, generating $145,000 in return logistics costs and customer delivery disputes.</p>
</article>

<article class="topic-card overview" id="topic-02-overview">
<h3>Locking/deadlocks are practised on Day 61</h3>
<p><strong class="keyword">ACID transaction semantics</strong> and isolation levels protect enterprise data integrity against partial failures and concurrent access race conditions. By wrapping multiple database mutations into an atomic unit of work (<kbd>BEGIN</kbd>, <kbd>COMMIT</kbd>, <kbd>ROLLBACK</kbd>), the database engine guarantees that either all operations succeed completely or the system reverts cleanly to its previous consistent state. Selecting appropriate transaction isolation levels (from Read Committed to Serializable) balances transactional safety against throughput, preventing fatal concurrency anomalies such as dirty reads, non-repeatable reads, and inventory overselling.</p>
<p><strong class="side-heading">Why today:</strong> Applications operating under default transaction isolation levels without concurrency controls frequently suffer from race conditions that allow identical inventory items to be sold simultaneously to multiple buyers.</p>
<p><strong class="side-heading">Where it sits:</strong> Governs database connection pools, backend transaction scopes, and distributed consistency models across Cloud SQL, Spanner, and Google Cloud application tiers.</p>
<p class="problem-preview">Problem preview: An order-processing service running under default Read Committed isolation executes non-atomic read-then-write stock checks during a flash sale. Because concurrent transactions read identical inventory counts before committing deductions, 450 customer orders are confirmed for an inventory of only 50 physical items, causing immediate inventory overselling and emergency cancellations.</p>
</article>'''

# Figure 16.1: Normalization (1NF to 3NF) Schema
FIG_16_1_HTML = '''<figure id="fig-16-1" class="diagram-figure">
<div class="diagram-wrapper" style="overflow-x: auto;">
<svg role="img" aria-labelledby="day16-norm-title day16-norm-desc" viewBox="0 0 940 370" width="940" height="370" style="max-width:100%;height:auto;display:block;margin:0 auto;background:#0d1117;border-radius:8px;">
<title id="day16-norm-title">Relational Normalization (1NF to 3NF) and Schema Architecture</title>
<desc id="day16-norm-desc">Relational database schema evolution illustrating First Normal Form atomicity, Second Normal Form partial dependency removal, and Third Normal Form transitive dependency decomposition into normalized tables with primary keys, foreign keys, and unique fulfillment constraints.</desc>
<defs>
<marker id="day16-fk-arr" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#38bdf8"/></marker>
</defs>

<!-- Column 1: Un-normalized / 1NF Table -->
<rect x="20" y="25" width="260" height="320" rx="8" fill="#161b22" stroke="#f43f5e" stroke-width="2"/>
<image href="../assets/icons/generic/database.svg" x="35" y="38" width="22" height="22"/>
<text x="65" y="54" fill="#f43f5e" font-size="12" font-weight="700">DENORMALIZED 1NF</text>
<text x="65" y="70" fill="#94a3b8" font-size="9.5">Redundant Flat Order Table</text>

<rect x="35" y="85" width="230" height="240" rx="4" fill="#21262d" stroke="#f43f5e" stroke-width="1.2"/>
<text x="45" y="104" fill="#fce7f3" font-size="10" font-weight="600">orders_flat (Denormalized)</text>
<text x="45" y="125" fill="#f43f5e" font-size="8.5">• order_id (PK)</text>
<text x="45" y="142" fill="#cbd5e1" font-size="8.5">• customer_name (Repeated)</text>
<text x="45" y="159" fill="#cbd5e1" font-size="8.5">• customer_email (Repeated)</text>
<text x="45" y="176" fill="#cbd5e1" font-size="8.5">• customer_address (Repeated)</text>
<text x="45" y="193" fill="#cbd5e1" font-size="8.5">• item_name, item_price</text>
<text x="45" y="210" fill="#cbd5e1" font-size="8.5">• quantity, total_amount</text>

<rect x="45" y="230" width="210" height="80" rx="4" fill="#1c2128" stroke="#f43f5e" stroke-width="1"/>
<text x="55" y="248" fill="#f43f5e" font-size="9" font-weight="700">Data Anomalies:</text>
<text x="55" y="264" fill="#94a3b8" font-size="8">• Update: Inconsistent addresses</text>
<text x="55" y="278" fill="#94a3b8" font-size="8">• Insertion: No customer without order</text>
<text x="55" y="292" fill="#94a3b8" font-size="8">• Deletion: Lose customer info on cancel</text>

<!-- Column 2: 2NF Partial Decomposition -->
<rect x="310" y="25" width="280" height="320" rx="8" fill="#161b22" stroke="#eab308" stroke-width="2"/>
<text x="325" y="52" fill="#eab308" font-size="12" font-weight="700">2NF DECOMPOSITION</text>
<text x="325" y="68" fill="#94a3b8" font-size="9.5">Remove Partial Dependencies</text>

<rect x="325" y="85" width="250" height="110" rx="4" fill="#21262d" stroke="#eab308" stroke-width="1.2"/>
<text x="335" y="104" fill="#fce7f3" font-size="10" font-weight="600">orders (Header)</text>
<text x="335" y="124" fill="#38bdf8" font-size="8.5">PK: order_id (INT)</text>
<text x="335" y="140" fill="#cbd5e1" font-size="8.5">customer_id, customer_name, email</text>
<text x="335" y="156" fill="#cbd5e1" font-size="8.5">order_date, total_amount_cents</text>

<rect x="325" y="210" width="250" height="115" rx="4" fill="#21262d" stroke="#eab308" stroke-width="1.2"/>
<text x="335" y="229" fill="#fce7f3" font-size="10" font-weight="600">order_items (Line Items)</text>
<text x="335" y="249" fill="#38bdf8" font-size="8.5">PK: (order_id, item_id)</text>
<text x="335" y="265" fill="#38bdf8" font-size="8.5">FK: order_id -&gt; orders.order_id</text>
<text x="335" y="281" fill="#cbd5e1" font-size="8.5">quantity, unit_price_cents</text>

<!-- Column 3: 3NF Fully Normalized Architecture -->
<rect x="620" y="25" width="300" height="320" rx="8" fill="#161b22" stroke="#34d399" stroke-width="2"/>
<image href="../assets/icons/generic/database.svg" x="635" y="38" width="22" height="22"/>
<text x="665" y="54" fill="#34d399" font-size="12" font-weight="700">3NF FULLY NORMALIZED</text>
<text x="665" y="70" fill="#94a3b8" font-size="9.5">Zero Transitive Dependencies</text>

<rect x="635" y="85" width="270" height="95" rx="4" fill="#21262d" stroke="#34d399" stroke-width="1.2"/>
<text x="645" y="104" fill="#34d399" font-size="10" font-weight="700">customers (Entity)</text>
<text x="645" y="122" fill="#38bdf8" font-size="8.5">PK: customer_id (UUID/INT)</text>
<text x="645" y="138" fill="#cbd5e1" font-size="8.5">name, email (UNIQUE), street_address</text>
<text x="645" y="154" fill="#34d399" font-size="8">✓ Address updated once; zero duplicates</text>

<rect x="635" y="190" width="270" height="135" rx="4" fill="#21262d" stroke="#34d399" stroke-width="1.2"/>
<text x="645" y="209" fill="#34d399" font-size="10" font-weight="700">orders (Header)</text>
<text x="645" y="227" fill="#38bdf8" font-size="8.5">PK: order_id (UUID/INT)</text>
<text x="645" y="243" fill="#38bdf8" font-size="8.5">FK: customer_id -&gt; customers.customer_id</text>
<text x="645" y="259" fill="#cbd5e1" font-size="8.5">status (ACCEPTED, FULFILLED), total_cents</text>
<text x="645" y="275" fill="#94a3b8" font-size="8.5">created_at (TIMESTAMP WITH TIME ZONE)</text>

<!-- Foreign Key Connector Arrow -->
<path d="M770 180 L770 190" stroke="#38bdf8" stroke-width="2" marker-end="url(#day16-fk-arr)"/>
</svg>
</div>
<figcaption>Figure 16.1: Relational database schema evolution illustrating First Normal Form atomicity, Second Normal Form partial dependency removal, and Third Normal Form transitive dependency decomposition into normalized tables with primary keys, foreign keys, and unique fulfillment constraints.</figcaption>
</figure>'''

# Figure 16.2: ACID Transaction Lifecycle & Isolation Anomaly Spectrum
FIG_16_2_HTML = '''<figure id="fig-16-2" class="diagram-figure">
<div class="diagram-wrapper" style="overflow-x: auto;">
<svg role="img" aria-labelledby="day16-acid-title day16-acid-desc" viewBox="0 0 940 330" width="940" height="330" style="max-width:100%;height:auto;display:block;margin:0 auto;background:#0d1117;border-radius:8px;">
<title id="day16-acid-title">ACID Transaction Lifecycle and ANSI SQL Isolation Anomaly Spectrum</title>
<desc id="day16-acid-desc">State machine diagram contrasting transaction states from Active to Committed or Aborted alongside the four ANSI SQL isolation levels and the concurrency anomalies they prevent.</desc>

<!-- Section 1: ACID Guarantees Box -->
<rect x="20" y="25" width="270" height="280" rx="8" fill="#161b22" stroke="#38bdf8" stroke-width="2"/>
<image href="../assets/icons/generic/policy.svg" x="35" y="38" width="22" height="22"/>
<text x="65" y="54" fill="#38bdf8" font-size="12" font-weight="700">ACID GUARANTEES</text>
<text x="65" y="70" fill="#94a3b8" font-size="9.5">Mathematical Invariants</text>

<rect x="35" y="85" width="240" height="48" rx="4" fill="#21262d" stroke="#38bdf8" stroke-width="1"/>
<text x="45" y="104" fill="#38bdf8" font-size="10" font-weight="700">A - Atomicity</text>
<text x="45" y="120" fill="#94a3b8" font-size="8.5">All-or-nothing execution; abort rolls back 100%</text>

<rect x="35" y="140" width="240" height="48" rx="4" fill="#21262d" stroke="#38bdf8" stroke-width="1"/>
<text x="45" y="159" fill="#38bdf8" font-size="10" font-weight="700">C - Consistency</text>
<text x="45" y="175" fill="#94a3b8" font-size="8.5">Transitions database between valid schema states</text>

<rect x="35" y="195" width="240" height="48" rx="4" fill="#21262d" stroke="#38bdf8" stroke-width="1"/>
<text x="45" y="214" fill="#38bdf8" font-size="10" font-weight="700">I - Isolation</text>
<text x="45" y="230" fill="#94a3b8" font-size="8.5">Concurrent transactions execute without interference</text>

<rect x="35" y="250" width="240" height="48" rx="4" fill="#21262d" stroke="#34d399" stroke-width="1"/>
<text x="45" y="269" fill="#34d399" font-size="10" font-weight="700">D - Durability</text>
<text x="45" y="285" fill="#94a3b8" font-size="8.5">Committed updates persist in WAL across crashes</text>

<!-- Section 2: Isolation Levels & Anomalies -->
<rect x="315" y="25" width="605" height="280" rx="8" fill="#161b22" stroke="#34d399" stroke-width="2"/>
<image href="../assets/icons/generic/decision.svg" x="330" y="38" width="22" height="22"/>
<text x="360" y="54" fill="#34d399" font-size="12" font-weight="700">ANSI SQL ISOLATION LEVELS &amp; CONCURRENCY ANOMALIES</text>
<text x="360" y="70" fill="#94a3b8" font-size="9.5">PostgreSQL / Cloud SQL Multi-Version Concurrency Control (MVCC)</text>

<!-- Isolation Level 1 -->
<rect x="330" y="85" width="575" height="48" rx="4" fill="#21262d" stroke="#f43f5e" stroke-width="1"/>
<text x="340" y="104" fill="#f43f5e" font-size="10" font-weight="700">Read Uncommitted</text>
<text x="480" y="104" fill="#ef4444" font-size="9">Permits Dirty Reads (Reads uncommitted dirty data)</text>
<text x="340" y="122" fill="#94a3b8" font-size="8.5">Never used in banking or inventory; not implemented in PostgreSQL (treated as Read Committed)</text>

<!-- Isolation Level 2 -->
<rect x="330" y="140" width="575" height="48" rx="4" fill="#21262d" stroke="#eab308" stroke-width="1"/>
<text x="340" y="159" fill="#eab308" font-size="10" font-weight="700">Read Committed (Default)</text>
<text x="480" y="159" fill="#fbbf24" font-size="9">Prevents Dirty Reads; Permits Non-Repeatable Reads</text>
<text x="340" y="177" fill="#94a3b8" font-size="8.5">Each query sees snapshot at query start; consecutive SELECTs within transaction can return different rows</text>

<!-- Isolation Level 3 -->
<rect x="330" y="195" width="575" height="48" rx="4" fill="#21262d" stroke="#38bdf8" stroke-width="1"/>
<text x="340" y="214" fill="#38bdf8" font-size="10" font-weight="700">Repeatable Read</text>
<text x="480" y="214" fill="#38bdf8" font-size="9">Prevents Dirty Reads &amp; Non-Repeatable Reads</text>
<text x="340" y="232" fill="#94a3b8" font-size="8.5">Entire transaction sees snapshot at transaction start; concurrent updates abort with serialization failure</text>

<!-- Isolation Level 4 -->
<rect x="330" y="250" width="575" height="48" rx="4" fill="#21262d" stroke="#34d399" stroke-width="1"/>
<text x="340" y="269" fill="#34d399" font-size="10" font-weight="700">Serializable</text>
<text x="480" y="269" fill="#34d399" font-size="9">Zero Anomalies (Strict Serializability)</text>
<text x="340" y="287" fill="#94a3b8" font-size="8.5">Guarantees execution equivalent to sequential serial order; highest safety; requires retry logic</text>
</svg>
</div>
<figcaption>Figure 16.2: ACID transaction guarantees and ANSI SQL isolation spectrum illustrating transaction lifecycle states, concurrency anomalies prevented at each isolation level, and PostgreSQL/Cloud SQL MVCC mechanics.</figcaption>
</figure>'''

# Figure 16.3: Incident 1 - Partial Write Failure
FIG_16_3_HTML = '''<figure id="fig-16-3" class="diagram-figure">
<div class="diagram-wrapper" style="overflow-x: auto;">
<svg role="img" aria-labelledby="day16-inc1-title day16-inc1-desc" viewBox="0 0 940 280" width="940" height="280" style="max-width:100%;height:auto;display:block;margin:0 auto;background:#0d1117;border-radius:8px;">
<title id="day16-inc1-title">Incident Diagram: Partial Write Transaction Failure and Atomic Rollback Remediation</title>
<desc id="day16-inc1-desc">Incident diagram contrasting an unmanaged autocommit execution path that leaves orphaned order headers when line items fail with an atomic transaction path that triggers complete rollback and enforces the duplicate fulfillment invariant.</desc>

<!-- Autocommit Failure Flow (Red) -->
<rect x="20" y="25" width="430" height="230" rx="8" fill="#161b22" stroke="#f43f5e" stroke-width="2"/>
<text x="35" y="50" fill="#f43f5e" font-size="12" font-weight="700">AUTOCOMMIT PARTIAL FAILURE (Broken Invariant)</text>

<rect x="35" y="65" width="400" height="42" rx="4" fill="#21262d" stroke="#f43f5e" stroke-width="1"/>
<text x="45" y="83" fill="#fce7f3" font-size="9.5" font-weight="600">1. INSERT INTO orders (order_id, customer_id, total_cents)</text>
<text x="45" y="98" fill="#34d399" font-size="8.5">Autocommitted immediately; order header permanently written</text>

<rect x="35" y="115" width="400" height="42" rx="4" fill="#21262d" stroke="#f43f5e" stroke-width="1"/>
<text x="45" y="133" fill="#fce7f3" font-size="9.5" font-weight="600">2. INSERT INTO order_items fails on FK / CHECK constraint</text>
<text x="45" y="148" fill="#f43f5e" font-size="8.5">Exception thrown; application aborts without rollback</text>

<rect x="35" y="165" width="400" height="75" rx="4" fill="#1c2128" stroke="#f43f5e" stroke-width="1.2"/>
<text x="45" y="185" fill="#f43f5e" font-size="10" font-weight="700">Corrupted Database State: Ghost Orders</text>
<text x="45" y="202" fill="#cbd5e1" font-size="9">• 850 orphaned order headers exist with 0 line items</text>
<text x="45" y="218" fill="#cbd5e1" font-size="9">• Customers billed $62,000; warehouse dispatches zero products</text>
<text x="45" y="232" fill="#ef4444" font-size="8.5">Audit failure: Accounting ledger desynchronized from fulfillment</text>

<!-- Atomic Transaction Flow (Green) -->
<rect x="480" y="25" width="440" height="230" rx="8" fill="#161b22" stroke="#34d399" stroke-width="2"/>
<text x="495" y="50" fill="#34d399" font-size="12" font-weight="700">ATOMIC TRANSACTION BLOCK (Remediation)</text>

<rect x="495" y="65" width="410" height="42" rx="4" fill="#21262d" stroke="#38bdf8" stroke-width="1"/>
<text x="505" y="83" fill="#fce7f3" font-size="9.5" font-weight="600">1. BEGIN TRANSACTION; INSERT order header</text>
<text x="505" y="98" fill="#38bdf8" font-size="8.5">Uncommitted changes staged in transaction WAL buffer</text>

<rect x="495" y="115" width="410" height="42" rx="4" fill="#21262d" stroke="#34d399" stroke-width="1"/>
<text x="505" y="133" fill="#fce7f3" font-size="9.5" font-weight="600">2. Line item fails; exception triggers ROLLBACK</text>
<text x="505" y="148" fill="#34d399" font-size="8.5">Engine rolls back entire transaction; zero rows modified</text>

<rect x="495" y="165" width="410" height="75" rx="4" fill="#1c2128" stroke="#34d399" stroke-width="1.2"/>
<text x="505" y="185" fill="#34d399" font-size="10" font-weight="700">100% Consistent State: Zero Orphaned Rows</text>
<text x="505" y="202" fill="#cbd5e1" font-size="9">• Database remains in pristine pre-transaction state</text>
<text x="505" y="218" fill="#cbd5e1" font-size="9">• Client receives clean HTTP 400 rejection; card not charged</text>
<text x="505" y="232" fill="#34d399" font-size="8.5">Fulfillment invariant preserved: Zero ghost orders created</text>
</svg>
</div>
<figcaption>Figure 16.3: Incident retrospective contrasting an unmanaged autocommit execution path that leaves orphaned order headers when line items fail with an atomic transaction path that triggers complete rollback and enforces the duplicate fulfillment invariant.</figcaption>
</figure>'''

# Figure 16.4: Incident 2 - Read Committed Overselling Anomaly
FIG_16_4_HTML = '''<figure id="fig-16-4" class="diagram-figure">
<div class="diagram-wrapper" style="overflow-x: auto;">
<svg role="img" aria-labelledby="day16-inc2-title day16-inc2-desc" viewBox="0 0 940 280" width="940" height="280" style="max-width:100%;height:auto;display:block;margin:0 auto;background:#0d1117;border-radius:8px;">
<title id="day16-inc2-title">Incident Diagram: Read Committed Concurrency Anomaly and Conditional Update Remediation</title>
<desc id="day16-inc2-desc">Concurrency race condition diagram contrasting Read Committed non-repeatable read anomalies that cause inventory overselling with atomic conditional updates that preserve stock invariants.</desc>

<!-- Race Condition Flow (Red) -->
<rect x="20" y="25" width="430" height="230" rx="8" fill="#161b22" stroke="#f43f5e" stroke-width="2"/>
<text x="35" y="50" fill="#f43f5e" font-size="12" font-weight="700">CONCURRENCY RACE CONDITION (Overselling)</text>

<rect x="35" y="65" width="400" height="42" rx="4" fill="#21262d" stroke="#f43f5e" stroke-width="1"/>
<text x="45" y="83" fill="#fce7f3" font-size="9.5" font-weight="600">Tx 1 &amp; Tx 2 both read: SELECT stock FROM inventory</text>
<text x="45" y="98" fill="#f43f5e" font-size="8.5">Both see stock = 1 (Initial available item count)</text>

<rect x="35" y="115" width="400" height="42" rx="4" fill="#21262d" stroke="#f43f5e" stroke-width="1"/>
<text x="45" y="133" fill="#fce7f3" font-size="9.5" font-weight="600">Both execute: UPDATE inventory SET stock = stock - 1</text>
<text x="45" y="148" fill="#f43f5e" font-size="8.5">Tx 1 commits (stock=0); Tx 2 commits (stock = -1 !)</text>

<rect x="35" y="165" width="400" height="75" rx="4" fill="#1c2128" stroke="#f43f5e" stroke-width="1.2"/>
<text x="45" y="185" fill="#f43f5e" font-size="10" font-weight="700">Flash Sale Disaster: 400 Items Oversold</text>
<text x="45" y="202" fill="#cbd5e1" font-size="9">• Inventory count dips to negative numbers</text>
<text x="45" y="218" fill="#cbd5e1" font-size="9">• 450 customer payments captured for 50 physical items</text>
<text x="45" y="232" fill="#ef4444" font-size="8.5">Outcome: 400 backorder cancellations; merchant refund fees</text>

<!-- Conditional Atomic Update (Green) -->
<rect x="480" y="25" width="440" height="230" rx="8" fill="#161b22" stroke="#34d399" stroke-width="2"/>
<text x="495" y="50" fill="#34d399" font-size="12" font-weight="700">CONDITIONAL ATOMIC UPDATE (Remediation)</text>

<rect x="495" y="65" width="410" height="42" rx="4" fill="#21262d" stroke="#38bdf8" stroke-width="1"/>
<text x="505" y="83" fill="#fce7f3" font-size="9.5" font-weight="600">1. UPDATE inventory SET stock = stock - 1 WHERE stock &gt;= 1</text>
<text x="505" y="98" fill="#38bdf8" font-size="8.5">Atomic row lock held by database engine during evaluation</text>

<rect x="495" y="115" width="410" height="42" rx="4" fill="#21262d" stroke="#34d399" stroke-width="1"/>
<text x="505" y="133" fill="#fce7f3" font-size="9.5" font-weight="600">2. Tx 1 updates 1 row; Tx 2 updates 0 rows</text>
<text x="505" y="148" fill="#34d399" font-size="8.5">Tx 2 detects rowcount == 0; cleanly triggers OUT_OF_STOCK</text>

<rect x="495" y="165" width="410" height="75" rx="4" fill="#1c2128" stroke="#34d399" stroke-width="1.2"/>
<text x="505" y="185" fill="#34d399" font-size="10" font-weight="700">Zero Overselling: Invariant Strictly Preserved</text>
<text x="505" y="202" fill="#cbd5e1" font-size="9">• Physical inventory never drops below 0</text>
<text x="505" y="218" fill="#cbd5e1" font-size="9">• Exactly 50 orders confirmed; 400 rejected gracefully at UI</text>
<text x="505" y="232" fill="#34d399" font-size="8.5">Business metric: 100% fulfillment accuracy; $0 refund penalties</text>
</svg>
</div>
<figcaption>Figure 16.4: Concurrency race condition diagram contrasting Read Committed non-repeatable read anomalies that cause inventory overselling with atomic conditional updates that preserve stock invariants.</figcaption>
</figure>'''
