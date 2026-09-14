from impc_api import get_core_fields


def test_get_core_fields_returns_documented_fields():
    fields = get_core_fields("experiment")

    assert isinstance(fields, list)
    assert "observation_id" in fields
