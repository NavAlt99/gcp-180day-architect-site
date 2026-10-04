from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from scripts.spec_v2_checks import check, file_checks


def fixture():
    return {'contract_version':2, 'roadmap_practice':'Compare supplied traces.', 'roadmap_exit':'Worksheet.',
            'sources':{'rfc':('Status (accessed 2026-10-04)', 'https://example.test/doc#status')},
            'topics':[{'key':'topic-01','lab':{'covers':'Compare supplied traces.',
                'mode':'Observed locally: none. Simulated or predicted: fixtures. Untested on GCP: all.',
                'steps':['```bash\ncommand -v ping\nping 127.0.0.1\n```']+['```bash\necho ok\n```']*7}}]}


class StrictChecks(unittest.TestCase):
    def test_required_fields_pass_and_fail(self):
        self.assertEqual(check(fixture()), ([], []))
        for field in ('roadmap_practice','roadmap_exit'):
            data=fixture(); data[field]=''
            self.assertTrue(any(field in e for e in check(data)[0]))
        data=fixture(); del data['topics'][0]['lab']['covers']
        self.assertTrue(any('covers' in e for e in check(data)[0]))

    def test_modes_pass_fail_each(self):
        for label in ('Observed locally:', 'Simulated or predicted:', 'Untested on GCP:'):
            data=fixture(); data['topics'][0]['lab']['mode']=data['topics'][0]['lab']['mode'].replace(label,'')
            self.assertTrue(any(label in e for e in check(data)[0]))
        self.assertFalse(check(fixture())[0])

    def test_masking_and_external_tools_pass_fail(self):
        self.assertFalse(check(fixture())[1])
        data=fixture(); data['topics'][0]['lab']['steps'][1]='```bash\nping 127.0.0.1 || true\n```'
        self.assertTrue(any('mask failures' in e for e in check(data)[0]))
        data['topics'][0]['lab']['steps'][0]='```bash\necho ready\n```'
        self.assertTrue(any('command -v' in w for w in check(data)[1]))
        data=fixture(); data['topics'][0]['lab']['steps'][7]='```bash\nkill 1 || true\n```'
        self.assertFalse(check(data)[0])

    def test_provenance_pass_fail(self):
        for word in ('proved','recorded','captured','observed'):
            data=fixture(); data['topics'][0]['scenario']={'facts':f'Illustrative log {word} failure.'}
            self.assertFalse(check(data)[1])
            data['topics'][0]['scenario']['facts']=f'Log {word} failure.'
            self.assertTrue(any('provenance' in w or 'observation language' in w for w in check(data)[1]))

    def test_embedded_caption_pass_fail(self):
        data=fixture(); data['technical']='<figure><figcaption>Illustrative log recorded errors.</figcaption></figure>'
        self.assertFalse(check(data)[1])
        data['technical']=data['technical'].replace('Illustrative ', '')
        self.assertTrue(any('figcaption[0]' in w for w in check(data)[1]))

    def test_address_pass_fail_and_allowlist(self):
        data=fixture(); data['text']='192.0.2.1 198.51.100.25 203.0.113.5 10.0.0.1 172.16.1.1 192.168.0.1 127.0.0.1 169.254.1.1 2001:db8::1 ::1 fe80::1'
        self.assertFalse(check(data)[1])
        for literal in ('35.200.10.5','2001:4860::8888'):
            data['text']=literal
            self.assertTrue(any(literal in w and 'spec.text' in w for w in check(data)[1]))
            self.assertFalse(check(data, allowlist=[literal])[1])

    def test_sources_pass_fail(self):
        self.assertEqual(check(fixture()), ([], []))
        data=fixture(); data['sources']['rfc']=('Status accessed 2026-10-04','https://example.test/doc')
        errors,warnings=check(data)
        self.assertTrue(any('accessed YYYY' in e for e in errors))
        self.assertTrue(any('whole-document link' in w for w in warnings))

    def test_inline_source_label_pass_fail(self):
        data=fixture(); data['technical']='<a href="https://example.test/doc#status">Status (accessed 2026-10-04)</a>'
        self.assertFalse(check(data)[0])
        data['technical']=data['technical'].replace(' (accessed 2026-10-04)', '')
        self.assertTrue(any('source_label' in e for e in check(data)[0]))

    def test_coverage_pass_fail(self):
        row={'topic_key':'topic-01','publisher_url':'https://example.test/doc#status'}
        self.assertFalse(check(fixture(),[row])[1])
        row['publisher_url']='https://example.test/other'
        self.assertTrue(any('publisher_url' in w for w in check(fixture(),[row])[1]))

    def test_diagram_count_pass_fail_skip(self):
        from types import SimpleNamespace
        data=fixture()
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'spec.py'; path.write_text('x')
            old='<figure><svg role="img"><title>HTTP versions</title></svg></figure>'
            with patch('scripts.spec_v2_checks.subprocess.run',return_value=SimpleNamespace(stdout=old)):
                self.assertTrue(any('HTTP versions' in w for w in file_checks(4,data,path,Path(temp))))
                data['technical']=old
                self.assertFalse(file_checks(4,data,path,Path(temp)))
            with patch('scripts.spec_v2_checks.subprocess.run',side_effect=FileNotFoundError):
                self.assertTrue(any('skipped' in w for w in file_checks(4,data,path,Path(temp))))

    def test_size_pass_fail(self):
        from types import SimpleNamespace
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'spec.py'; path.write_text('x')
            with patch('scripts.spec_v2_checks.subprocess.run',return_value=SimpleNamespace(stdout='')):
                self.assertFalse(file_checks(4,fixture(),path,Path(temp)))
                path.write_text('x'*(100*1024+1))
                self.assertTrue(any('use directory form for revisions' in w for w in file_checks(4,fixture(),path,Path(temp))))

    def test_legacy_gating(self):
        data=fixture(); data.pop('contract_version'); data.pop('roadmap_practice'); data['topics'][0]['lab']['mode']='legacy'
        errors,warnings=check(data)
        self.assertFalse(errors)
        self.assertTrue(warnings)
