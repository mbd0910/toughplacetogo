from enum import StrEnum

class ExternalSource(StrEnum):
    FOOTBALL_DATA = 'football-data.co.uk'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

class Gender(StrEnum):
    MALE = 'male'
    FEMALE = 'female'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

class TeamType(StrEnum):
    CLUB = 'club'
    NATIONAL = 'national'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

class CompetitionType(StrEnum):
    DOMESTIC = 'domestic'
    CLUB_INTERNATIONAL = 'club_international'
    NATIONAL = 'national'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

class TeamExternalLinkType(StrEnum):
    ID = 'id'
    URL = 'url'
    NAME = 'name'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
