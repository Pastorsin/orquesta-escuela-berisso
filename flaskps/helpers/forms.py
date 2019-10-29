def not_empty_fields(form):
    fields = form.values()
    return all(fields)


def empty_fields(form):
    return not not_empty_fields(form)
