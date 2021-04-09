from django_enumfield.enum import Enum as DjangoEnum


class RoomTypes(DjangoEnum):
    STUDIO = 1
    BEDROOM1 = 2
    BEDROOM2 = 3
    BEDROOM3 = 4
    
    __labels__ = {
        STUDIO: 'Studio',
        BEDROOM1: '1 Bedroom',         
        BEDROOM2: '2 Bedrooms',         
        BEDROOM3: '3 Bedrooms',         
    }


class GainEntry(DjangoEnum):
    WE = 1
    DOORMAN = 2
    OTHER = 3

    __labels__ = {
        WE: 'We will let you in',
        DOORMAN: 'Doorman will give access',
        OTHER: 'Other (Include specifics in the comment section below)'
    }

class Pets(DjangoEnum):
    NO = 1
    DOG = 2
    CAT = 3

    __labels__ = {
        DOG: 'Dog',
        CAT: 'Cat',
        NO: 'No pets'
    }

class CovidExposure(DjangoEnum):

    NO = 1
    YES = 2
    CALL = 3

    __labels__ = {
        YES: 'Yes',
        NO: 'No',
        CALL: 'Give me a call'
    }
