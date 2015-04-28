from ..schema_utils import (
    load_schema,
)
from ..contentbase import (
    calculated_property,
    collection,
)
from .base import (
    Item,
    paths_filtered_by_status,
)


@collection(
    name='libraries',
    unique_key='accession',
    properties={
        'title': 'Libraries',
        'description': 'Libraries used in the ENCODE project',
    })
class Library(Item):
    item_type = 'library'
    schema = load_schema('library.json')
    name_key = 'accession'
    embedded = [
        'biosample',
        'biosample.submitted_by',
        'biosample.source',
        'biosample.organism',
        'biosample.treatments',
        'biosample.donor.organism',
        'biosample.donor.mutated_gene',
        'documents',
        'documents.lab',
        'documents.submitted_by',
        'documents.award',
    ]

    @calculated_property(condition='nucleic_acid_term_name', schema={
        "title": "Nucleic acid ID",
        "type": "string",
    })
    def nucleic_acid_term_id(self, nucleic_acid_term_name):
        if nucleic_acid_term_name is not None:
            mapping = {
                "DNA": "SO:0000352",
                "RNA": "SO:0000356",
                "polyadenylated mRNA": "SO:0000871",
                "miRNA": "SO:0000276"
            }
            return mapping[nucleic_acid_term_name]

    @calculated_property(condition='depleted_in_term_name', schema={
        "title": "Depleted in ID",
        "type": "string",
    })
    def depleted_in_term_id(self, depleted_in_term_name):
        if depleted_in_term_name is not None:
            mapping = {
                "rRNA": "SO:0000252",
                "polyadenylated mRNA": "SO:0000871",
                "capped mRNA": "SO:0000862"
            }
            return mapping[depleted_in_term_name]
