"""Day 131 authoring data: lifecycle controls, policy exceptions, and adoption."""

DAY_NUM = 131

DATA = {
    'day': 131,
    'part1_intro': (
        'Day 131 turns platform governance into an operating lifecycle: every resource has a responsible owner, cost and purpose '
        'metadata, a review date, a retirement path, and evidence that cleanup completed. It then applies the same discipline to a '
        'team request for a nonstandard runtime, where a time-bounded exception must keep business continuity, blast radius, funding, '
        'and staff capability visible. The practice is deliberately a synthetic design review; it does not create cloud resources or '
        'change a live organization policy.'
    ),
    'exit_summary': (
        'A written nonstandard-runtime exception decision and resource lifecycle policy, with named owners, funding and cleanup '
        'responsibilities, training actions, expiry dates, evidence checks, and explicit review triggers.'
    ),
    'part2_intro': (
        'Follow the governance path from resource inventory and ownership metadata through policy evaluation, a time-boxed exception, '
        'operational readiness, and a verified retirement or renewal decision. The architecture boundary is organizational: metadata '
        'helps people find and attribute resources, while policy constraints control permitted actions and service-specific cleanup '
        'still needs its own checks.'
    ),
    'arch_table_html': '''<div class="table-container"><table><thead><tr><th>Control</th><th>Owner and boundary</th><th>Evidence and trigger</th><th>Limit and trade-off</th></tr></thead><tbody>
<tr><td>Resource registry</td><td>Service owner supplies purpose, team, cost center, environment, data class, creation date, and review date; platform team defines required fields.</td><td>Inventory export has no unowned production resources; missing or stale owner metadata opens a named remediation item.</td><td>Labels are queryable annotations, do not automatically propagate from projects to child resources, and do not themselves enforce policy. Service-level support varies.</td></tr>
<tr><td>Expiry and cleanup</td><td>Workload owner proposes retention and dependency order; operations validates backup, retention, and recovery obligations before deletion.</td><td>Expiry queue identifies due resources; deletion record includes resource ID, approver, backup check, result, and timestamp.</td><td>Automatic deletion is fast but can remove a dependency or evidence needed for recovery. Quarantine and review reduce accidental removal at the cost of temporary spend.</td></tr>
<tr><td>Policy guardrail rollout</td><td>Platform/security team owns constraints at the organization or folder boundary; application teams supply representative requests.</td><td>Dry-run or simulator findings are reviewed by service owner and policy owner before staged enforcement; denied requests identify the violated constraint.</td><td>Dry-run coverage is limited to supported constraints and logged observations do not prove that every workload path was exercised.</td></tr>
<tr><td>Exception and adoption</td><td>Business sponsor funds the exception; platform owner accepts bounded risk; service owner operates it; named reviewer closes or renews it.</td><td>Exception record has scope, compensating controls, expiry, training owner, continuity test, and review triggers.</td><td>Exceptions preserve delivery flexibility but add a distinct support path, recurring review work, and concentration risk if expertise is held by one person.</td></tr>
</tbody></table></div>''',
    'arch_diagram': {
        'type': 'topology',
        'title': 'Day 131: Resource lifecycle and exception governance boundaries',
        'desc': 'Accessible governance flow from inventory ownership metadata to policy evaluation, bounded exception, adoption readiness, and cleanup evidence. Metadata, enforcement, and deletion are separate boundaries.',
        'caption': 'Figure 131.1: Governance path and ownership boundaries. This design view does not prove that a particular organization policy is available, that an inventory is complete, or that cleanup is safe for a live workload.',
        'width': 1100, 'height': 660,
        'layers': [
            {'name':'LAYER 1: Inventory and resource identity','desc':'Resource IDs, owner, purpose, cost center, data class','y':10,'h':90,'stroke':'#38bdf8','fill':'#0c1e38','title_color':'#38bdf8'},
            {'name':'LAYER 2: Lifecycle state and review clock','desc':'Create → operate → quarantine → retire / renew','y':115,'h':90,'stroke':'#22c55e','fill':'#072417','title_color':'#22c55e'},
            {'name':'LAYER 3: Policy evaluation boundary','desc':'Supported constraint, inheritance, test evidence','y':220,'h':90,'stroke':'#818cf8','fill':'#141838','title_color':'#818cf8'},
            {'name':'LAYER 4: Time-bounded exception and continuity','desc':'Sponsor, compensating controls, runbook, funding','y':325,'h':90,'stroke':'#f59e0b','fill':'#261a08','title_color':'#f59e0b'},
            {'name':'LAYER 5: Adoption, review, and closure evidence','desc':'Training, exercise, review triggers, cleanup receipt','y':430,'h':90,'stroke':'#f43f5e','fill':'#2a0a14','title_color':'#f43f5e'}],
        'components': [
            {'name':'Resource inventory','detail':'Owner + purpose + data class','x':80,'y':30,'w':260,'h':52,'stroke':'#38bdf8','fill':'#0e294b'},
            {'name':'Cost attribution','detail':'Cost center + environment','x':420,'y':30,'w':260,'h':52,'stroke':'#38bdf8','fill':'#0e294b'},
            {'name':'Review queue','detail':'Review date + named reviewer','x':80,'y':135,'w':260,'h':52,'stroke':'#22c55e','fill':'#0b3824'},
            {'name':'Retirement gate','detail':'Dependencies + backup + approval','x':420,'y':135,'w':260,'h':52,'stroke':'#22c55e','fill':'#0b3824'},
            {'name':'Policy evaluation','detail':'Constraint + scope + evidence','x':80,'y':240,'w':260,'h':52,'stroke':'#818cf8','fill':'#191c4d'},
            {'name':'Exception record','detail':'Scope + expiry + risk owner','x':420,'y':240,'w':260,'h':52,'stroke':'#818cf8','fill':'#191c4d'},
            {'name':'Continuity controls','detail':'Fallback + recovery exercise','x':80,'y':345,'w':260,'h':52,'stroke':'#f59e0b','fill':'#38230a'},
            {'name':'Platform skills','detail':'Primary + trained backup','x':420,'y':345,'w':260,'h':52,'stroke':'#f59e0b','fill':'#38230a'},
            {'name':'Review decision','detail':'Renew, remediate, or retire','x':80,'y':450,'w':260,'h':52,'stroke':'#f43f5e','fill':'#3d101d'},
            {'name':'Closure receipt','detail':'Action + result + timestamp','x':420,'y':450,'w':260,'h':52,'stroke':'#f43f5e','fill':'#3d101d'}],
        'boundaries': [
            {'label':'METADATA SUPPORTS DISCOVERY; IT DOES NOT ENFORCE POLICY','x':60,'y':20,'w':640,'h':195,'color':'#38bdf8'},
            {'label':'POLICY TEST / ENFORCEMENT BOUNDARY','x':60,'y':230,'w':640,'h':195,'color':'#818cf8'},
            {'label':'HUMAN APPROVAL, ADOPTION, AND CLEANUP EVIDENCE','x':60,'y':440,'w':640,'h':195,'color':'#f43f5e'}],
        'flows': [
            {'x1':340,'y1':56,'x2':420,'y2':56,'label':'Attribute spend','type':'ok'},
            {'x1':210,'y1':82,'x2':210,'y2':135,'label':'Set review date','type':'ok'},
            {'x1':340,'y1':161,'x2':420,'y2':161,'label':'Check safe retirement','type':'warn'},
            {'x1':210,'y1':187,'x2':210,'y2':240,'label':'Evaluate request','type':'ok'},
            {'x1':340,'y1':266,'x2':420,'y2':266,'label':'If needed, time-box','type':'warn'},
            {'x1':210,'y1':292,'x2':210,'y2':345,'label':'Prove continuity','type':'ok'},
            {'x1':340,'y1':371,'x2':420,'y2':371,'label':'Train backup owner','type':'ok'},
            {'x1':210,'y1':397,'x2':210,'y2':450,'label':'Review trigger','type':'ok'},
            {'x1':340,'y1':476,'x2':420,'y2':476,'label':'Record closure','type':'ok'}],
        'probes': [
            {'cx':80,'cy':135,'label':'PROBE 1: Every production asset has an accountable owner and next review date','badge':'P1','color':'#22c55e'},
            {'cx':80,'cy':240,'label':'PROBE 2: Exception has bounded scope, sponsor, expiry, and compensating control','badge':'P2','color':'#818cf8'},
            {'cx':80,'cy':450,'label':'PROBE 3: Renewal / retirement decision has evidence and an accountable reviewer','badge':'P3','color':'#f43f5e'}]
    },
    'part3_intro': (
        'These synthetic Brightloaf cases are design-review exercises, not reports of observed production incidents. Separate the '
        'supplied request or inventory row from architectural inference, then choose a control whose result can be checked. Keep the '
        'business invariant explicit: a platform exception must not create an unowned service, an untested recovery path, or an '
        'unreviewed permanent bypass.'
    ),
    'part4_intro': (
        'Complete both local/tabletop exercises with synthetic data. The commands create files only in a disposable local directory; '
        'they do not call Google Cloud, enable APIs, or alter live resources. Preserve the generated decision artifacts as Day 131 '
        'exit evidence and label predictions as predictions.'
    ),
    'topics': [
        {
            'key':'topic-01', 'title':'Resource ownership, tagging, expiry and cleanup',
            'overview':(
                'A lifecycle policy assigns each resource a responsible team and business purpose, captures cost and environment metadata, '
                'sets a review or expiry date, and defines how an authorized owner validates dependencies, retention, and recovery before '
                'retirement. It belongs after service-catalog ownership because catalog records are only useful when operational inventory '
                'and cleanup controls keep them current. In Google Cloud, labels help query and attribute supported resources; labels do not '
                'automatically propagate from a project to its children and cannot themselves impose policy. Resource tags are a separate '
                'mechanism for policy conditions. An expiry date is a review trigger, not sufficient deletion authorization.'),
            'preview':(
                'A production inventory row has no owner and its review date is 45 days overdue, so nobody can confirm whether its disk is still needed for recovery. '
                'The team keeps paying for an unaccountable resource while deletion risk and recovery uncertainty remain unresolved.'),
            'technical':(
                '#### Resource identity and ownership\n'
                'A useful inventory record connects a stable resource identifier to a service, environment, owning team, cost center, data classification, creation time, review date, and lifecycle state. Keep identifiers and owner contacts out of unbounded free-text conventions; define allowed values and who may change them. Project labels are project metadata and do not propagate automatically to child resources, so inventory coverage must be checked at the resource types that matter. Labels support filtering and cost analysis but are not an authorization mechanism.\n\n'
                '#### Lifecycle state machine\n'
                'Use explicit states such as `active`, `review-due`, `quarantined`, `retirement-approved`, and `retired`. A review-due state creates a ticket for the named owner. Quarantine is appropriate only when the service owner has confirmed that a bounded observation window will not break production; it can incur cost and must have a deadline. Before destructive cleanup, enumerate dependencies, retention obligations, snapshots or backups, restore evidence, and downstream consumers. Execute cleanup in reverse dependency order, capture each result, then reconcile the inventory against the actual resource list.\n\n'
                '#### Control ownership, signal, and limits\n'
                'The service owner certifies purpose and recovery needs; the platform team defines required metadata and expiry workflow; finance defines cost-center vocabulary; security/compliance defines retention. The observable signal is a dated inventory exception with an owner and disposition, followed by a deletion or renewal receipt. A complete label report does not prove resource inventory completeness: compare it with the service inventory source and resource APIs. Automated expiry reduces forgotten spend but increases accidental-retirement risk if dependencies or legal holds are missing.\n\n'
                '**Written sources checked 2026-09-29:** [Project label scope and update behavior](https://docs.cloud.google.com/resource-manager/docs/creating-managing-labels) and [labels versus policy tags](https://docs.cloud.google.com/resource-manager/docs/labels-overview#labels_and_tags).'),
            'questions':[
                'Why can a complete project-label report still miss unowned child resources?',
                'What evidence must the service owner provide before an expiry date becomes deletion approval?',
                'When is quarantine safer than deletion, and what deadline prevents quarantine becoming permanent?'],
            'reference':'https://docs.cloud.google.com/resource-manager/docs/creating-managing-labels',
            'reference_label':'Google Cloud Resource Manager: create and update project labels (section checked 2026-09-29)',
            'scenario':{
                'scenario':'Synthetic Brightloaf inventory review: an unattached analytics disk is labeled environment=prod, but its team and recovery purpose are blank; the last owner review was 45 days ago. The evidence does not establish that the disk is safe to delete.',
                'impact':'Continued storage charges and an unresolved risk that an old snapshot or restore procedure depends on the disk; automatic deletion could turn a cost issue into a recovery incident.',
                'constraints':'Keep the order service available, retain approved recovery evidence, assign a cleanup owner, and avoid treating synthetic inventory rows as live cloud observations.',
                'evidence':'Supplied synthetic row: resource=analytics-disk-17; attachment=none; environment=prod; owner=blank; purpose=blank; last_review=45 days overdue; snapshot_dependency=unknown.',
                'root':'The defect is missing ownership and dependency evidence, not proof of an orphan that can be deleted. Inference: the label gives an environment value but no owner or recovery relationship, so neither finance attribution nor safe cleanup can be completed.',
                'diagnostic_steps':['Join the resource ID to the workload catalog and billing owner; record whether a match exists.','Ask the recovery owner to identify backup, retention, and restore dependencies, including a restore test reference.','Set an explicit disposition and next review date; distinguish a verified unused resource from an unresolved inventory gap.'],
                'fix':'Assign a named team and service owner; keep the disk in review-due until recovery dependencies are checked; then quarantine only with a bounded observation window or approve cleanup with a reverse-dependency checklist and recorded receipt.',
                'verify':'The review record contains owner, purpose, cost center, data class, dependency check, approver, decision date, and evidence link. If approved for deletion, the synthetic cleanup receipt names the resource and confirms the dependent workload remains healthy.',
                'residual':'A tabletop checklist cannot establish whether an actual resource exists, whether backups restore, or whether retention rules permit deletion. A real cleanup needs authorized inventory and recovery evidence.',
                'facts':'Synthetic inventory row: analytics-disk-17 has no attachment, no owner, no purpose, and an overdue review; snapshot dependency is unknown.',
                'inference':'The row is unresolved rather than proven safe to delete; stale metadata creates cost and recovery uncertainty.',
                'expected':'After owner and recovery review, the resource is either renewed with a future review date or retired with a recorded dependency check and cleanup receipt.',
                'diagram':('Unowned disk passes expiry date','Review date mistaken for delete authorization','Recovery data or spend is lost / unresolved','Owner checks catalog, hold, backup, and dependency evidence','Renew with owner or retire with receipt')
            },
            'lab':{
                'name':'Lifecycle inventory triage and safe retirement record',
                'goal':'Turn a synthetic inventory into owned lifecycle decisions and a verifiable cleanup queue.',
                'expected':'A CSV inventory, a triage report, and a lifecycle policy containing named owners, due dates, dependency gates, and closure evidence.',
                'mode':'local Python 3 + tabletop review; zero cloud access or spend',
                'prereq':'A shell, Python 3, and Day 130 service-catalog exit artifact or a note that it is unavailable.',
                'preflight':'Use a disposable local folder. Confirm no gcloud commands or cloud credentials are needed; all rows below are synthetic.',
                'file':'day-131-lifecycle-policy.md',
                'steps':[
                    '**Stage 1 — Preflight and confirm scope.** Run these local checks:\n\n```sh\npython3 --version\nmkdir -p ~/day131-lifecycle-lab\ncd ~/day131-lifecycle-lab\n```\nRecord the Day 130 service-catalog artifact path or write `missing; owner lookup remains open`. Expected: a local folder exists and the scope note says `synthetic only; no cloud calls`.',
                    '**Stage 2 — Prepare the inventory input.** Create `inventory.csv` with this exact content:\n\n```sh\ncat > inventory.csv <<\'EOF\'\nresource_id,service,environment,owner,cost_center,review_due_days,dependency_status,monthly_cost_usd\norders-api-prod,orders,prod,commerce-platform,CC-41,30,restore-tested,420\nanalytics-disk-17,analytics,prod,,CC-41,-45,unknown,38\npreview-bucket-3,preview,dev,developer-experience,CC-72,-12,none,9\nEOF\n```\nExpected: three rows; the analytics disk has blank owner, overdue review, and unknown dependencies.',
                    '**Stage 3 — Author lifecycle gates.** Create `lifecycle-policy.md` with this exact starter content and add one sentence mapping each rule to the supplied CSV:\n\n```text\nrequired fields: resource_id, service, environment, owner, cost_center, purpose, data_class, created_on, review_date\nreview due: create owner ticket; do not delete\nquarantine: owner approves, maximum 14 days, monitoring stays on\ndelete: named service owner + recovery/retention check + dependency order + cleanup receipt\nrenew: record reason, funding owner, next review date\n```\nExpected: expiry is explicitly not equal to deletion permission.',
                    '**Stage 4 — Execute inventory triage.** Create `triage.py` with:\n\n```python\nimport csv\nwith open("inventory.csv", newline="") as f:\n    rows = list(csv.DictReader(f))\nfor r in rows:\n    flags = []\n    if not r["owner"]: flags.append("MISSING_OWNER")\n    if int(r["review_due_days"]) < 0: flags.append("REVIEW_OVERDUE")\n    if r["dependency_status"] == "unknown": flags.append("DEPENDENCY_UNVERIFIED")\n    print(r["resource_id"] + ": " + (",".join(flags) or "REVIEW_CURRENT"))\n```\nExecute and capture the triage result:\n\n```sh\npython3 triage.py\n```\nExpected exact lines: `orders-api-prod: REVIEW_CURRENT`; `analytics-disk-17: MISSING_OWNER,REVIEW_OVERDUE,DEPENDENCY_UNVERIFIED`; `preview-bucket-3: REVIEW_OVERDUE`.',
                    '**Stage 5 — Verify decisions against evidence.** Create `decisions.csv` with this exact content:\n\n```csv\nresource_id,owner,decision,evidence,next_review\norders-api-prod,commerce-platform,renew,restore-tested and service owner confirmed,2026-10-29\nanalytics-disk-17,UNASSIGNED,hold for owner and recovery lookup,no deletion approval while dependency unknown,2026-10-06\npreview-bucket-3,developer-experience,retire after owner confirms no consumers,dependency_status=none; approval still required,2026-10-06\n```\nRead the file and check every row has a future review date. Expected: the overdue disk remains held, not deleted.',
                    '**Stage 6 — Rehearse an edge case.** Copy the inventory to `inventory-edge.csv` and change `orders-api-prod` dependency status to `unknown`. Rerun the triage logic against that copy. Record the resulting flag and change the decision from `renew` to `hold for recovery review`. Expected: unknown dependency blocks retirement even when owner metadata is complete.',
                    '**Stage 7 — Diagnose and record remediation.** Create `review-notes.md` with three entries: `Observed in synthetic input: analytics-disk-17 has missing owner, overdue review, unknown dependency`; `Inference: safe deletion is not established`; `Remediation: catalog lookup by resource ID, recovery-owner check, then renew or approve retirement`. Add a reviewer name/role, review date, and a cleanup receipt template (`resource_id | approver | dependency check | action | result | timestamp`). Expected: fact, inference, and next action are separate.',
                    '**Stage 8 — Close out and reconcile.** Run the checks below and save their output in `run-log.txt`:\n\n```sh\npython3 -m py_compile triage.py\npython3 triage.py\nls -l inventory.csv lifecycle-policy.md triage.py decisions.csv review-notes.md\n```\nAdd the final named lifecycle policy and owner for each unresolved item. After retaining the original inventory and evidence, remove only the disposable edge-case copy:\n\n```sh\nrm -f inventory-edge.csv\n```\nExpected: no cloud resource was created and every unresolved row has a named next action.'
                ],
                'verification':'Expected triage flags match the three exact lines in Stage 4; analytics-disk-17 is held because no owner or dependency evidence exists; edge case changes the orders disk decision to hold.',
                'accept':'Submit `day-131-lifecycle-policy.md` with inventory, triage output, decision table, fact/inference notes, owner and review dates for all open items, a cleanup receipt template, and a short policy adoption owner. Keep all data synthetic.',
                'trouble':'If Python is unavailable, execute the same three flag checks manually and record the exact matching fields. If a supplied prerequisite is missing, record the catalog lookup as an open action; do not invent an owner or claim a restore test.',
                'cleanup':'Local-only exercise. Preserve the final policy and run log as exit evidence; delete the disposable directory only after copying those artifacts. No billing or cloud cleanup applies.'
            }
        },
        {
            'key':'topic-02', 'title':'Policy guardrails, business continuity and team skills',
            'overview':(
                'A guardrail limits unsafe configurations at an organizational boundary; an exception documents why one workload cannot '
                'yet comply, what compensating controls bound the risk, who funds and operates it, and when the decision expires. This '
                'belongs after lifecycle ownership because a policy without an accountable service team becomes an unexplained denial, '
                'while a permanent exception becomes an unreviewed bypass. Business continuity requires a named fallback and a tested '
                'recovery path; adoption requires the primary and backup operators to demonstrate the skills needed to run the approved '
                'runtime. A staged rollout uses representative requests and review evidence before enforcement.'),
            'preview':(
                'A team requests a nonstandard runtime with no trained backup and no tested fallback before the proposed guardrail deadline. '
                'Approving an indefinite exception leaves the service unsupported during an incident and shifts unplanned cost and risk to the platform team.'),
            'technical':(
                '#### Guardrail path and failure signals\n'
                'A request passes through the inherited organization or folder policy, then the target project/service configuration, then runtime admission or deployment. The API error can identify a violated constraint; trace the constraint and hierarchy before editing a workload or asking for an exception. Resource labels help discovery but are not conditional policy controls. Tags can carry policy conditions. Organization Policy dry-run mode records what a supported policy would deny without blocking that operation, but only supported constraint types are eligible and billing is required for the project. A dry-run observation proves only that the observed request path was exercised.\n\n'
                '#### Exception record and adoption boundary\n'
                'An exception should include the request and business reason, exact service/project scope, sponsor and budget, named service and platform owners, threat and blast-radius statement, compensating controls, continuity fallback, training plan for primary and backup operators, start and expiry dates, reviewer, and measurable review triggers. Review triggers include an incident, a policy or runtime update, a failed recovery exercise, missing training evidence, budget threshold breach, or approaching expiry. Renewal is a new risk decision with fresh evidence, not an automatic extension.\n\n'
                '#### Staged rollout, continuity, and trade-off\n'
                'Collect representative deployment attempts; evaluate or simulate the policy; run dry-run where the constraint supports it; classify observed conflicts; remediate compliant workloads; pilot enforcement in a low-blast-radius scope; verify denials and rollback; then expand by ring. The platform owner owns guardrail design and audit evidence; the service owner owns workload compatibility and recovery; the sponsor funds work; training owner closes skills gaps. Strict enforcement can prevent risky configurations but can also block urgent delivery when rollout evidence is poor. Exceptions preserve service delivery but enlarge the supported surface and require expiry enforcement.\n\n'
                '**Written sources checked 2026-09-29:** [Organization Policy dry-run behavior and limits](https://docs.cloud.google.com/organization-policy/test-policies#limitations), [policy violation troubleshooting](https://docs.cloud.google.com/organization-policy/troubleshoot-policies), and [operational excellence and continual team learning](https://docs.cloud.google.com/architecture/framework/operational-excellence/continuously-improve-and-innovate).'),
            'questions':[
                'Which exact evidence would change a temporary exception into a renewal decision?',
                'Why does an empty dry-run log not prove that a policy is safe to enforce?',
                'How do a trained backup operator and a recovery exercise reduce different continuity risks?'],
            'reference':'https://docs.cloud.google.com/organization-policy/test-policies#limitations',
            'reference_label':'Google Cloud Organization Policy: dry-run limitations (checked 2026-09-29)',
            'scenario':{
                'scenario':'Synthetic Brightloaf platform review: the order-pricing service requests a nonstandard runtime for a required native library. Its sponsor can fund a six-week migration window, but the supplied request names no trained backup operator and includes no recovery exercise result.',
                'impact':'Immediate denial could delay a committed release; an unbounded approval leaves incident response dependent on one specialist and can turn a routine failure into prolonged order-pricing unavailability.',
                'constraints':'Preserve one price decision per order, keep customer data protected, maintain a recoverable supported service, and limit exception scope and duration to the funded migration window.',
                'evidence':'Supplied synthetic request: runtime=nonstandard; business reason=native library; sponsor=Commerce; funding window=6 weeks; backup operator=not named; recovery exercise=not supplied; expiry=not supplied.',
                'root':'The decision is blocked by missing continuity and adoption evidence, not by proof that the runtime is technically unsafe. Inference: without a backup and recovery result, the service has a single-person operational dependency.',
                'diagnostic_steps':['Identify the policy constraint, its inherited scope, and the deployment request that would violate it; use policy simulation or dry-run only if that constraint and environment support it.','Ask the service owner for a fallback path and recovery objective, then request a dated exercise result that preserves one price decision per order.','Ask the sponsor to name funding and an expiry date; assign primary and backup operators with a skills demonstration date.'],
                'fix':'Grant only a six-week, service-scoped exception after naming the sponsor, primary and trained backup, compensating controls, funding, fallback, expiry, and a successful recovery exercise. If any gate is unmet, keep the request in a time-bounded remediation state and offer the supported runtime path.',
                'verify':'The exception record names its policy and resource scope, approver, risk owner, controls, budget, expiry, renewal trigger, and evidence links. A tabletop recovery walk-through covers a primary-operator absence and confirms one price decision per order; a real approval requires local policy-owner review.',
                'residual':'A tabletop exercise cannot prove runtime compatibility, policy coverage, or recovery timing. A dry-run log does not block actions and only reflects requests that actually occurred.',
                'facts':'Synthetic request states nonstandard runtime and native-library need, six-week sponsor funding, no named backup, no recovery evidence, and no expiry.',
                'inference':'Until ownership, recovery, and expiry gates are met, the exception is not supportable as an operating service.',
                'expected':'Decision is conditional and time-bounded: supported runtime now, or scoped exception after all continuity and adoption gates pass; review before expiry and on incident or failed exercise.',
                'diagram':('Nonstandard runtime request arrives','Exception lacks expiry and backup owner','Policy bypass outlives funding; recovery depends on one person','Bound scope, fund, train backup, and rehearse fallback','Reviewer renews with evidence or closes by expiry')
            },
            'lab':{
                'name':'Runtime exception decision and staged guardrail adoption review',
                'goal':'Make a defensible decision on a nonstandard-runtime request and define evidence-based rollout, continuity, funding, expiry, and training gates.',
                'expected':'A completed exception decision with named roles, a staged rollout plan, and a review-trigger register.',
                'mode':'local tabletop worksheet; zero cloud policy changes',
                'prereq':'A shell or editor and the Day 130 ownership artifact; use synthetic inputs if unavailable.',
                'preflight':'Do not run gcloud or change organization policy. The supplied request is synthetic; no actual company policy or exception approval is implied.',
                'file':'day-131-runtime-exception-decision.md',
                'steps':[
                    '**Stage 1 — Preflight and define decision boundary.** Create and enter a local folder:\n\n```sh\nmkdir -p ~/day131-exception-lab\ncd ~/day131-exception-lab\n```\nCreate `scope.md` containing `Synthetic Brightloaf request; decision exercise only; no live policy or deployment`. Write the service, policy owner, business sponsor, and reviewer roles from the Day 130 artifact; if missing, mark each `unconfirmed`. Expected: no role is silently invented.',
                    '**Stage 2 — Prepare the exact request record.** Create `request.csv` with:\n\n```sh\ncat > request.csv <<\'EOF\'\nservice,runtime,business_reason,sponsor,funding_window_weeks,primary_operator,backup_operator,recovery_evidence,requested_expiry\norder-pricing,nonstandard,native library required,Commerce,6,Alex,UNNAMED,NOT_SUPPLIED,NOT_SUPPLIED\nEOF\n```\nExpected: request is service-scoped and visibly incomplete on backup, recovery, and expiry.',
                    '**Stage 3 — Author the policy and exception plan.** Create `decision.md` with sections `Constraint and scope`, `Business reason`, `Supported alternative`, `Sponsor and budget`, `Blast radius`, `Compensating controls`, `Continuity fallback`, `Primary and backup skills`, `Expiry`, `Review triggers`, `Approver`. Copy the exact request row values; write `TBD—approval blocked` for facts not supplied. Choose candidate expiry `2026-11-10` (six weeks from the exercise date 2026-09-29) and state it is a proposed tabletop date. Expected: missing required evidence is explicit.',
                    '**Stage 4 — Execute the decision gate.** Create `gate-checklist.csv` with this exact content:\n\n```csv\ngate,status,evidence_or_action\nbusiness reason,PASS,native library named\nscope,PASS,order-pricing only\nfunding,PASS,Commerce funds 6-week window\nbackup operator,FAIL,name and skills demonstration required\nrecovery exercise,FAIL,record fallback and one-price-per-order result\nexpiry,FAIL,approver must accept proposed date\npolicy owner,FAIL,confirm constraint and scope\n```\nCount the failed rows:\n\n```sh\ngrep -c FAIL gate-checklist.csv\n```\nExpected: `4`.',
                    '**Stage 5 — Verify outcome and continuity invariant.** In `decision.md`, enter `Decision: CONDITIONAL HOLD; no exception approval until four failed gates close.` Add an acceptance check: during the synthetic fallback walkthrough, replaying order `BL-1042` returns the same price decision and produces exactly one pricing record. Record which participant supplies the observation and mark it `tabletop prediction`. Expected: the business invariant is measurable and not presented as observed production behavior.',
                    '**Stage 6 — Rehearse a bounded failure.** Add an edge-case section: `Primary operator unavailable on day 10; policy owner cannot be reached; the runtime fails during order pricing.` Using only the supplied inputs, write the first safe action, fallback owner, customer impact signal, abort/escalation point, and decision if no trained backup exists. Expected: no irreversible policy relaxation; hold new exception traffic on supported fallback and escalate to sponsor/platform incident owner.',
                    '**Stage 7 — Diagnose evidence and set adoption actions.** Create `actions.csv` with this exact content:\n\n```csv\naction,owner,due,proof,review_trigger\nname backup operator,Commerce service owner,2026-10-02,accepted rota entry,operator unavailable\nrecovery walkthrough,Service owner + SRE,2026-10-06,one price decision for BL-1042,failed exercise\npolicy scope review,Platform policy owner,2026-10-02,constraint and inheritance note,policy update\nruntime training,Platform enablement,2026-10-09,primary and backup skill check,training missed\nfunding and expiry,Commerce sponsor,2026-10-03,budget code and signed expiry,forecast breach\n```\nCheck every row has an owner and due date. Expected: adoption and funding are owned actions, not generic aspirations.',
                    '**Stage 8 — Close the review and prepare staged rollout.** Add rings to `decision.md`: `Ring 0: collect representative requests and run supported simulation/dry-run; Ring 1: pilot in isolated low-blast-radius scope with rollback; Ring 2: expand only after denial, continuity, and training evidence review`. Add close condition `renew with fresh evidence or close no later than proposed expiry`. Verify the artifact set:\n\n```sh\nls -l scope.md request.csv decision.md gate-checklist.csv actions.csv\n```\nRetain these files and write the final exception decision. Expected: rollout and expiry have a reviewer and evidence gate; no cloud state changed.'
                ],
                'verification':'The four failed gates remain explicit until evidence is added; decision is conditional hold. Staged rollout begins with representative requests and only uses dry-run if the real constraint supports it; each ring has a reviewer and rollback condition.',
                'accept':'Submit `day-131-runtime-exception-decision.md` with the exact request, gate count and evidence, conditional decision, business continuity invariant, exception owner/sponsor/funding/expiry, primary and backup training actions, staged rollout rings, renewal criteria, and review triggers.',
                'trouble':'If the policy constraint is unknown, request the platform policy owner to identify its name and inherited scope; do not claim a dry-run feature applies to every constraint. If role identities are unavailable, keep them marked unconfirmed and leave approval blocked.',
                'cleanup':'Local tabletop only. Preserve the decision and actions as exit evidence, then delete temporary CSV copies if desired. No cloud policy, API, or resource was changed.'
            }
        }
    ]
}
