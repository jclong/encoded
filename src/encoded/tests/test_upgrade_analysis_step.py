import pytest


@pytest.fixture
def analysis_step(software_version):
    return {
        'name': 'align-star-pe-v-1-0',
        'title': 'Title',
        'schema_version': '2',
        'software_versions': [
        ],
        'analysis_step_types': [
            'alignment'
        ],
        'input_file_types': [
            'reads'
        ]
    }


def test_analysis_step_upgrade_1(app, analysis_step):
    migrator = app.registry['migrator']
    value = migrator.upgrade('analysis_step', analysis_step, '2', target_version='3')
    assert value['schema_version'] == '3'
    assert value['version']['major'] == 1
    assert value['version']['minor'] == 0
