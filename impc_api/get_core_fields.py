from .utils.validators import ValidationJson


def get_core_fields(core: str) -> list[str]:
    """Return the documented fields available for an IMPC Solr core.

    Fields are read from the same source of truth used to validate requests.
    This function does not make a request to the IMPC Solr API.

    Args:
        core: Name of a public IMPC Solr core.

    Returns:
        The documented field names, or an empty list when ``core`` is unknown.

    Example:
        >>> from impc_api import get_core_fields
        >>> fields = get_core_fields("genotype-phenotype")
        >>> fields[:3]
        ['doc_id', 'ontology_db_id', 'assertion_type']
    """
    return ValidationJson().valid_fields(core)
