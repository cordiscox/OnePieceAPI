from config import db
from enum import Enum

fruit_types = ('Zoan', 'Zoan Ancient', 'Zoan Mythical', 'Zoan Artificial', 'Paramecia', 'Logia', 'Undetermined')
marine_positions = ('Fleet Admiral', 'Admiral', 'Vice Admiral', 'Rear Admiral', 'Commodore',
        'Captain', 'Commander', 'Lieutenant Commander', 'Lieutenant', 'Lieutenant Junior Grade',
        'Ensign', 'Warrant Officer', 'Master Chief Petty Officer', 'Chief Petty Officer',
        'Petty Officer', 'Seaman First Class', 'Seaman Apprentice', 'Seaman Recruit',
        'Chore Boy', 'Inspector General', 'Instructor', 'Undetermined')
statuses = ('Alive', 'Dead', 'Undetermined')

#Then I will create a skill_level_enum variable and assign it an ENUM class with the skill level values as args.#

fruit_types_enum = db.Enum(*fruit_types, name="fruit_type")
marine_positions_enum = db.Enum(*marine_positions, name="marine_position")
statuses_enum = db.Enum(*statuses, name="status")


class Statuses(Enum):
    Alive = 'Alive'
    Dead = 'Dead'
    Undetermined = 'Undetermined'


''' EXAMPLE HOW YOU ADD ENUM IN YOUR MODEL
import emuns

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    fruit_type = db.Column(fruit_type)

'''