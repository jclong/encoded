import pytest


@pytest.fixture
def base_award(testapp):
    item = {
        'name': 'U54HG006991',
        'rfa': 'ENCODE3'
    }
    return testapp.post_json('/awards', item, status=201).json['@graph'][0]


@pytest.fixture
def unapproved_characterization_method(testapp, lab, base_award, target, antibody_lot):
    item = {
        'award': base_award['uuid'],
        'characterization_method': 'motif enrichment',
        'target': target['uuid'],
        'lab': lab['uuid'],
        'characterizes': antibody_lot['uuid']
    }
    return testapp.post_json('/antibody-characterizations', item, status=201).json['@graph'][0]


def test_audit_characterization_method(testapp, unapproved_characterization_method):
    res = testapp.get(unapproved_characterization_method['@id'] + '@@index-data')
    error, = res.json['audit']
    assert error['category'] == 'unapproved method'