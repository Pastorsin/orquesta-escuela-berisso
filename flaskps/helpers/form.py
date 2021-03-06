from abc import ABC, abstractmethod, abstractproperty
import itertools


class Validator(ABC):

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def message(self):
        pass


class EmptyFieldsValidator(Validator):

    def __init__(self, form):
        self.fields = form

    def validate(self):
        return bool(self.fields) and all(self.fields.values())

    def message(self):
        return 'Error! Todos los campos son obligatorios.'


class Form(ABC):

    def __init__(self, form):
        self.fields = dict(form)
        self.validators = [EmptyFieldsValidator(self.fields)]

    def is_valid(self):
        return all(self.__validation_results())

    def __validation_results(self):
        return map(
            lambda validator: validator.validate(), self.validators
        )

    @abstractmethod
    def success_message(self):
        pass

    def error_messages(self):
        messages = map(
            lambda validator: validator.message(), self.__failed_validators()
        )
        return list(messages)

    def __failed_validators(self):
        return filter(
            lambda validator: not validator.validate(), self.validators
        )

    @abstractproperty
    def values(self):
        pass

    @classmethod
    def is_valid_forms(cls, forms):
        return all(cls.__validation_results_forms(forms))

    @classmethod
    def __validation_results_forms(cls, forms):
        return map(lambda form: form.is_valid(), forms)

    @classmethod
    def build_forms(cls, form_data):
        forms = [cls(data) for data in form_data]
        return forms

    @classmethod
    def invalid_messages(cls, forms):
        messages = map(
            lambda form: form.error_messages(), cls.__invalid_forms(forms)
        )
        flat_messages = set(itertools.chain(*messages))
        return list(flat_messages)

    @classmethod
    def __invalid_forms(cls, forms):
        return filter(lambda form: not form.is_valid(), forms)

    @classmethod
    def save(self, forms):
        return list(map(lambda form: form.save(), forms))
