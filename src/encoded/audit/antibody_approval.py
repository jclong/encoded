from ..auditor import (
    AuditFailure,
    audit_checker,
)


@audit_checker('antibody_approval')
def audit_target_match(value, system):
    '''Antibody characterization and antibody approval targets should match'''
    if value['status'] == 'deleted':
        # Don't worry about checking if approval is deleted
        return

    if not value['characterizations']:
        # Don't worry about checking if there are no characterizations to check
        return

    for char in value['characterizations']:
        char_target = char['target']
        approv_target = value['target']

        # Check if approval and characterization targets match
        if approv_target['label'] != char_target['label']:
            detail = 'Target {} and {} mismatch'.format(approv_target['label'], char_target['label'])
            yield AuditFailure('target mismatch', detail, level='ERROR')
            continue

        char_organism = char_target['organism']
        approv_organism = approv_target['organism']

        # Check if approval and characterization targets are in the same organism
        if approv_organism['name'] != char_organism['name']:
            detail = 'Organism target {} and {} mismatch'.format(approv_organism['name'], char_organism['name'])
            yield AuditFailure('target organism mismatch', detail, level='ERROR')
            continue