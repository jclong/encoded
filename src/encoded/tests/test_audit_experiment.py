import pytest


@pytest.fixture
def base_experiment(testapp, lab, award):
    item = {
        'award': award['uuid'],
        'lab': lab['uuid']
    }
    return testapp.post_json('/experiment', item, status=201).json['@graph'][0]


@pytest.fixture
def base_biosample(testapp, lab, award, source, organism):
    item = {
        'award': award['uuid'],
        'biosample_term_id': 'UBERON:349829',
        'biosample_type': 'tissue',
        'lab': lab['uuid'],
        'organism': organism['uuid'],
        'source': source['uuid']
    }
    return testapp.post_json('/biosample', item, status=201).json['@graph'][0]


@pytest.fixture
def base_library(testapp, lab, award):
    item = {
        'award': award['uuid'],
        'lab': lab['uuid'],
        'nucleic_acid_term_id': 'SO:0000352',
        'nucleic_acid_term_name': 'DNA',
    }
    return testapp.post_json('/library', item, status=201).json['@graph'][0]


@pytest.fixture
def base_antibody_lot(testapp, lab, award, organism, source):
    item = {
        'award': award['uuid'],
        'lab': lab['uuid'],
        'source': source['uuid'],
        'product_id': 'ab12345',
        'lot_id': '54321',
        'host_organism': organism['uuid']
    }
    return testapp.post_json('/antibody_lot', item, status=201).json['@graph'][0]


@pytest.fixture
def base_replicate1(testapp, base_experiment):
    item = {
        'biological_replicate_number': 1,
        'technical_replicate_number': 1,
        'experiment': base_experiment['@id']
    }
    return testapp.post_json('/replicate', item, status=201).json['@graph'][0]


@pytest.fixture
def base_replicate2(testapp, base_experiment):
    item = {
        'biological_replicate_number': 2,
        'technical_replicate_number': 1,
        'experiment': base_experiment['@id']
    }
    return testapp.post_json('/replicate', item, status=201).json['@graph'][0]    


@pytest.fixture
def fake_target(testapp, organism):
    item = {
        'label': 'faketarget',
        'organism': organism['uuid'],
        'gene_name': 'fake-o',
        'aliases': ['test:faketarget']
    }
    return testapp.post_json('/target', item, status=201).json['@graph'][0]


@pytest.fixture
def base_approval(testapp, award, lab, fake_target, base_antibody_lot):
    item = {
        'award': award['uuid'],
        'lab': lab['uuid'],
        'antibody': base_antibody_lot['uuid'],
        'status': 'pending dcc review',
        'target': fake_target['uuid']
    }
    return testapp.post_json('/antibodies', item, status=201).json['@graph'][0]


def test_audit_experiment_target(testapp, base_experiment):
    testapp.patch_json(base_experiment['@id'], {'assay_term_id': 'OBI:0000716', 'assay_term_name': 'ChIP-seq'})
    res = testapp.get(base_experiment['@id'] + '@@index-data')
    errors = res.json['audit']
    assert any(error['category'] == 'missing target' for error in errors)


def test_audit_experiment_replicate_paired_end(testapp, base_experiment, base_replicate1):
    res = testapp.get(base_experiment['@id'] + '@@index-data')
    errors = res.json['audit']
    assert any(error['category'] == 'missing replicate paired end' for error in errors)


def test_audit_experiment_library_paired_end(testapp, base_experiment, base_replicate1, base_library):
    testapp.patch_json(base_replicate1['@id'], {'library': base_library['@id']})
    res = testapp.get(base_experiment['@id'] + '@@index-data')
    errors = res.json['audit']
    assert any(error['category'] == 'missing library paired end' for error in errors)


def test_audit_experiment_paired_end_mismatch(testapp, base_experiment, base_replicate1, base_library):
    testapp.patch_json(base_library['@id'], {'paired_ended': False})
    testapp.patch_json(base_replicate1['@id'], {'library': base_library['@id'], 'paired_ended': True})
    res = testapp.get(base_experiment['@id'] + '@@index-data')
    errors = res.json['audit']
    assert any(error['category'] == 'paired end mismatch' for error in errors)


def test_audit_experiment_paired_end_required(testapp, base_experiment, base_replicate1, base_library):
    testapp.patch_json(base_experiment['@id'], {'assay_term_id': 'OBI:0001849', 'assay_term_name': 'DNA-PET'})
    testapp.patch_json(base_library['@id'], {'paired_ended': False})
    testapp.patch_json(base_replicate1['@id'], {'library': base_library['@id'], 'paired_ended': True})
    res = testapp.get(base_experiment['@id'] + '@@index-data')
    errors = res.json['audit']
    assert any(error['category'] == 'paired end required for assay' for error in errors)


def test_audit_experiment_antibody_in_replicate(testapp, experiment, target, base_replicate1, base_replicate2):
    testapp.patch_json(base_replicate1['@id'], {'biological_replicate_number': 1, 'technical_replicate_number': 1, 'experiment': experiment['@id']})
    testapp.patch_json(base_replicate2['@id'], {'biological_replicate_number': 2, 'technical_replicate_number': 1, 'experiment': experiment['@id']})
    testapp.patch_json(experiment['@id'], {'target': target['@id'], 'assay_term_id': 'OBI:0000716', 'assay_term_name': 'ChIP-seq'})
    res = testapp.get(experiment['@id'] + '@@index-data')
    errors = res.json['audit']
    assert any(error['category'] == 'missing antibody' for error in errors)


def test_audit_experiment_orphan_antibody_lot(testapp, base_experiment, base_replicate1, target, base_antibody_lot):
    testapp.patch_json(base_replicate1['@id'], {'antibody': base_antibody_lot['@id'], 'paired_ended': True})
    testapp.patch_json(base_experiment['@id'], {'target': target['@id'], 'assay_term_id': 'OBI:0000716', 'assay_term_name': 'ChIP-seq'})
    res = testapp.get(base_experiment['@id'] + '@@index-data')
    errors = res.json['audit']
    assert any(error['category'] == 'missing approval' for error in errors)


def test_audit_experiment_antibody_lot_mismatch(testapp, base_experiment, base_replicate1, base_replicate2, target, base_antibody_lot, antibody_lot, base_approval):
    testapp.patch_json(base_replicate1['@id'], {'antibody': antibody_lot['@id'], 'paired_ended': True})
    testapp.patch_json(base_replicate2['@id'], {'antibody': base_antibody_lot['@id'], 'paired_ended': True})
    testapp.patch_json(base_experiment['@id'], {'target': target['@id'], 'assay_term_id': 'OBI:0000716', 'assay_term_name': 'ChIP-seq'})
    res = testapp.get(base_experiment['@id'] + '@@index-data')
    errors = res.json['audit']
    print "%s" % res.json
    assert any(error['category'] == 'antibody mismatch' for error in errors)
