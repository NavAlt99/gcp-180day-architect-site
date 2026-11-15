# Page quality standard (all days)

Read once per run. This file defines what a good explanation is. The contract and
standing rules R1-R13 still apply; this standard never overrides them.

1. **Reader.** A beginner with basic computing knowledge and no networking or
   cloud background. Every term, abbreviation and diagram label (for example A, B,
   R, R-left, R-right) is defined in words at its first use in the text.
2. **One idea per paragraph, at most three sentences.** A list item may contain
   several short paragraphs. Check whether R2 and `check_page_rules.py` accept
   multiple `<p>` inside one `<li>`; if not, use `<br><br>` inside the same `<li>`.
   Keep the exact `<li><strong class="side-heading">Label:</strong>` form either way.
3. **Order.** Observation or plain-language explanation first, an analogy for any
   abstract idea, then the precise term, then the architect's decision.
4. **Worked starting point.** States a concrete observation: command output, a
   number from the scenario, a quoted log line or a named scenario. It never
   restates the dossier title. A digit inside a name (IPv4, Day 2) is not
   evidence, whatever R11 accepts.
5. **Predicted output** is allowed only when labelled "Simulated or predicted:".
   Never present it as captured.
6. **Relevance to GCP.** Teaches documented behaviour with a primary source and
   labels inference as inference. No claims about Google internals unless documented.
7. **Evidence limit.** Names exactly what was not tested.
8. **Tone.** No emphasis by capitals or exclamation marks. Nothing is stated more
   strongly than its source.
9. **Template.** Keep the exact labels: What it is in general / Relevance to a
   cloud architect / Relevance to GCP / Further study / Concrete example /
   Evidence limit. Dossiers keep the six rows: Mechanism, Ownership and boundary,
   Failure reasoning, Trade-off or limit, Verification checkpoint, Evidence limit.
10. **Shared text** (method notes, scope guards) is written once at the level it
    applies to, never repeated per dossier.
