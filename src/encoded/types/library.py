from contentbase.schema_utils import (
    load_schema,
)
from contentbase import (
    calculated_property,
    collection,
)
from .base import (
    Item,
    paths_filtered_by_status,
)


@collection(
    name='libraries',
    properties={
        'title': 'Libraries',
        'description': 'Listing of Libraries',
    })
class Library(Item):
    item_type = 'library'
    schema = load_schema('library.json')
    name_key = 'accession'
    embedded = ['biosample']

    @calculated_property(condition='nucleic_acid_term_name', schema={
        "title": "Nucleic acid ID",
        "type": "string",
    })
    def nucleic_acid_term_id(self, nucleic_acid_term_name):
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
    def depleted_in_term_id(self, depleted_in_term_name=None):
        if depleted_in_term_name is not None:
            mapping = {
                "rRNA": "SO:0000252",
                "polyadenylated mRNA": "SO:0000871",
                "capped mRNA": "SO:0000862"
            }
            term_ids = []
            for term_name in depleted_in_term_name:
                term_ids.append(mapping[term_name])

            return term_ids
