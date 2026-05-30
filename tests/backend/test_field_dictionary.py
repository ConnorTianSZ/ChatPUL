from app.backend.chatbi.field_dictionary import (
    FIELD_DICTIONARY,
    FILTER_FIELD_NAMES,
    GROUP_BY_FIELD_NAMES,
    RESULT_FIELD_NAMES,
)


def test_every_exposed_chatbi_field_has_tooltip_ready_metadata():
    exposed_fields = set(FILTER_FIELD_NAMES) | set(GROUP_BY_FIELD_NAMES) | set(RESULT_FIELD_NAMES)

    missing = sorted(field_name for field_name in exposed_fields if field_name not in FIELD_DICTIONARY)
    assert missing == []

    for field_name in exposed_fields:
        entry = FIELD_DICTIONARY[field_name]
        assert entry.field_name == field_name
        assert entry.source_header
        assert entry.business_label
        assert entry.data_type
        assert entry.meaning
        assert entry.allowed_usages
        assert entry.result_label
        assert entry.source_trace_label


def test_sensitive_commercial_fields_are_not_default_result_fields():
    assert "net_price" not in RESULT_FIELD_NAMES
    assert "net_value_domestic_currency" not in RESULT_FIELD_NAMES

