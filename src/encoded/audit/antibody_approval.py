from ..auditor import (
    AuditFailure,
    audit_checker,
)


@audit_checker('antibody_approval')
def audit_target_match(value, system):
    '''Antibody characterization and antibody approval targets should match'''
    if value['status'] in ['not pursued', 'deleted', 'not eligible for new data']:
        # Don't worry about checking if approval unless it is active
        return

    if not value['characterizations']:
        # Don't worry about checking if there are no characterizations to check
        return

    for char in value['characterizations']:
        char_target = char['target']
        approv_target = value['target']

        # Check if approval and characterization targets match
        if approv_target['@id'] != char_target['@id']:
            detail = 'Target {} and {} mismatch'.format(approv_target['@id'], char_target['@id'])
            yield AuditFailure('target mismatch', detail, level='ERROR')


@audit_checker('antibody_approval')
def audit_fully_characterized(value, system):
    '''Antibodies should have at least one compliant primary and at least one compliant secondary characterization'''
    if value['status'] in ['deleted', 'not pursued']:
        # Don't worry about doing this check on non active approval
        return

    characterization_types = []
    for char in value['characterizations']:
        if (char['characterization_method'] in ['immunoblot', 'immunoprecipitation', 'immunofluorescence']) and (char['status'] == 'compliant'):
            characterization_types.append('primary')
        elif (char['characterization_method'] in ['dot blot assay', 'knockdown or knockout', 'ChIP-seq comparison', 'peptide array assay', 'peptide ELISA assay', 'peptide competition assay', 'immunoprecipitation followed by mass spectrometry', 'overexpression assay']) and (char['status'] == 'compliant'):
            characterization_types.append('secondary')
        else:
            # ignore any other characterization_method
            pass

    if characterization_types.count('primary') < 1:
        detail = 'No primary characterization'
        yield AuditFailure('no compliant characterization 1', detail, level='WARNING')

    if characterization_types.count('secondary') < 1:
        detail = 'No secondary characterization'
        yield AuditFailure('no compliant characterization 2', detail, level='WARNING')
