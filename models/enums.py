from config import db
from enum import Enum

#Then I will create a skill_level_enum variable and assign it an ENUM class with the skill level values as args.#
class Statuses(Enum):
    Alive = 'Alive'
    Dead = 'Dead'
    Undetermined = 'Undetermined'

    @classmethod
    def Statuses(cls):
        return ('Alive', 'Dead', 'Undetermined')
    

class Fruit_types(Enum):
    Zoan = 'Zoan'
    Zoan_Ancient = 'Zoan Ancient'
    Zoan_Mythical = 'Zoan Mythical'
    Paramecia = 'Paramecia'
    Logia = 'Logia'
    Undetermined = 'Undetermined'

    @classmethod
    def Fruit_types(cls):
        return ('Zoan', 'Zoan Ancient', 'Zoan Mythical', 'Zoan Artificial', 'Paramecia', 'Logia', 'Undetermined')


class Marine_positions(Enum):
    Fleet_Admiral = 'Fleet Admiral'
    Admiral = 'Admiral'
    Vice_Admiral = 'Vice Admiral'
    Rear_Admiral = 'Rear Admiral'
    Commodore = 'Commodore'
    Captain = 'Captain' 
    Commander = 'Commander'
    Lieutenant_Commander = 'Lieutenant Commander'
    Lieutenant = 'Lieutenant'
    Lieutenant_Junior_Grade = 'Lieutenant Junior Grade'
    Ensign = 'Ensign'
    Warrant_Officer = 'Warrant Officer'
    Master_Chief_Petty_Officer = 'Master Chief Petty Officer'
    Chief_Petty_Officer = 'Chief Petty Officer'
    Petty_Officer = 'Petty Officer'
    Seaman_First_Class = 'Seaman First Class'
    Seaman_Apprentice = 'Seaman Apprentice'
    Seaman_Recruit = 'Seaman Recruit'
    Chore_Boy = 'Chore Boy'
    Inspector_General = 'Inspector General'
    Instructor = 'Instructor'
    Undetermined = 'Undetermined'

    @classmethod
    def Marine_positions(cls):
        return ('Fleet Admiral', 'Admiral', 'Vice Admiral', 'Rear Admiral', 'Commodore','Captain', 
                'Commander', 'Lieutenant Commander', 'Lieutenant', 'Lieutenant Junior Grade',
                'Ensign', 'Warrant Officer', 'Master Chief Petty Officer', 'Chief Petty Officer',
                'Petty Officer', 'Seaman First Class', 'Seaman Apprentice', 'Seaman Recruit',
                'Chore Boy', 'Inspector General', 'Instructor', 'Undetermined')
 
fruit_types_enum = db.Enum(*Fruit_types.Fruit_types(), name="fruit_type")
marine_positions_enum = db.Enum(*Marine_positions.Marine_positions(), name="marine_position")
statuses_enum = db.Enum(*Statuses.Statuses(), name="status")