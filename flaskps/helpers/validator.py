from abc import ABC, abstractmethod, abstractproperty


class Validator(ABC):

    @abstractmethod
    def validate(self):
        pass

    @abstractproperty
    def message(self):
        pass


class EmptyFieldsValidator(Validator):

    def __init__(self, form):
        self.fields = form

    def validate(self):
        return all(self.fields.values())

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

    @abstractproperty
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
