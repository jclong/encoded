import pytest


@pytest.fixture
def base_award(testapp):
    item = {
        'name': 'U54HG006991',
        'rfa': 'ENCODE3'
    }
    return testapp.post_json('/awards', item, status=201).json['@graph'][0]


@pytest.fixture
def organism1(testapp):
    item = {
        'name': 'opossum',
        'taxon_id': '13616'
    }
    return testapp.post_json('/organism', item, status=201).json['@graph'][0]


@pytest.fixture
def organism2(testapp):
    item = {
        'name': 'woollyflyingsquirrel',
        'taxon_id': '226699'
    }
    return testapp.post_json('/organism', item, status=201).json['@graph'][0]


@pytest.fixture
def target1(testapp, organism1):
    item = {
        'label': 'H3K4me3',
        'organism': organism1['uuid']
    }
    return testapp.post_json('/target', item, status=201).json['@graph'][0]


@pytest.fixture
def target2(testapp, organism2):
    item = {
        'label': 'H3K4me3',
        'organism': organism2['uuid']
    }
    return testapp.post_json('/target', item, status=201).json['@graph'][0]


@pytest.fixture
def target3(testapp, organism1):
    item = {
        'label': 'H3K9ac',
        'organism': organism1['uuid']
    }
    return testapp.post_json('/target', item, status=201).json['@graph'][0]


@pytest.fixture
def characterization1(testapp, lab, base_award, target1, antibody_lot):
    item = {
        'award': base_award['uuid'],
        'target': target1['uuid'],
        'lab': lab['uuid'],
        'characterizes': antibody_lot['uuid'],
        'characterization_method': 'immunoblot',
        'status': 'pending dcc review'
    }
    return testapp.post_json('/antibody-characterizations', item, status=201).json['@graph'][0]


@pytest.fixture
def characterization2(testapp, lab, base_award, target2, antibody_lot):
    item = {
        'award': base_award['uuid'],
        'target': target2['uuid'],
        'lab': lab['uuid'],
        'characterizes': antibody_lot['uuid'],
        'characterization_method': 'dot blot assay',
        'status': 'not compliant'
    }
    return testapp.post_json('/antibody-characterizations', item, status=201).json['@graph'][0]


@pytest.fixture
def characterization3(testapp, lab, base_award, target3, antibody_lot):
    item = {
        'award': base_award['uuid'],
        'target': target3['uuid'],
        'lab': lab['uuid'],
        'characterizes': antibody_lot['uuid'],
        'characterization_method': 'motif enrichment',
        'status': 'not compliant'
    }
    return testapp.post_json('/antibody-characterizations', item, status=201).json['@graph'][0]
 

@pytest.fixture
def base_approval(testapp, base_award, lab, target1, antibody_lot):
    item = {
        'award': base_award['uuid'],
        'lab': lab['uuid'],
        'antibody': antibody_lot['uuid'],
        'status': 'pending dcc review',
        'target': target1['uuid']
    }
    return testapp.post_json('/antibodies', item, status=201).json['@graph'][0]


def test_audit_approval_target(testapp, characterization1, characterization3, base_approval):
    testapp.patch_json(base_approval['@id'], {'characterizations': [characterization1['uuid'], characterization3['uuid']]})
    res = testapp.get(base_approval['@id'] + '@@index-data')
    errors = res.json['audit']
    assert any(error['category'] == 'target mismatch' for error in errors)


def test_audit_approval_target_organism(testapp, characterization1, characterization2, base_approval):
    testapp.patch_json(base_approval['@id'], {'characterizations': [characterization1['uuid'], characterization2['uuid']]})
    res = testapp.get(base_approval['@id'] + '@@index-data')
    errors = res.json['audit']
    assert any(error['category'] == 'target organism mismatch' for error in errors)


def test_audit_approval_no_primary(testapp, base_approval, characterization2):
    testapp.patch_json(base_approval['@id'], {'characterizations': [characterization2['uuid']]})
    res = testapp.get(base_approval['@id'] + '@@index-data')
    print "%s" % res.json
    errors = res.json['audit']
    assert any(error['category'] == 'no compliant characterzation 1' for error in errors)


def test_audit_approval_no_secondary(testapp, base_approval, characterization1):
    testapp.patch_json(base_approval['@id'], {'characterizations': [characterization1['uuid']]})
    res = testapp.get(base_approval['@id'] + '@@index-data')
    errors = res.json['audit']
    assert any(error['category'] == 'no compliant characterization 2' for error in errors)