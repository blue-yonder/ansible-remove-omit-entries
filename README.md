# Ansible Role: remove-omit-entries

In a nutshell, this role gives you behavior similar to Ansible's `omit`,
but for dictionaries and lists instead of modules' parameters.

For this, the role defines two filters (`remove_omit_entries` and `remove_omit_entries_get_marker` [only used internally]) and one var (`remove_omit_entries_marker`).
The role itself does not run any tasks.

## Usage

- Add the role to the roles section of your playbook.
- Set `remove_omit_entries_marker` as a default value for entries that should be removed by the filter.
- Run dicts or lists through `remove_omit_entries` to remove entries having `remove_omit_entries_marker` as their value.

## Requirements and Dependencies

None

## Example

The need for the role arose from the inadequacy of Ansible's `omit` when passing dicts as modules' parameters.
`omit` can be used as default value for possibly undefined variables.
When passing parameters to modules, Ansible will not pass omitted parameters.

~~~
debug:
  # debug_msg will not be passed to the debug module if undefined
  msg: "{{ debug_msg|default(omit) }}"
~~~

However, this does not work for entries of dictionaries.
Ansible will pass the complete `error_info` dictionary to the `debug` module:

~~~
vars:
  error_info:
    code: 10
    reason: "{{ error_reason|default(omit) }}"
    
tasks:
  - debug:
      msg: error_info
~~~

This will print something like:

~~~
TASK [debug] ********************************************************************
ok: [localhost] => {
    "msg": {
        "code": 10,
        "reason": "__omit_place_holder__ab8264664a4f0a83fa01e9ee3f221d79acecefc8"
    }
}
~~~

To prevent the debug module from seeing the undefined `reason` entry of the `error_info` dictionary,
we can use the `remove-omit-entries-role`.

~~~
roles:
  # Include the remove-omit-entries role
  - role: remove-omit-entries
  
vars:
  error_info:
    code: 10
    # Use remove_omit_entries_marker as default value for possibly undefined values
    reason: "{{ error_reason|default(remove_omit_entries_marker) }}"

tasks:
  - debug:
      # Pass the dict through the remove_omit_entries filter
      msg: "{{ error_info|remove_omit_entries }}"
~~~

Now, the `debug` module will receive a dictionary that only contains the defined entry `code`.

~~~
TASK [debug] ********************************************************************
ok: [localhost] => {
    "msg": {
        "code": 10
    }
}
~~~

## Behavior of `remove_omit_entries` filter

Removes dict entries whose value is OMIT_MARKER:

~~~
>>> remove_omit_entries({'key1': 'some_value', 'key2': OMIT_MARKER})
{'key1': 'some_value'}
~~~

Removes list items whose value is OMIT_MARKER:
~~~
>>> remove_omit_entries([OMIT_MARKER])
[]
~~~

Works recursively:
~~~
>>> remove_omit_entries({'key1': {'key11': OMIT_MARKER}})
{'key1': {}}
~~~

Returns everything else as is:
~~~
>>> remove_omit_entries('')
''
>>> remove_omit_entries({OMIT_MARKER: 'some_value'}) == {OMIT_MARKER: 'some_value'}
True
>>> remove_omit_entries(OMIT_MARKER) == OMIT_MARKER
True
~~~

## License

MIT
