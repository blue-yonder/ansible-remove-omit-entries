OMIT_MARKER = '__designated_omit_marker_that_results_in_deletion_of_the_corresponding_entry_in_dict_or_item_in_list'


def remove_omit_entries(thing, omit_marker=OMIT_MARKER):
    """
    Removes dict entries whose value is OMIT_MARKER:
    >>> remove_omit_entries({'key1': 'some_value', 'key2': OMIT_MARKER})
    {'key1': 'some_value'}

    Removes list items whose value is OMIT_MARKER:
    >>> remove_omit_entries([OMIT_MARKER])
    []

    Works recursively:
    >>> remove_omit_entries({'key1': {'key11': OMIT_MARKER}})
    {'key1': {}}

    Returns everything else as is:
    >>> remove_omit_entries('')
    ''
    >>> remove_omit_entries({OMIT_MARKER: 'some_value'}) == {OMIT_MARKER: 'some_value'}
    True
    >>> remove_omit_entries(OMIT_MARKER) == OMIT_MARKER
    True
    """
    if isinstance(thing, dict):
        cleaned = {}
        for key, value in thing.items():
            if isinstance(value, list) or isinstance(value, dict):
                cleaned[key] = remove_omit_entries(value)
            elif value != omit_marker:
                cleaned[key] = value
        return cleaned
    elif isinstance(thing, list):
        cleaned = []
        for item in thing:
            if item != omit_marker:
                cleaned.append(remove_omit_entries(item))
        return cleaned
    else:
        return thing


def remove_omit_entries_get_marker(arg):
    return OMIT_MARKER


class FilterModule(object):

    def filters(self):
        return dict(remove_omit_entries=remove_omit_entries, remove_omit_entries_get_marker=remove_omit_entries_get_marker)

