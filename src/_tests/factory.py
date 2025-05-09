from mimesis import Field, Fieldset, Generic, Person, Schema
from mimesis.builtins import RussiaSpecProvider
from mimesis.locales import Locale

generic = Generic(locale=Locale.RU)
field = Field(locale=Locale.RU)
fieldset = Fieldset(locale=Locale.RU)
russia = RussiaSpecProvider()
person = Person(locale=Locale.RU)


class FixtureFactory:
    def __init__(self) -> None:
        self.generic = generic
        self.field = field
        self.fieldset = fieldset
        self.schema = Schema
        self.russia = russia
        self.person = person
