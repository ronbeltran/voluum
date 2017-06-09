from urllib.parse import quote_plus


def build_query_str(columns):
    """
    columns is a list of column name
    columns = ['foo', 'bar', 'baz']
    returns:
    "columns=foo&columns=bar&columns=baz"
    """
    if not isinstance(columns, (list, tuple)):
        return ''
    query_str = map(lambda x: 'columns={}'.format(
                    quote_plus(str(x).encode('utf-8'))), columns)
    return '&'.join(query_str)
