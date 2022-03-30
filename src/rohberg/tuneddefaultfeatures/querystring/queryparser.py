# Query operators

def _exclude(context, row):
    return {row.index: {'not': row.values}}
