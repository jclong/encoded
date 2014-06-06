from ..auditor import (
    AuditFailure,
    audit_checker,
)


@audit_checker('antibody_characterization')
def audit_unapproved_method(value, system):
    '''Only approved characterization methods in the standard can be used'''
    award = value['award']
    if (value['characterization_method'] in ['annotation enrichment', 'motif enrichment', 'mutant organism', 'mutant histone', 'mutant histone modifier']) and (award['rfa'] == 'ENCODE3'):
        detail = '{} is not an approved characterization method at this time'.format(value['characterization_method'])
        raise AuditFailure('unapproved method', detail, level='WARNING')