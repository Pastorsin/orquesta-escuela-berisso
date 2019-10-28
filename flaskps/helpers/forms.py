def not_empty_fields(form):
    fields = form.values()
    return all(fields)
