def build_columns_query_str(columns):
    """
    columns is a list of column name
    columns = ['foo', 'bar', 'baz']
    returns:
    "columns=foo&columns=bar&columns=baz"
    """
    query_str = map(lambda x: 'columns={}'.format(x), columns)
    return '&'.join(query_str)
