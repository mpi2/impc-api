from .utils.validators import ValidationJson


def get_core_fields(core: str) -> list[str]:
    """Return the documented fields available for an IMPC Solr core.

    Args:
        core: Name of a public IMPC Solr core.

    Returns:
        The documented field names, or an empty list when ``core`` is unknown.
    """
    return ValidationJson().valid_fields(core)
