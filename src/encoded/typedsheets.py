from pyramid.settings import asbool


def parse_array(value):
    return [v.strip() for v in value.decode('utf-8').split(';') if v.strip()]


def decode_utf8(value):
    return value.decode('utf-8')


def ignore(value):
    return None


def parse_number(value):
    try:
        return int(value)
    except ValueError:
        return float(value)


TYPE_BY_NAME = {
    'string': decode_utf8,
    'number': parse_number,
    'boolean': asbool,
    'integer': int,
    'array': parse_array,
    'ignore': ignore,
}


def convert(name, value):
    """ fieldname:<cast>, value -> fieldname, cast(value)
    """
    parts = name.rsplit(':', 1)
    name = parts[0]
    if len(parts) == 2:
        type_name = parts[1]
    else:
        type_name = 'string'
    if value.lower() == 'null':
        return name, None
    if type_name != 'string' and value == '':
        return name, None
    cast = TYPE_BY_NAME[type_name]
    value = cast(value)
    return name, value


def cast_rows(dictrows):
    """ Wrapper generator for typing csv.DictReader rows
    """
    for row in dictrows:
        yield dict(convert(name, value) for name, value in row.iteritems())


def remove_nulls(dictrows):
    for row in dictrows:
        row = dict(
            (name, value) for name, value in row.iteritems()
            if value is not None and name
        )
        if row:
            yield row
