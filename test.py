from datetime import datetime
from config import db 
from models.type import Type
from models.sea import Sea
from models.crew import Crew
from models.devil_fruit import Devil_Fruit
from models.enums import Fruit_types  # Asegúrate de tener acceso a tu enumeración

def create_sample_data():
    # Crear instancias de tipos
    type1 = Type(type=Fruit_types.Zoan, description='Type 1 Description')
    type2 = Type(type=Fruit_types.Paramecia, description='Type 2 Description')

    # Crear instancias de mares
    sea1 = Sea(name='East Blue')
    sea2 = Sea(name='Grand Line')

    # Crear instancias de tripulaciones
    crew1 = Crew(name='Straw Hat Pirates')
    crew2 = Crew(name='Blackbeard Pirates')

    # Crear instancias de frutas del diablo
    devil_fruit1 = Devil_Fruit(
        id_type=type1.id_type,
        name='Gomu Gomu no Mi',
        description='A rubber-based Devil Fruit',
    )
    devil_fruit2 = Devil_Fruit(
        id_type=type2.id_type,
        name='Bara Bara no Mi',
        description='A chopping-based Devil Fruit',
    )

    # Agregar instancias a la sesión y realizar la transacción
    with db.session.begin():
        db.session.add_all([type1, type2, sea1, sea2, crew1, crew2, devil_fruit1, devil_fruit2])

if __name__ == '__main__':
    # Ejecutar la función si este script es ejecutado directamente
    create_sample_data()


"""
CREATE OR REPLACE VIEW public.get_devil_fruits
 AS
 SELECT dv.id_devil_fruit,
    t.type,
    dv.name,
    dv.description,
    dv.created_at,
    dv.updated_at
   FROM devil_fruits dv
     JOIN types t ON t.id_type = dv.id_type;

ALTER TABLE public.get_devil_fruits
    OWNER TO postgres;

-- FUNCTION: public.get_devil_fruit(integer)

-- DROP FUNCTION IF EXISTS public.get_devil_fruit(integer);

CREATE OR REPLACE FUNCTION public.get_devil_fruit(pid_devil_fruit integer)
    RETURNS TABLE(type fruit_type, name character varying, description character varying) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
BEGIN
    RETURN QUERY
    SELECT  DF.type, DF.name, DF.description
	FROM get_devil_fruits DF
	WHERE DF.id_devil_fruit = pid_devil_fruit;
END;
$BODY$;

ALTER FUNCTION public.get_devil_fruit(integer)
    OWNER TO postgres;

INSERT INTO seas (name) VALUES
('East Blue'),
('West Blue'),
('North Blue'),
('South Blue'),
('Grand Line'),
('New World');


INSERT INTO crews (name) VALUES
('Straw Hat Pirates'),
('Red-Haired Pirates'),
('Whitebeard Pirates'),
('Big Mom Pirates'),
('Blackbeard Pirates'),
('Heart Pirates'),
('Kid Pirates'),
('Sun Pirates'),
('Roger Pirates'),
('Donquixote Pirates'),
('Kuja Pirates'),
('Beasts Pirates'),
('Hawkins Pirates'),
('Drake Pirates');

INSERT INTO types (type, description) VALUES
  ('Zoan', 'Devil fruit that grants the ability to transform into animals.'),
  ('Zoan Ancient', 'Ancient devil fruit that bestows transformations into extinct animals.'),
  ('Zoan Mythical', 'Mythical devil fruit that allows transformations into mythical creatures.'),
  ('Paramecia', 'Devil fruit that grants special abilities but no physical transformations.'),
  ('Logia', 'Devil fruit that grants control and transformation into natural substances.'),
  ('Undetermined', 'Type of devil fruit whose properties have not been fully determined.');

INSERT INTO devil_fruits (id_type, name, description)
VALUES
  (1, 'Gomu Gomu no Mi', 'Grants the ability to stretch one''s body like rubber.'),
(4, 'Mera Mera no Mi', 'Grants the ability to control and become fire.'),
  (2, 'Hito Hito no Mi, Model: Daibutsu', 'Allows the consumer to transform into a Daibutsu (Buddha).'),
  (5, 'Gura Gura no Mi', 'Grants the ability to create earthquakes and tremors.'),
  (3, 'Zushi Zushi no Mi', 'Allows the consumer to manipulate gravity at will.'),
  (6, 'Bara Bara no Mi', 'Grants the ability to split one''s body into separate pieces.'),
  (1, 'Goro Goro no Mi', 'Grants the ability to create, control, and transform into electricity.'),
  (4, 'Magu Magu no Mi', 'Allows the consumer to create, control, and transform into magma.'),
  (2, 'Ushi Ushi no Mi, Model: Bison', 'Allows the consumer to transform into a bison.'),
  (5, 'Bomu Bomu no Mi', 'Grants the ability to create and control explosions.');
"""
