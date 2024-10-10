from enum import StrEnum

class ExternalSource(StrEnum):
    FOOTBALL_DATA = 'football-data.co.uk'
    UNDERSTAT = 'Understat'
    FOT_MOB = 'FotMob'

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

class GameExternalLinkType(StrEnum):
    ID = 'id'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

class GameStatus(StrEnum):
    FINISHED = 'finished'
    ABANDONED = 'abandoned'
    FORFEIT = 'forfeit'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

class FantasyFootballProvider(StrEnum):
    FPL = 'fpl'
    EFL = 'efl'
    FANTRAX = 'fantrax'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

class GameweekType(StrEnum):
    SINGLE = 'single'
    DOUBLE = 'double'
    TRIPLE = 'triple'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]