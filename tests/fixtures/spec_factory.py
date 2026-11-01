"""Static authored-spec fixtures for validator tests.

These deliberately avoid importing curriculum day specs. Tests may mutate the
returned dictionaries without coupling their expectations to authored content.
"""
from copy import deepcopy


TITLES = {
    2: ('Fixture layers', 'Fixture addressing', 'Fixture packet path'),
    3: ('Fixture IPv6', 'Fixture DNS', 'Fixture transport'),
    4: ('Fixture HTTP', 'Fixture TLS', 'Fixture MTU'),
}


def coverage(day):
    return [{
        'day': str(day),
        'topic_key': f'topic-{index:02d}',
        'topic': title,
        'overview_anchor': f'topic-{index:02d}-overview',
        'technical_anchor': f'topic-{index:02d}-technical',
        'problem_anchor': f'topic-{index:02d}-problem',
        'lab_anchor': f'topic-{index:02d}-lab',
        'publisher_url': 'https://example.test/docs#section',
    } for index, title in enumerate(TITLES[day], 1)]


def diagram(index):
    return f'''<figure class="diagram-figure">
<svg viewBox="0 0 120 60" role="img" aria-labelledby="fixture-title-{index} fixture-desc-{index}">
<title id="fixture-title-{index}">Fixture request path {index}</title>
<desc id="fixture-desc-{index}">A client sends a request to a target.</desc>
<image href="../assets/icons/generic/client.svg" x="8" y="8" width="24" height="24"/>
<rect x="70" y="8" width="36" height="24"/>
</svg><figcaption>Scope: static validator fixture.</figcaption></figure>'''


def technical(index):
    figure = diagram(index) if index in (2, 3) else ''
    return f'''<p>Subtopics in this discussion:</p><ul><li>Fixture mechanism {index}</li></ul>
<h4>Fixture mechanism {index}</h4>
<p><strong class="keyword">Fixture term</strong>. <strong>What it is in general:</strong> A bounded mechanism.</p>
<p><strong>Relevance to a cloud architect:</strong> It exposes ownership and failure boundaries.</p>
<p><strong>Relevance to GCP:</strong> This fixture makes no product claim. <a href="https://example.test/docs#section">Fixture section (accessed 2026-10-01)</a></p>
<p><strong>Concrete example:</strong> A request crosses one boundary. <strong>Evidence limit:</strong> Static test data only.</p>{figure}'''


def stage(index):
    return (f'**Stage {index}: fixture action**\n\n**Location:** local worksheet.\n\n'
            f'1. Record fixture input {index}.\n2. Confirm fixture result {index}.\n\n'
            f'**Expected result:** Fixture stage {index} is recorded.\n\n**Save:** fixture-stage-{index}.txt')


def topic(index, title):
    key = f'topic-{index:02d}'
    return {
        'key': key,
        'title': title,
        'preview': 'A fixture symptom appears. A fixture user sees an effect.',
        'technical': technical(index),
        'reference': 'https://example.test/docs#section',
        'reference_label': 'Fixture section (accessed 2026-10-01)',
        'scenario': {'diagram_enabled': False},
        'lab': {
            'name': f'Fixture lab {index}',
            'covers': 'Inspect the supplied fixture.',
            'mode': 'Observed locally: none. Simulated or predicted: fixture. Untested on GCP: all.',
            'prereq': 'A text editor.',
            'preflight': 'Confirm the fixture is present.',
            'trouble': 'Re-read the fixture input.',
            'cleanup': 'Delete only fixture notes.',
            'steps': [stage(i) for i in range(1, 9)],
        },
    }


def spec(day, contract_version=1):
    topics = [topic(index, title) for index, title in enumerate(TITLES[day], 1)]
    incident_index = 0 if day == 4 else 2 if day == 2 else None
    if incident_index is not None:
        topics[incident_index]['scenario'] = {
            'diagram_enabled': True,
            'diagram': ('Fixture trigger', 'Fixture defect', 'Fixture impact',
                        'Fixture control', 'Fixture outcome'),
            'facts': 'Supplied fixture facts.',
            'inference': 'Architectural fixture inference.',
            'expected': 'Expected post-fix fixture behavior.',
        }
    cards = ''.join(
        f'''<article id="topic-{index:02d}-overview">
<p><strong class="side-heading">Why today:</strong> Static validator coverage.</p>
<p><strong class="side-heading">Where it sits:</strong> Inside the fixture boundary.</p>
<p class="problem-preview"><strong class="side-heading">Problem preview:</strong> A fixture symptom appears. A fixture user sees an effect.</p>
</article>'''
        for index in range(1, len(topics) + 1)
    )
    data = {
        'day': day,
        'contract_version': contract_version,
        'roadmap_practice': 'Inspect the supplied fixture.',
        'roadmap_exit': 'A saved fixture record.',
        'part1_html': cards,
        'part2_intro': 'Static technical fixture.',
        'part3_intro': 'Static scenario fixture.',
        'part4_intro': 'Static lab fixture.',
        'exit_summary': 'A saved fixture record.',
        'topics': topics,
    }
    return deepcopy(data)
