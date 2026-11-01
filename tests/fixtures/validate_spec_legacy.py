from tests.fixtures.spec_factory import spec

_SPEC = spec(3, contract_version=1)
DAY = 3
ACCESS_DATE = '2026-10-01'
SOURCES = {'fixture': ('Fixture section (accessed 2026-10-01)', 'https://example.test/docs#section')}
TOPICS = _SPEC['topics']
PART1_INTRO = '<strong class="side-heading">Legacy Part 1 fixture.</strong>'
PART2_INTRO = _SPEC['part2_intro']
PART3_INTRO = _SPEC['part3_intro']
PART4_INTRO = _SPEC['part4_intro']
EXIT_SUMMARY = _SPEC['exit_summary']
