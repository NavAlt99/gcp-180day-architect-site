"""day_data_087.py — Exhaustive architecture data specification for Day 87.

Covers Incidents, Blameless Post-Mortems, and Capacity Planning:
1. Incident management (severity levels P1-P4, Incident Commander ICS roles, escalation paths).
2. Blameless post-mortems (Five Whys, timeline reconstruction, systemic guardrails, SMART action items).
3. Capacity planning and load forecasting (N+1 regional redundancy, Google Cloud quota headroom, seasonal peak modeling).
Follows PAGE_AUTHORING_CONTRACT.md with deep technical mechanics, trade-off matrices,
dual-lane failure investigations, and runnable 8-stage operational engineering exercises.
"""

DAY_NUM = 87

DATA = {'day': 87,
 'part1_intro': 'Day 87 masters the operational human and organizational protocols that preserve cloud resilience: '
                'structured incident management, blameless post-mortems, and predictive capacity planning. Technology '
                'fails inevitably; the differentiator of high-performing engineering organizations is the speed, '
                'coordination, and psychological safety with which teams respond to outages and extract systemic '
                'learnings. Following the battle-tested Incident Command System (ICS), architects learn to separate '
                'command leadership from technical execution, triage severity levels from P1 to P4, and shield '
                "responders from executive interruption. Furthermore, today's curriculum establishes blameless "
                'post-mortem culture—treating human error not as a root cause, but as a symptom of inadequate systemic '
                'guardrails—and formulates rigorous capacity planning models that manage Google Cloud quota ceilings '
                'and N+1 redundancy.',
 'exit_summary': 'Constructed an enterprise Incident Response Playbook defining ICS roles (Incident Commander, '
                 'Operations Lead, Communications Lead) and severity escalation matrices; completed a comprehensive '
                 'blameless post-mortem analysis with second-by-second timeline reconstruction and Five Whys causal '
                 'analysis for a simulated regional database failover incident; authored five SMART preventive action '
                 'items; implemented an automated Python capacity planning calculator modeling seasonal load surges '
                 'and GCP quota headroom.',
 'part2_intro': 'Operational resilience transforms chaotic firefighting into a disciplined, repeatable engineering '
                'workflow. The sections below detail ICS role boundaries, severity triage thresholds, post-mortem '
                'authoring rubrics, and capacity forecasting mathematics.',
 'arch_table_html': '<div class="table-container">\n'
                    '<table>\n'
                    '  <thead>\n'
                    '    <tr>\n'
                    '      <th>Severity Tier</th>\n'
                    '      <th>Business &amp; User Impact Criteria</th>\n'
                    '      <th>Response Target (MTTA)</th>\n'
                    '      <th>Command Cadence &amp; Escalation</th>\n'
                    '      <th>External Communication Policy</th>\n'
                    '    </tr>\n'
                    '  </thead>\n'
                    '  <tbody>\n'
                    '    <tr>\n'
                    '      <td><strong>P1 — Critical</strong></td>\n'
                    '      <td>Core revenue path down (e.g. 100% checkout failure); data loss risk; active security '
                    'breach.</td>\n'
                    '      <td><strong>&lt; 5 minutes</strong> (Immediate 24/7 page)</td>\n'
                    '      <td>Incident Commander dedicated; war room established; VP Eng notified immediately.</td>\n'
                    '      <td>Public status page updated every 15 minutes; executive briefings every 30 '
                    'minutes.</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>P2 — Major</strong></td>\n'
                    '      <td>Significant service degradation (>10% users affected); core feature impaired without '
                    'workaround.</td>\n'
                    '      <td><strong>&lt; 15 minutes</strong> (Primary + Secondary page)</td>\n'
                    '      <td>Operations Lead directs triage; technical bridge formed; on-call manager engaged.</td>\n'
                    '      <td>Status page updated every 30 minutes; internal stakeholder email sent hourly.</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>P3 — Moderate</strong></td>\n'
                    '      <td>Non-critical feature down (e.g. search recommendations); workaround exists; minimal '
                    'user disruption.</td>\n'
                    '      <td><strong>&lt; 1 hour</strong> (Business hours / on-call ticket)</td>\n'
                    '      <td>On-call engineer investigates during working shift; escalates if blast radius '
                    'grows.</td>\n'
                    '      <td>No public status update; daily operational summary report.</td>\n'
                    '    </tr>\n'
                    '    <tr>\n'
                    '      <td><strong>P4 — Minor</strong></td>\n'
                    '      <td>Cosmetic UI bug; internal reporting delay; non-impacting telemetry failure.</td>\n'
                    '      <td><strong>&lt; 24 hours</strong> (Next business day)</td>\n'
                    '      <td>Standard engineering backlog grooming; regular sprint ticket triage.</td>\n'
                    '      <td>Internal release notes only.</td>\n'
                    '    </tr>\n'
                    '  </tbody>\n'
                    '</table>\n'
                    '</div>',
 'arch_diagram': {'type': 'topology',
                  'title': 'Day 87: Incident Command Lifecycle and Capacity Planning Governance Topology',
                  'desc': 'Multi-tier infrastructure topology illustrating incident detection, ICS role separation air '
                          'gaps, rapid mitigation routing, blameless post-mortem tracking, and capacity quota '
                          'forecasting.',
                  'caption': 'Figure 87.1: Multi-tier architectural topology illustrating request flows through edge '
                             'Anycast, decoupled compute tiers, HA persistence, and shared control plane boundaries.',
                  'width': 1100,
                  'height': 640,
                  'layers': [{'name': 'LAYER 1: Detection & Multi-Burn Telemetry Tier',
                              'desc': 'Cloud Monitoring Multi-Burn Rate Alarms and PagerDuty 24/7 Automated On-Call '
                                      'Escalation',
                              'fill': '#1e3a5f',
                              'y': 10,
                              'h': 90},
                             {'name': 'LAYER 2: Incident Command System (ICS) Air-Gapped Roles',
                              'desc': 'Incident Commander, Operations Lead, and Communications Lead with Strict '
                                      'Air-Gap Protection',
                              'fill': '#0f2338',
                              'y': 115,
                              'h': 90},
                             {'name': 'LAYER 3: Rapid Mitigation & Traffic Routing Layer',
                              'desc': 'Anycast GCLB Regional Traffic Drain, Runtime Feature Flag Disabling, and Canary '
                                      'Rollback',
                              'fill': '#064e3b',
                              'y': 220,
                              'h': 90},
                             {'name': 'LAYER 4: Forensics, Telemetry & Post-Mortem Analytics',
                              'desc': 'Cloud Logging Aggregated Sinks, Second-by-Second Timeline Reconstruction, and '
                                      'Five Whys Causal Audit',
                              'fill': '#1e1b4b',
                              'y': 325,
                              'h': 90},
                             {'name': 'LAYER 5: Preventative Engineering & Capacity Governance',
                              'desc': 'Google Cloud Quota Headroom Evaluator, N+1 Multi-Zone Redundancy Model, and '
                                      'SMART Action Tracking',
                              'fill': '#3b0764',
                              'y': 430,
                              'h': 90}],
                  'components': [{'id': 'mon_detect',
                                  'name': 'Cloud Monitoring Alarm',
                                  'detail': 'P1 Fast Burn (14.4x) Trigger',
                                  'x': 80,
                                  'y': 30,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#0f283d',
                                  'stroke': '#38bdf8'},
                                 {'id': 'pager_router',
                                  'name': 'PagerDuty Webhook',
                                  'detail': 'On-Call Page (<5m MTTA)',
                                  'x': 420,
                                  'y': 30,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#0f283d',
                                  'stroke': '#38bdf8'},
                                 {'id': 'ic_lead',
                                  'name': 'Incident Commander (IC)',
                                  'detail': 'Sole Decision Authority',
                                  'x': 80,
                                  'y': 135,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#092e28',
                                  'stroke': '#10b981'},
                                 {'id': 'comms_lead',
                                  'name': 'Communications Lead',
                                  'detail': 'Executive Stakeholder Shield',
                                  'x': 420,
                                  'y': 135,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#092e28',
                                  'stroke': '#10b981'},
                                 {'id': 'traffic_drain',
                                  'name': 'Anycast Traffic Drain',
                                  'detail': 'Instant Regional Failover',
                                  'x': 80,
                                  'y': 240,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#093322',
                                  'stroke': '#22c55e'},
                                 {'id': 'flag_cutoff',
                                  'name': 'Feature Flag Cutoff',
                                  'detail': 'Disable Degraded Auxiliary APIs',
                                  'x': 420,
                                  'y': 240,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#093322',
                                  'stroke': '#22c55e'},
                                 {'id': 'postmortem_hub',
                                  'name': 'Blameless Post-Mortem',
                                  'detail': 'Five Whys & Timeline Audit',
                                  'x': 80,
                                  'y': 345,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#1b143a',
                                  'stroke': '#a855f7'},
                                 {'id': 'smart_actions',
                                  'name': 'SMART Action Tracker',
                                  'detail': 'Immutable Prevention Items',
                                  'x': 420,
                                  'y': 345,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#1b143a',
                                  'stroke': '#a855f7'},
                                 {'id': 'quota_forecaster',
                                  'name': 'Capacity Forecaster',
                                  'detail': 'N+1 Regional Headroom Engine',
                                  'x': 80,
                                  'y': 450,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#280a3c',
                                  'stroke': '#c084fc'},
                                 {'id': 'gcp_quota_api',
                                  'name': 'GCP Service Quotas API',
                                  'detail': 'Automated Headroom Alerting',
                                  'x': 420,
                                  'y': 450,
                                  'w': 260,
                                  'h': 52,
                                  'fill': '#280a3c',
                                  'stroke': '#c084fc'}],
                  'boundaries': [{'x': 60,
                                  'y': 14,
                                  'w': 640,
                                  'h': 80,
                                  'label': 'DETECTION & ESCALATION AIR-GAP PERIMETER',
                                  'color': '#38bdf8'},
                                 {'x': 60,
                                  'y': 120,
                                  'w': 640,
                                  'h': 80,
                                  'label': 'INCIDENT COMMAND & TECHNICAL TRIAGE PERIMETER',
                                  'color': '#10b981'},
                                 {'x': 60,
                                  'y': 330,
                                  'w': 640,
                                  'h': 80,
                                  'label': 'BLAMELESS POST-MORTEM & PREVENTATIVE CAPACITY BOUNDARY',
                                  'color': '#a855f7'}],
                  'flows': [{'x1': 340, 'y1': 56, 'x2': 420, 'y2': 56, 'type': 'ok', 'label': 'Alert Trigger (P1)'},
                            {'x1': 210, 'y1': 82, 'x2': 210, 'y2': 135, 'type': 'ok', 'label': 'Mobilize IC Command'},
                            {'x1': 340, 'y1': 161, 'x2': 420, 'y2': 161, 'type': 'ok', 'label': 'Shield from Execs'},
                            {'x1': 210,
                             'y1': 187,
                             'x2': 210,
                             'y2': 240,
                             'type': 'ok',
                             'label': 'Mitigate: Shift Traffic'},
                            {'x1': 340,
                             'y1': 266,
                             'x2': 420,
                             'y2': 266,
                             'type': 'ok',
                             'label': 'Isolate Faulty Service'},
                            {'x1': 210, 'y1': 292, 'x2': 210, 'y2': 345, 'type': 'ok', 'label': 'Post-Mortem Timeline'},
                            {'x1': 340, 'y1': 371, 'x2': 420, 'y2': 371, 'type': 'ok', 'label': 'Assign SMART Fixes'},
                            {'x1': 210, 'y1': 397, 'x2': 210, 'y2': 450, 'type': 'ok', 'label': 'Model Capacity Gaps'},
                            {'x1': 340,
                             'y1': 476,
                             'x2': 420,
                             'y2': 476,
                             'type': 'warn',
                             'label': 'Request Quota Increase'}],
                  'probes': [{'cx': 420, 'cy': 56, 'label': 'PROBE 1: MTTA Response Latency (<5m)', 'color': '#38bdf8'},
                             {'cx': 420,
                              'cy': 161,
                              'label': 'PROBE 2: Air-Gap Enforcement (Zero Exec Distraction)',
                              'color': '#22c55e'},
                             {'cx': 420,
                              'cy': 476,
                              'label': 'PROBE 3: Quota Buffer Margin (>25% headroom)',
                              'color': '#f59e0b'}]},
 'topics': [{'key': 'topic-01',
             'title': 'Incident management: severity levels, on-call, and incident command',
             'preview': 'During a major payment outage, twenty senior executives join the Slack triage channel '
                        'demanding instant updates, distracting the lead database engineer so severely that she '
                        'accidentally enters a command that deletes the primary database table.',
             'overview': 'Modern incident response is modeled after the industrial Incident Command System (ICS), '
                         'designed to coordinate high-stress, time-critical emergencies without organizational chaos. '
                         'The golden rule of incident response is the strict separation of roles: the **Incident '
                         'Commander (IC)** owns overall decision authority, assigns investigation streams, and '
                         'maintains situational awareness, but *never* touches a terminal or debugs code directly. The '
                         '**Operations Lead** directs technical troubleshooting and executes runbooks. The '
                         '**Communications Lead** handles all stakeholder and customer communication, actively '
                         'shielding the technical team from executive distraction. Clearly codified severity tiers (P1 '
                         'to P4) dictate response timeframes, alerting channels, and escalation paths, ensuring that '
                         'high-impact outages receive immediate, structured focus without panic.',
             'technical': 'Incident operations must strictly adhere to documented organizational protocols:\n'
                          '\n'
                          '### 1. Incident Command System (ICS) Core Roles\n'
                          '- **Incident Commander (IC):** Holds absolute operational authority during the incident. '
                          'Assesses severity, appoints leads, approves high-risk mitigations (such as regional traffic '
                          'drains or database restarts), and maintains a calm, disciplined cadence.\n'
                          '- **Operations Lead (Ops Lead):** Directs the technical responders. Formulates diagnostic '
                          'hypotheses, reviews telemetry, and assigns specific investigation tasks to domain experts '
                          '(networking, database, compute).\n'
                          '- **Communications Lead (Comms Lead):** The sole liaison to executive leadership, customer '
                          'support, and public status pages. Updates the public status page at fixed intervals (e.g. '
                          'every 15 minutes for P1) and prevents external stakeholders from entering the technical war '
                          'room.\n'
                          '\n'
                          '### 2. The Mitigation-First Imperative\n'
                          'In enterprise SRE, **mitigation always precedes root cause analysis**. The sole objective '
                          'during an active incident is restoring user-facing availability as rapidly as possible '
                          '(e.g., rolling back a release, draining traffic to a secondary region, toggling a feature '
                          'flag, or restarting an autoscaling group). Diagnosing *why* the bug occurred must be '
                          'deferred until after user service is restored.\n'
                          '\n'
                          '### 3. Formal Shift Handoff Protocol\n'
                          'For incidents spanning multiple hours, responders suffer cognitive fatigue. Handoffs must '
                          'be conducted synchronously using a formal written summary: current operational state, '
                          'proven facts, ruled-out hypotheses, active mitigation streams, and explicit verbal transfer '
                          'of IC authority.',
             'questions': ['Why must the Incident Commander refrain from typing debugging commands or inspecting logs '
                           'directly during a P1 incident?',
                           'What is the specific role of the Communications Lead in protecting technical responders '
                           'from executive interference?',
                           'Why must teams prioritize rapid mitigation (e.g., traffic drain or rollback) over finding '
                           'the underlying code defect?'],
             'reference': 'https://docs.cloud.google.com/architecture/framework/operational-excellence#manage-incidents',
             'reference_label': 'Google Cloud Architecture Framework: Managing and escalating enterprise incidents',
             'scenario': {'symptom': 'Brightloaf suffered a 75-minute outage of its checkout API. Early in the outage, '
                                     'the VP of Sales and Director of Support joined the engineering incident bridge, '
                                     'repeatedly interrogating the database engineer about customer impact. '
                                     'Disoriented by the pressure, the engineer applied a hotfix directly to '
                                     'production without testing, which doubled the volume of 500 errors.',
                          'constraints': 'Must establish strict communication air gaps between executives and '
                                         'technical responders while maintaining 15-minute stakeholder updates.',
                          'evidence': 'Incident voice bridge recording showed 42 minutes of discussion between '
                                      'executives and engineers debating revenue impact, leaving the on-call engineer '
                                      'only 18 minutes to investigate database connection pool deadlocks.',
                          'diagnostic_steps': ['Review incident bridge timeline and message logs to measure time spent '
                                               'answering non-technical executive questions.',
                                               'Analyze the failed hotfix commit pushed during the incident to '
                                               'identify why standard review controls were bypassed.',
                                               'Audit the absence of a designated Communications Lead in the '
                                               'historical incident logs.'],
                          'root': 'Failure to implement Incident Command System (ICS) role separation: the absence of '
                                  'an Incident Commander and Communications Lead allowed external stakeholders to '
                                  'directly distract and pressure technical responders, causing an error that worsened '
                                  'the outage.',
                          'fix': 'Mandate ICS role assignment on all P1/P2 incidents: appoint a dedicated '
                                 'Communications Lead who hosts an executive broadcast channel, and enforce a strict '
                                 'policy locking technical debugging bridges to authorized engineering responders '
                                 'only.',
                          'verify': 'Execute a tabletop incident simulation with executive observers; verify '
                                    'responders operate without interruption and public status updates occur every 15 '
                                    'minutes.',
                          'residual': 'Executives may initially feel excluded; requires leadership alignment meetings '
                                      'to explain that air-gapping responders accelerates MTTR.',
                          'diagram': ('Execs enter eng channel',
                                      'Database lead distracted',
                                      'Unverified hotfix fails',
                                      'Appoint Comms Lead air gap',
                                      'MTTR reduced by 60%'),
                          'facts': '42 minutes of technical troubleshooting were lost to answering executive status '
                                   'inquiries on the primary bridge.',
                          'inference': 'Responders cannot conduct complex distributed systems triage while '
                                       'simultaneously managing executive anxiety.',
                          'expected': 'Communications Lead handles external messaging, allowing Operations Lead to '
                                      'execute technical recovery unhindered.'},
             'lab': {'name': 'Incident Command Playbook and Severity Triage Matrix',
                     'file': 'day-087-topic-01-ics-playbook.md',
                     'goal': 'Author an enterprise Incident Response Playbook specifying ICS roles, paging triggers, '
                             'and communication cadences.',
                     'expected': 'A structured Markdown playbook covering P1-P4 triage rules, war room protocols, and '
                                 'executive communication templates.',
                     'mode': 'tabletop analysis & architecture synthesis',
                     'prereq': 'Review Day 86 golden signals and error budget artifacts.',
                     'preflight': 'Initialize incident playbook template in workspace.',
                     'steps': ['#### Stage 1: Pre-Flight Incident Command Taxonomy & Invariants\n'
                               'Establish the core governance invariants for enterprise incident response:\n'
                               '- **Incident Commander (IC):** Absolute decision authority; strictly air-gapped from '
                               'hands-on terminal typing.\n'
                               '- **Operations Lead (Ops):** Formulates hypotheses, directs triage, and executes '
                               'runbooks.\n'
                               '- **Communications Lead (Comms):** Manages status pages and executive briefings; '
                               'prevents stakeholder interference.\n'
                               '- **Mitigation-First Imperative:** Availability restoration strictly precedes root '
                               'cause diagnosis.',
                               '#### Stage 2: Environment Preflight & Role Verification Harness\n'
                               'Author a validation script (<kbd>test_ics_roles.py</kbd>) verifying that operational '
                               'roles are uniquely assigned:\n'
                               '\n'
                               '```python\n'
                               '# test_ics_roles.py\n'
                               "incident_roles = {'IC': 'Sarah Chen', 'OpsLead': 'Marcus Vance', 'CommsLead': 'Elena "
                               "Rostova'}\n"
                               'unique_personnel = set(incident_roles.values())\n'
                               "assert len(unique_personnel) == 3, 'ICS roles must be assigned to distinct "
                               "individuals'\n"
                               "assert 'IC' in incident_roles and 'OpsLead' in incident_roles\n"
                               "print('[PASS] ICS role separation verified without dual-assignment conflicts.')\n"
                               '```\n'
                               '\n'
                               'Execute preflight validation:\n'
                               '\n'
                               '```sh\n'
                               'python3 test_ics_roles.py\n'
                               '```',
                               '#### Stage 3: Core Implementation: Incident Severity Triage Engine\n'
                               'Author the automated severity triage and escalation engine '
                               '(<kbd>incident_triage_engine.py</kbd>):\n'
                               '\n'
                               '```python\n'
                               '#!/usr/bin/env python3\n'
                               '"""incident_triage_engine.py — Evaluates outage symptoms and assigns severity tiers '
                               'P1-P4."""\n'
                               'from typing import Dict\n'
                               '\n'
                               'def triage_incident(revenue_path_down: bool, affected_users_pct: float, '
                               'data_loss_risk: bool) -> Dict:\n'
                               '    if revenue_path_down or data_loss_risk or affected_users_pct >= 25.0:\n'
                               "        return {'severity': 'P1', 'mtta_target_mins': 5, 'page_cadence': "
                               "'IMMEDIATE_24x7', 'comms_cadence_mins': 15}\n"
                               '    elif affected_users_pct >= 5.0:\n'
                               "        return {'severity': 'P2', 'mtta_target_mins': 15, 'page_cadence': "
                               "'PRIMARY_SECONDARY', 'comms_cadence_mins': 30}\n"
                               '    elif affected_users_pct >= 1.0:\n'
                               "        return {'severity': 'P3', 'mtta_target_mins': 60, 'page_cadence': "
                               "'BUSINESS_HOURS', 'comms_cadence_mins': 60}\n"
                               "    return {'severity': 'P4', 'mtta_target_mins': 1440, 'page_cadence': "
                               "'SPRINT_BACKLOG', 'comms_cadence_mins': 0}\n"
                               '\n'
                               "if __name__ == '__main__':\n"
                               '    res = triage_incident(revenue_path_down=True, affected_users_pct=80.0, '
                               'data_loss_risk=False)\n'
                               '    print(f"Triage Result: Severity {res[\'severity\']} | MTTA: '
                               '{res[\'mtta_target_mins\']}m | Comms: Every {res[\'comms_cadence_mins\']}m")\n'
                               "    assert res['severity'] == 'P1' and res['mtta_target_mins'] == 5\n"
                               "    print('[PASS] Triage engine correctly categorized critical checkout failure as "
                               "P1.')\n"
                               '```',
                               '#### Stage 4: Execution & Incident Escalation Simulation\n'
                               'Execute the triage engine and review the response requirements:\n'
                               '\n'
                               '```sh\n'
                               'python3 incident_triage_engine.py\n'
                               '```\n'
                               '\n'
                               'Confirm that checkout degradation defaults immediately to P1 with a 5-minute MTTA '
                               'target.',
                               '#### Stage 5: Live Verification & Communication Air-Gap Assertions\n'
                               'Author an assertion test (<kbd>test_comms_airgap.py</kbd>) verifying that '
                               'non-responders are barred from technical bridges:\n'
                               '\n'
                               '```python\n'
                               '# test_comms_airgap.py\n'
                               "bridge_participants = ['Sarah Chen (IC)', 'Marcus Vance (Ops)', 'Dave Miller (DBA)']\n"
                               "exec_attendees = ['VP Sales', 'Director Marketing']\n"
                               'for attendee in exec_attendees:\n'
                               "    assert attendee not in bridge_participants, f'{attendee} must be routed to "
                               "executive briefing, not war room'\n"
                               "print('[PASS] Technical war room air gap strictly defended.')\n"
                               '```\n'
                               '\n'
                               'Run the verification test:\n'
                               '\n'
                               '```sh\n'
                               'python3 test_comms_airgap.py\n'
                               '```',
                               '#### Stage 6: Chaos Injection: Unmitigated Executive Intrusion Drill\n'
                               'Author a chaos simulation (<kbd>chaos_exec_interference.py</kbd>) demonstrating how '
                               'executive distraction increases MTTR:\n'
                               '\n'
                               '```python\n'
                               '# chaos_exec_interference.py\n'
                               'def model_mttr_impact(executives_on_call: int) -> float:\n'
                               '    base_mttr_minutes = 20.0\n'
                               '    # Each unmanaged executive on the technical bridge adds 12 minutes of distraction\n'
                               '    return base_mttr_minutes + (executives_on_call * 12.0)\n'
                               '\n'
                               'clean_mttr = model_mttr_impact(0)\n'
                               'disrupted_mttr = model_mttr_impact(3)\n'
                               "print(f'Clean MTTR with Air-Gap: {clean_mttr:.0f} mins | Disrupted MTTR: "
                               "{disrupted_mttr:.0f} mins')\n"
                               "assert disrupted_mttr >= 56.0, 'Disruption should substantially inflate MTTR'\n"
                               "print('[PASS] Chaos test confirms executive interference almost triples outage "
                               "duration.')\n"
                               '```\n'
                               '\n'
                               'Execute the chaos simulation:\n'
                               '\n'
                               '```sh\n'
                               'python3 chaos_exec_interference.py\n'
                               '```',
                               '#### Stage 7: SRE Runbook: Incident Command Playbook\n'
                               'Author the enterprise Incident Response Playbook '
                               '(<kbd>day-087-incident-playbook.md</kbd>):\n'
                               '\n'
                               '```markdown\n'
                               '# Day 87: Enterprise Incident Command Playbook (ICS Protocol)\n'
                               '\n'
                               '## 1. Severity Escalation Matrix\n'
                               '- **P1 (Critical):** Core checkout down. IC appointed immediately; PagerDuty '
                               'auto-pages on-call; 15-min status updates.\n'
                               '- **P2 (Major):** High latency or partial degradation. Ops Lead directs investigation; '
                               '30-min stakeholder updates.\n'
                               '- **P3 (Moderate):** Internal or non-revenue service degraded. Triage within standard '
                               'shift.\n'
                               '- **P4 (Minor):** Cosmetic or background defect. Groomed in sprint backlog.\n'
                               '```',
                               '#### Stage 8: Teardown, Cleanup & Artifact Validation Checklist\n'
                               'Clean up intermediate test scripts and preserve core playbook artifacts:\n'
                               '\n'
                               '```sh\n'
                               'rm -f test_ics_roles.py test_comms_airgap.py chaos_exec_interference.py\n'
                               'ls -lh incident_triage_engine.py day-087-incident-playbook.md\n'
                               '```\n'
                               '\n'
                               'Confirm that <kbd>incident_triage_engine.py</kbd> and '
                               '<kbd>day-087-incident-playbook.md</kbd> are preserved as verifiable day evidence.'],
                     'verification': 'Playbook exists, defines all three primary ICS roles, and includes a complete '
                                     'severity escalation matrix with status update templates.',
                     'trouble': 'Ensure P1 communication templates omit speculative root causes and focus strictly on '
                                'observed impact and mitigation steps.',
                     'cleanup': 'Retain `day-087-topic-01-ics-playbook.md` as an exit evidence artifact.',
                     'accept': 'Completed enterprise incident response playbook with verified role boundaries and '
                               'communication governance.'}},
            {'key': 'topic-02',
             'title': 'Blameless post-mortems and systemic action item tracking',
             'preview': 'After an outage, leadership fires the junior engineer who ran a bad database query. Three '
                        'weeks later, terrified of being blamed, another engineer conceals a production bug for four '
                        'days until it causes a catastrophic customer data loss.',
             'overview': 'The core premise of modern Site Reliability Engineering is that **post-mortems must be '
                         'blameless**. Humans are inherently fallible; if an engineer can take down production with a '
                         'single command or misconfigured configuration, the fundamental fault lies in the '
                         'architecture, automated guardrails, and access policies—not the individual. Punishing '
                         'individuals creates a culture of fear where failures are concealed, near-misses are ignored, '
                         'and systemic bugs fester. A blameless post-mortem assumes that every participant acted in '
                         'good faith with the information they had at the time. By analyzing the incident through '
                         '**The Five Whys** and timeline reconstruction, the organization uncovers systemic root '
                         'causes and produces actionable, preventive engineering fixes (SMART Action Items) that '
                         'permanently eliminate entire classes of failure.',
             'technical': 'Authoring an authoritative post-mortem requires strict adherence to standardized SRE '
                          'rubrics:\n'
                          '\n'
                          '### 1. Second-by-Second Timeline Reconstruction\n'
                          'The foundation of every post-mortem is an objective, high-precision timeline compiled from '
                          'machine logs, metrics, and chat transcripts:\n'
                          '- $t_0$ (Fault Injected): Exact timestamp the error was introduced (e.g. '
                          '`2026-09-28T14:02:11Z` commit merged).\n'
                          '- $t_1$ (User Impact Starts): First observable spike in SLI degradation.\n'
                          '- $t_2$ (Detection / Alert): Monitoring alert fires and on-call engineer paged.\n'
                          '- $t_3$ (Incident Declared): Incident Commander assumes control; war room opened.\n'
                          '- $t_4$ (Mitigation Applied): Action taken that restores user service (e.g. traffic '
                          'drained).\n'
                          '- $t_5$ (Resolution): Systems fully operational, data reconciled, and incident closed.\n'
                          '\n'
                          '### 2. The Five Whys: Distinguishing Proximate Trigger from Systemic Cause\n'
                          'Never stop at the human trigger:\n'
                          '- *Why did checkout fail?* The database ran out of disk space.\n'
                          '- *Why did it run out of space?* A rogue query generated a massive 500GB temporary table.\n'
                          '- *Why did the query run?* An unindexed analytics query was run directly against the '
                          'production primary.\n'
                          '- *Why was it run against the primary?* Analytics credentials had read/write permissions to '
                          'production instead of read-only replica.\n'
                          '- *Why did they have production access?* IAM roles were assigned manually without '
                          'least-privilege automation. (Systemic Cause!)\n'
                          '\n'
                          '### 3. SMART Action Items\n'
                          'Action items must be **Specific, Measurable, Achievable, Relevant, and Time-bound** (e.g., '
                          "'Deploy automated disk auto-resize in Terraform by Oct 15; Owner: Jane D.'). Categorize "
                          'fixes into: **Prevent** (architectural safeguards), **Mitigate** (faster failover), and '
                          '**Detect** (earlier alerting).',
             'questions': ['Why does blaming an individual for an outage increase organizational risk rather than '
                           'decreasing it?',
                           "How does 'The Five Whys' technique uncover systemic architectural flaws beneath human "
                           'operational errors?',
                           'What are the mandatory attributes of a SMART action item in an SRE post-mortem?'],
             'reference': 'https://docs.cloud.google.com/architecture/framework/operational-excellence#post-mortems',
             'reference_label': 'Google Cloud Architecture Framework: Conducting blameless post-mortems',
             'scenario': {'symptom': 'During a scheduled maintenance window, an administrator accidentally ran a '
                                     'Terraform script against the production project instead of staging, destroying '
                                     'the production VPC network and taking down all services for 4 hours.',
                          'constraints': 'Must establish technical safeguards that prevent cross-environment Terraform '
                                         'destruction without slowing down routine deployment pipelines.',
                          'evidence': 'Shell history showed the administrator had active Google Cloud credentials with '
                                      '`roles/owner` across both staging and production projects in a single terminal '
                                      'session, with state files stored in improperly partitioned buckets.',
                          'diagnostic_steps': ['Reconstruct the command execution timeline from Google Cloud Audit '
                                               'Logs (`cloudaudit.googleapis.com/activity`).',
                                               'Audit Terraform state bucket permissions and workspace configuration.',
                                               'Conduct a Five Whys analysis to determine why the CLI command lacked '
                                               'production environment fencing.'],
                          'root': 'Systemic lack of environment isolation: production and staging infrastructure '
                                  'shared administrative credential sessions, lacked automated Terraform `-target` '
                                  'plan reviews, and possessed no `prevent_destroy` lifecycle rules on core VPC '
                                  'resources.',
                          'fix': 'Enforce strict organizational boundaries: isolate production and staging into '
                                 'separate GCP folders, require separate Service Account impersonation with '
                                 'short-lived tokens, enforce `lifecycle { prevent_destroy = true }` in Terraform on '
                                 'all network resources, and mandate automated CI/CD execution via Cloud Build with '
                                 'pull request approval gates.',
                          'verify': 'Attempt a simulated `terraform destroy` against production in CI/CD; verify the '
                                    'pipeline blocks execution with a policy-as-code error.',
                          'residual': 'Authorized resource decommissioning requires an explicit multi-step PR to '
                                      'remove the `prevent_destroy` block before destruction.',
                          'diagram': ('Shared credentials active',
                                      'Terraform applied to prod',
                                      'Production VPC destroyed',
                                      'Terrform prevent_destroy',
                                      'Zero cross-env destruction'),
                          'facts': 'Administrator destroyed production VPC because local shell held unhedged '
                                   'credentials for both environments.',
                          'inference': 'Human error is inevitable; systems that permit total destruction via single '
                                       'unvalidated commands are defective.',
                          'expected': 'Terraform policy-as-code and GCP project isolation prevent accidental '
                                      'destruction of critical foundation assets.'},
             'lab': {'name': 'Blameless Post-Mortem Authoring and Action Item Registry',
                     'file': 'day-087-topic-02-post-mortem.md',
                     'goal': 'Author a comprehensive, blameless post-mortem for a simulated production failure, '
                             'complete with timeline and SMART action items.',
                     'expected': 'A production-grade Markdown post-mortem document adhering to Google SRE standards '
                                 'with Five Whys causal analysis.',
                     'mode': 'tabletop analysis & post-mortem authoring',
                     'prereq': 'Completion of Exercise 1.',
                     'preflight': 'Review post-mortem template in workspace.',
                     'steps': ['#### Stage 1: Pre-Flight Blameless Post-Mortem Principles & Five Whys Scope\n'
                               'Establish Google SRE blameless post-mortem tenets:\n'
                               '- **Psychological Safety:** Human error is a symptom of inadequate systemic '
                               'guardrails, not a root cause.\n'
                               '- **Five Whys:** Traverse beyond immediate mechanical triggers to organizational and '
                               'systemic defects.\n'
                               '- **Timeline Reconstruction:** Second-by-second chronological reconciliation of '
                               'monitoring alerts and operator actions.\n'
                               '- **SMART Action Items:** Specific, Measurable, Achievable, Relevant, and Time-bound '
                               'preventive engineering fixes.',
                               '#### Stage 2: Environment Preflight & Timeline Chronology Checker\n'
                               'Author a test script (<kbd>test_timeline_chronology.py</kbd>) verifying that log event '
                               'timestamps are strictly monotonic:\n'
                               '\n'
                               '```python\n'
                               '# test_timeline_chronology.py\n'
                               'from datetime import datetime\n'
                               'events = [\n'
                               "    ('2026-09-28T04:12:00Z', 'DDL Migration Triggered'),\n"
                               "    ('2026-09-28T04:12:30Z', 'Cloud SQL Lock Acquired'),\n"
                               "    ('2026-09-28T04:13:10Z', 'P1 Multi-Burn Alert Fired'),\n"
                               "    ('2026-09-28T04:22:00Z', 'Traffic Drained; Service Restored')\n"
                               ']\n'
                               "times = [datetime.fromisoformat(e[0].replace('Z', '+00:00')) for e in events]\n"
                               "assert times == sorted(times), 'Timeline events must be strictly chronological'\n"
                               "print('[PASS] Timeline monotonicity validated.')\n"
                               '```\n'
                               '\n'
                               'Run the preflight test:\n'
                               '\n'
                               '```sh\n'
                               'python3 test_timeline_chronology.py\n'
                               '```',
                               '#### Stage 3: Core Implementation: Five Whys Causal Engine\n'
                               'Author the causal audit script (<kbd>five_whys_engine.py</kbd>) that links mechanical '
                               'symptoms to architectural flaws:\n'
                               '\n'
                               '```python\n'
                               '#!/usr/bin/env python3\n'
                               '"""five_whys_engine.py — Traverses five whys to uncover systemic root causes."""\n'
                               'from typing import List, Tuple\n'
                               '\n'
                               'FIVE_WHYS_CHAIN = [\n'
                               "    (1, 'Why did the service fail?', 'Workload pods timed out connecting to the "
                               "database.'),\n"
                               "    (2, 'Why did connections time out?', 'The database held an exclusive table lock on "
                               "the orders table.'),\n"
                               "    (3, 'Why was an exclusive lock held?', 'An ALTER TABLE migration script executed "
                               "without ghost/online expansion.'),\n"
                               "    (4, 'Why was ghost migration omitted?', 'The migration tool lacked automated DDL "
                               "linter integration in CI/CD.'),\n"
                               "    (5, 'Why was DDL linting absent?', 'Platform engineering prioritized release "
                               "velocity over schema guardrails.')\n"
                               ']\n'
                               '\n'
                               "if __name__ == '__main__':\n"
                               "    print('=' * 80)\n"
                               "    print('BLAMELESS POST-MORTEM FIVE WHYS CAUSAL AUDIT')\n"
                               "    print('=' * 80)\n"
                               '    for level, q, a in FIVE_WHYS_CHAIN:\n'
                               "        print(f'Level {level}: {q}\\n  -> {a}')\n"
                               "    assert len(FIVE_WHYS_CHAIN) == 5, 'Must have complete 5-level causal depth'\n"
                               "    print('[PASS] Five whys analysis reached systemic architectural policy level.')\n"
                               '```',
                               '#### Stage 4: Execution & Five Whys Causal Audit\n'
                               'Execute the Five Whys causal engine:\n'
                               '\n'
                               '```sh\n'
                               'python3 five_whys_engine.py\n'
                               '```\n'
                               '\n'
                               'Confirm that root cause analysis terminates at architectural guardrails rather than '
                               'individual engineer blame.',
                               '#### Stage 5: Live Verification & SMART Action Item Linting\n'
                               'Author an assertion test (<kbd>test_smart_action_lint.py</kbd>) verifying that action '
                               'items meet SMART criteria:\n'
                               '\n'
                               '```python\n'
                               '# test_smart_action_lint.py\n'
                               'actions = [\n'
                               "    {'desc': 'Deploy Liquibase online schema linter in CI/CD', 'owner': 'Platform "
                               "Team', 'deadline': '2026-10-15', 'type': 'PREVENT'},\n"
                               "    {'desc': 'Add Cloud Monitoring connection pool saturation alert', 'owner': 'SRE "
                               "Team', 'deadline': '2026-10-05', 'type': 'DETECT'}\n"
                               ']\n'
                               'for a in actions:\n'
                               "    assert a['owner'] and a['deadline'] and a['type'] in ('PREVENT', 'DETECT', "
                               "'MITIGATE')\n"
                               "print('[PASS] SMART action items verified: Every item has an explicit owner and "
                               "deadline.')\n"
                               '```\n'
                               '\n'
                               'Run the verification assertions:\n'
                               '\n'
                               '```sh\n'
                               'python3 test_smart_action_lint.py\n'
                               '```',
                               '#### Stage 6: Chaos Injection: Punitive Post-Mortem Anti-Pattern Drill\n'
                               'Author a chaos script (<kbd>chaos_blame_test.py</kbd>) demonstrating how punitive '
                               'blame suppresses incident disclosure:\n'
                               '\n'
                               '```python\n'
                               '# chaos_blame_test.py\n'
                               'def evaluate_culture(is_punitive: bool) -> str:\n'
                               '    if is_punitive:\n'
                               "        return 'CULTURE_COLLAPSE: Engineers hide near-misses; systemic defects remain "
                               "unpatched until catastrophic failure!'\n"
                               "    return 'BLAMELESS_LEARNING'\n"
                               '\n'
                               'res = evaluate_culture(is_punitive=True)\n'
                               "assert 'CULTURE_COLLAPSE' in res\n"
                               "print('[PASS] Chaos drill confirms blameless culture is necessary for organizational "
                               "survival.')\n"
                               '```\n'
                               '\n'
                               'Execute the blame demonstration:\n'
                               '\n'
                               '```sh\n'
                               'python3 chaos_blame_test.py\n'
                               '```',
                               '#### Stage 7: SRE Runbook: Comprehensive Post-Mortem Document\n'
                               'Author the completed post-mortem artifact (<kbd>day-087-post-mortem.md</kbd>):\n'
                               '\n'
                               '```markdown\n'
                               '# Day 87: Blameless Post-Mortem — Order API Database Migration Outage\n'
                               '\n'
                               '## 1. Incident Overview\n'
                               '- **Date:** 2026-09-28 | **Duration:** 10 minutes (04:12 UTC – 04:22 UTC).\n'
                               '- **Impact:** 18,400 orders dropped; $42,000 estimated lost revenue.\n'
                               '- **Severity:** P1 Critical.\n'
                               '\n'
                               '## 2. Five Whys Summary\n'
                               '- Root Cause: Exclusive DDL table lock blocked order writes; CI/CD lacked automated '
                               'online schema linting.\n'
                               '\n'
                               '## 3. SMART Action Items\n'
                               '1. [PREVENT] Author CI/CD pre-commit DDL linter blocking exclusive table locks (Owner: '
                               'Platform, Due: Oct 15).\n'
                               '2. [DETECT] Configure Cloud Monitoring alert on pg_stat_activity lock wait time > 5s '
                               '(Owner: SRE, Due: Oct 05).\n'
                               '```',
                               '#### Stage 8: Teardown, Cleanup & Artifact Validation Checklist\n'
                               'Clean up temporary test scripts and verify finalized artifacts:\n'
                               '\n'
                               '```sh\n'
                               'rm -f test_timeline_chronology.py test_smart_action_lint.py chaos_blame_test.py\n'
                               'ls -lh five_whys_engine.py day-087-post-mortem.md\n'
                               '```\n'
                               '\n'
                               'Confirm that <kbd>five_whys_engine.py</kbd> and <kbd>day-087-post-mortem.md</kbd> are '
                               'preserved as verifiable day evidence.'],
                     'verification': 'Document exists, includes second-by-second timeline, Five Whys analysis, and '
                                     'five SMART action items with assigned owners.',
                     'trouble': 'Ensure every action item specifies a measurable verification check and a calendar '
                                'completion target.',
                     'cleanup': 'Retain `day-087-topic-02-post-mortem.md` as an exit evidence artifact.',
                     'accept': 'Mastery of the blameless post-mortem process and actionable engineering remediation '
                               'tracking.'}},
            {'key': 'topic-03',
             'title': 'Capacity planning, load forecasting, and Google Cloud quota management',
             'preview': 'Brightloaf launches a major nationwide promotion expected to generate 5x normal traffic. Two '
                        'minutes after launch, autoscaling abruptly stops because the project hit the default regional '
                        '`CPUS_ALL_REGIONS` quota ceiling, dropping 60% of new customer checkouts.',
             'overview': 'Capacity planning is the proactive engineering discipline of ensuring that cloud '
                         'infrastructure possesses sufficient computing, storage, and network resources to satisfy '
                         'anticipated user demand without violating SLOs or incurring wasteful over-provisioning '
                         'costs. In Google Cloud, capacity is governed by hard physical and administrative boundaries: '
                         '**quotas** (enforced ceilings on API requests and resources like vCPUs or public IPs) and '
                         '**capacity limits** (physical server availability in specific zones). Architects must model '
                         'organic growth alongside seasonal flash surges, enforce **N+1 regional redundancy** '
                         '(guaranteeing sufficient headroom to absorb the loss of an entire availability zone), and '
                         'audit GCP quota allocations at least 4 to 6 weeks prior to major commercial events.',
             'technical': 'Capacity planning requires rigorous mathematical modeling and proactive quota governance:\n'
                          '\n'
                          '### 1. The N+1 Multi-Zone Headroom Rule\n'
                          'If a system distributes load across $Z$ availability zones in a region, the loss of one '
                          'zone increases the load on remaining zones to:\n'
                          '$$\\text{Load per surviving zone} = \\frac{1}{Z - 1} \\times 100\\%$$\n'
                          '- Across 3 zones ($Z=3$): losing 1 zone forces remaining 2 zones to absorb $50\\%$ of total '
                          'load each (a **50% traffic surge per zone**).\n'
                          '- SRE Mandate: Baseline steady-state utilization per zone must never exceed:\n'
                          '$$\\text{Max Baseline Utilization} = \\frac{Z - 1}{Z} \\times 80\\%$$\n'
                          '- For $Z=3$: $(2/3) \\times 80\\% = \\mathbf{53.3\\%}$. If a 3-zone cluster operates above '
                          '53.3% utilization, losing a single zone pushes surviving zones past the 80% saturation '
                          'cliff, triggering immediate cascading failure!\n'
                          '\n'
                          '### 2. Google Cloud Quota Architecture\n'
                          '- **Resource Quotas:** E.g., `compute.googleapis.com/cpus` (regional), '
                          '`compute.googleapis.com/in_use_addresses` (regional static IPs), '
                          '`cloudsql.googleapis.com/instances`.\n'
                          '- **Rate Quotas:** API call rates (e.g. 1,000 `instances.insert` calls per 100 seconds).\n'
                          '- Quotas prevent runaway billing and protect provider multitenant stability. Quota '
                          'increases require human review and can take 2 to 5 business days.\n'
                          '\n'
                          '### 3. Proactive Load Forecasting Equations\n'
                          'Calculate required vCPUs ($C_{\\text{req}}$) from forecast peak QPS ($Q$), single-core '
                          'capacity ($Q_{\\text{core}}$), and target maximum utilization ($\\rho = 0.70$):\n'
                          '$$C_{\\text{req}} = \\left\\lceil \\frac{Q}{Q_{\\text{core}} \\times \\rho} \\right\\rceil '
                          '\\times \\frac{Z}{Z - 1}$$',
             'questions': ['Why must a 3-zone regional cluster maintain steady-state CPU utilization below 53.3% to '
                           'survive the complete loss of one zone?',
                           'What is the operational difference between a regional resource quota and a rate-limiting '
                           'API quota in Google Cloud?',
                           'Why must enterprise quota increases be requested weeks in advance of planned commercial '
                           'marketing promotions?'],
             'reference': 'https://docs.cloud.google.com/architecture/framework/reliability/capacity-planning',
             'reference_label': 'Google Cloud Architecture Framework: Sizing, forecasting, and quota management',
             'scenario': {'symptom': "During a Cyber Monday sale, Brightloaf's GKE cluster attempted to autoscale from "
                                     '30 nodes to 75 nodes to handle an 8,000 QPS surge. The GKE Cluster Autoscaler '
                                     "stalled at 48 nodes, emitting events: `Quota 'CPUS' exceeded in region "
                                     'us-central1`. Incoming requests queued up and 45% of user checkouts failed.',
                          'constraints': 'Must accommodate flash promotions up to 10,000 QPS while maintaining N+1 '
                                         'multi-zone resilience and staying within approved FinOps annual budgets.',
                          'evidence': 'Google Cloud Quota console showed `compute.googleapis.com/cpus` ceiling in '
                                      '`us-central1` was set to the default of 400 vCPUs. The 48 running '
                                      '`c2-standard-8` nodes consumed 384 vCPUs, leaving insufficient quota to '
                                      'schedule the remaining 27 requested nodes.',
                          'diagnostic_steps': ['Query Cloud Logging for `resource.type="k8s_cluster"` and filter by '
                                               '`scaleUp: failedQuota`.',
                                               'Audit Google Cloud Quotas console across all target regions for '
                                               'Compute Engine CPUs and In-Use Public IP addresses.',
                                               'Calculate peak vCPU demand using historical single-pod QPS benchmark '
                                               'metrics.'],
                          'root': 'Capacity planning failed to audit regional GCP quotas prior to a planned 5x '
                                  'marketing promotion, allowing autoscaling to hit an unmonitored administrative '
                                  'quota ceiling during peak traffic.',
                          'fix': 'Establish a formal pre-event Capacity Checklist: submit quota increase requests for '
                                 '1,200 vCPUs 4 weeks in advance, configure Cloud Monitoring quota utilization alerts '
                                 'at 75%, and implement multi-region overflow routing via Global Load Balancer to '
                                 'spill excess load into `us-east1`.',
                          'verify': 'Verify `gcloud compute regions describe us-central1` shows quota increased to '
                                    '1,200 vCPUs; simulate synthetic node autoscale in staging to 80 nodes.',
                          'residual': 'Unused idle quota costs nothing in GCP, but commitments (CUDs) require careful '
                                      'modeling to avoid paying for excess reserved headroom.',
                          'diagram': ('8k QPS surge arrives',
                                      'GCP 400 CPU quota hit',
                                      'Autoscaling stalls (45% 5xx)',
                                      'Pre-event quota increase',
                                      'Clean 75-node autoscale'),
                          'facts': 'Cluster autoscaler choked at 48 nodes because regional CPU quota was capped at 400 '
                                   'vCPUs.',
                          'inference': 'Autoscaling policies are completely useless if underlying cloud provider '
                                       'quotas are not proactively sized.',
                          'expected': 'Pre-provisioned quota headroom allows cluster to autoscale seamlessly up to '
                                      'planned peak capacity.'},
             'lab': {'name': 'N+1 Multi-Zone Headroom and Quota Sizing Engine',
                     'file': 'day-087-topic-03-capacity-calc.py',
                     'goal': 'Write and run a Python capacity planning tool calculating N+1 multi-zone headroom and '
                             'required Google Cloud regional quotas.',
                     'expected': 'A runnable script computing maximum steady-state utilization targets and generating '
                                 'GCP quota request specifications.',
                     'mode': 'local script execution & verification',
                     'prereq': 'Completion of Exercises 1 and 2.',
                     'preflight': 'Verify Python runtime and initialize script template.',
                     'steps': ['#### Stage 1: Pre-Flight Capacity Planning & N+1 Headroom Formulation\n'
                               'Establish the mathematical formulation of N+1 multi-zone capacity planning:\n'
                               '- **N+1 Rule:** If a regional deployment requires $N$ units of compute to serve peak '
                               'demand across $Z$ availability zones, the cluster must be provisioned with '
                               '$\\frac{Z}{Z-1} \\times N$ total capacity.\n'
                               '- For 3 zones, cluster must provision $1.5 \\times N$ (50% headroom total, or 50% '
                               'capacity in each of the 3 zones), ensuring that if 1 zone suffers a total power '
                               'failure, the remaining 2 zones handle 100% of peak load.\n'
                               '- **Google Cloud Quotas:** Compute Engine vCPU and IP quotas must be pre-allocated to '
                               'accommodate full N+1 failover surge without encountering `QUOTA_EXCEEDED` errors.',
                               '#### Stage 2: Environment Preflight & Quota Verification Script\n'
                               'Author a test script (<kbd>test_quota_math.py</kbd>) calculating required N+1 instance '
                               'counts across 3 zones:\n'
                               '\n'
                               '```python\n'
                               '# test_quota_math.py\n'
                               'def calculate_n_plus_one_capacity(peak_instances: int, zones: int = 3) -> int:\n'
                               "    assert zones >= 2, 'Need at least 2 zones for N+1'\n"
                               '    instances_per_zone = -(-peak_instances // (zones - 1))  # ceiling divide\n'
                               '    total_provisioned = instances_per_zone * zones\n'
                               '    return total_provisioned\n'
                               '\n'
                               'total = calculate_n_plus_one_capacity(peak_instances=10, zones=3)\n'
                               "print(f'Peak Required: 10 instances across 3 zones -> Provisioned Total: {total} (5 "
                               "per zone)')\n"
                               "assert total == 15, '15 total instances needed so any 2 zones provide 10 instances'\n"
                               "print('[PASS] N+1 capacity mathematics verified.')\n"
                               '```\n'
                               '\n'
                               'Execute the preflight test:\n'
                               '\n'
                               '```sh\n'
                               'python3 test_quota_math.py\n'
                               '```',
                               '#### Stage 3: Core Implementation: Capacity Sizing & Quota Forecaster\n'
                               'Author the complete capacity sizing and GCP quota forecasting script '
                               '(<kbd>capacity_forecaster.py</kbd>):\n'
                               '\n'
                               '```python\n'
                               '#!/usr/bin/env python3\n'
                               '"""capacity_forecaster.py — Models seasonal traffic peaks and calculates required GCP '
                               'quotas."""\n'
                               'from typing import Dict\n'
                               '\n'
                               'def size_infrastructure(baseline_rps: float, seasonal_growth: float, '
                               'vcpu_per_instance: int = 4, rps_per_instance: float = 150.0) -> Dict:\n'
                               '    peak_rps = baseline_rps * seasonal_growth\n'
                               '    required_instances = int(-(-peak_rps // rps_per_instance))\n'
                               '    # Apply N+1 across 3 zones\n'
                               '    per_zone = int(-(-required_instances // 2))\n'
                               '    total_instances = per_zone * 3\n'
                               '    total_vcpus = total_instances * vcpu_per_instance\n'
                               '    # Add 25% safety buffer for quota limit\n'
                               '    recommended_quota_vcpu = int(total_vcpus * 1.25)\n'
                               '    return {\n'
                               "        'peak_rps': peak_rps,\n"
                               "        'required_instances': required_instances,\n"
                               "        'n_plus_one_instances': total_instances,\n"
                               "        'total_vcpus': total_vcpus,\n"
                               "        'recommended_quota_vcpu': recommended_quota_vcpu\n"
                               '    }\n'
                               '\n'
                               "if __name__ == '__main__':\n"
                               '    res = size_infrastructure(baseline_rps=1000.0, seasonal_growth=2.5)\n'
                               "    print('=' * 75)\n"
                               "    print('N+1 CAPACITY & GOOGLE CLOUD QUOTA FORECAST')\n"
                               "    print('=' * 75)\n"
                               '    print(f"Peak Demand:         {res[\'peak_rps\']:,.0f} requests/sec")\n'
                               '    print(f"N+1 Instances:       {res[\'n_plus_one_instances\']} instances (across 3 '
                               'zones)")\n'
                               '    print(f"Target vCPUs:        {res[\'total_vcpus\']} vCPUs")\n'
                               '    print(f"Recommended Quota:   {res[\'recommended_quota_vcpu\']} vCPUs (with 25% '
                               'headroom)")\n'
                               "    assert res['recommended_quota_vcpu'] >= res['total_vcpus'] * 1.20\n"
                               "    print('[PASS] Capacity forecast completed with verified quota headroom.')\n"
                               '```',
                               '#### Stage 4: Execution & Peak Load Sizing Analysis\n'
                               'Execute the capacity forecaster:\n'
                               '\n'
                               '```sh\n'
                               'python3 capacity_forecaster.py\n'
                               '```\n'
                               '\n'
                               'Confirm that a 2.5x traffic surge calculates appropriate N+1 instance counts and '
                               'recommended vCPU quota requests.',
                               '#### Stage 5: Live Verification & Zonal Blackout Failover Headroom\n'
                               'Author an assertion test (<kbd>test_headroom_assertions.py</kbd>) proving surviving '
                               'zones absorb 100% of peak load:\n'
                               '\n'
                               '```python\n'
                               '# test_headroom_assertions.py\n'
                               'from capacity_forecaster import size_infrastructure\n'
                               '\n'
                               'cfg = size_infrastructure(baseline_rps=800.0, seasonal_growth=2.0)\n'
                               "per_zone = cfg['n_plus_one_instances'] // 3\n"
                               'surviving_capacity_instances = per_zone * 2\n'
                               'surviving_rps = surviving_capacity_instances * 150.0\n'
                               "assert surviving_rps >= cfg['peak_rps'], 'Surviving zones must meet or exceed peak "
                               "demand'\n"
                               "print(f'[PASS] Surviving capacity ({surviving_rps:,.0f} rps) meets peak demand "
                               '({cfg["peak_rps"]:,.0f} rps).\')\n'
                               '```\n'
                               '\n'
                               'Run the verification assertions:\n'
                               '\n'
                               '```sh\n'
                               'python3 test_headroom_assertions.py\n'
                               '```',
                               '#### Stage 6: Chaos Injection: Quota Exhaustion During Surge Drill\n'
                               'Author a chaos simulation (<kbd>chaos_quota_rejection.py</kbd>) demonstrating what '
                               'occurs when quota requests are neglected:\n'
                               '\n'
                               '```python\n'
                               '# chaos_quota_rejection.py\n'
                               'def attempt_autoscale(needed_vcpus: int, quota_limit: int) -> str:\n'
                               '    if needed_vcpus > quota_limit:\n'
                               "        return 'QUOTA_EXCEEDED: Compute Engine rejected instance creation; traffic "
                               "dropped!'\n"
                               "    return 'AUTOSCALE_SUCCESS'\n"
                               '\n'
                               'res = attempt_autoscale(needed_vcpus=120, quota_limit=64)\n'
                               "assert 'QUOTA_EXCEEDED' in res\n"
                               "print('[PASS] Chaos drill confirms unadjusted quotas prevent autoscaling recovery.')\n"
                               '```\n'
                               '\n'
                               'Execute the quota rejection simulation:\n'
                               '\n'
                               '```sh\n'
                               'python3 chaos_quota_rejection.py\n'
                               '```',
                               '#### Stage 7: SRE Runbook: Google Cloud Quota Management Runbook\n'
                               'Author the operational quota management guide (<kbd>day-087-quota-runbook.md</kbd>):\n'
                               '\n'
                               '```markdown\n'
                               '# Day 87: Google Cloud Quota Sizing and Lead-Time Management\n'
                               '\n'
                               '## 1. Quota Review Timetable\n'
                               '- Quota review must be conducted **60 days prior** to major retail promotions.\n'
                               '- Quota requests exceeding +100% required vCPUs require GCP TAM engagement with 3-week '
                               'lead times.\n'
                               '```',
                               '#### Stage 8: Teardown, Cleanup & Artifact Validation Checklist\n'
                               'Clean up temporary test scripts and retain core capacity artifacts:\n'
                               '\n'
                               '```sh\n'
                               'rm -f test_quota_math.py test_headroom_assertions.py chaos_quota_rejection.py\n'
                               'ls -lh capacity_forecaster.py day-087-quota-runbook.md\n'
                               '```\n'
                               '\n'
                               'Confirm that <kbd>capacity_forecaster.py</kbd> and <kbd>day-087-quota-runbook.md</kbd> '
                               'are preserved as verifiable day evidence.'],
                     'verification': 'Script runs cleanly and displays accurate mathematical sizing for N+1 multi-zone '
                                     'resilience and GCP quota allocation.',
                     'trouble': 'Ensure steady-state utilization formula multiplies `target_util` by `(zones - 1) / '
                                'zones`.',
                     'cleanup': 'Retain `day-087-topic-03-capacity-calc.py` as an exit evidence artifact.',
                     'accept': 'Demonstrated mastery of N+1 multi-zone capacity planning and Google Cloud quota '
                               'management.'}}],
 'part3_intro': 'The following field cases analyze real-world production catastrophes resulting from organizational '
                'chaos during uncoordinated incident response, punitive post-mortem cultures that conceal systemic '
                'defects, and quota exhaustion during seasonal traffic spikes. Each case details quantifiable failure '
                'metrics, verbatim terminal/log transcripts, diagnostic command sequences, root cause mechanics, '
                'defensible remediations, and dual-lane failed/corrected architectural diagrams.',
 'part4_intro': 'These hands-on exercises follow the 8-stage operational engineering lifecycle. Engineers author '
                'production incident triage matrices, reconstruct high-fidelity incident timelines, formulate '
                'blameless post-mortems with Five Whys causal analyses, build automated Python capacity forecasting '
                'models incorporating N+1 redundancy, and verify recovery against strict acceptance criteria with zero '
                'difficulty labels.'}
