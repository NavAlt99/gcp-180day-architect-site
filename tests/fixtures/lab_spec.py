"""Offline executable fixture: state, multiple blocks, and authored cleanup."""
def stage(i, command, save):
    return f'**Stage {i}: fixture**\n\n**Location:** Local Linux Bash terminal.\n\n```bash\n{command}\n```\n\n**Expected result:** file saved.\n\n**Save:** {save}'

STEPS = [stage(1, '''command -v python3
command -v mktemp
LAB_DIR=$(mktemp -d /tmp/fixture.XXXXXX)
cd "$LAB_DIR"
export FIXTURE_STATE=retained
printf ready > preflight.log''', 'preflight.log')]
STEPS += [stage(i, f'test "$FIXTURE_STATE" = retained\nprintf stage{i} > stage{i}.txt', f'stage{i}.txt') for i in range(2, 8)]
STEPS += [stage(8, 'rm stage2.txt\nprintf closed > cleanup.log', 'cleanup.log')]
DATA = {'day': 1, 'topics': [{'key': 'topic-01', 'title': 'Fixture', 'lab': {'name': 'Fixture', 'steps': STEPS}}]}
