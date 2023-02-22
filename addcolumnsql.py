# when adding new columns to a database, we need to migrate. this is not a trivial
# procedure for me, so I needed here  to hack from sqlalchemy barebones, and see if I can go up to flask

import sqlalchemy
import sqlalchemy.ext.declarative

# from mynewapp import app, db, User, Sesion, 
from sqlalchemy import create_engine, inspect
engine = create_engine("sqlite:///quickstart_backup.sqlite")
insp = inspect(engine)
print(insp.get_table_names())
#metadata.reflect(engine)

# object_methods = [method_name for method_name in dir(insp)
#                   if callable(getattr(object, method_name))]

#print(object_methods)

#print(dir(insp))
#help(insp)

#this worked fine but created a numeric column instead of string field
#engine.execute('alter table historia add column image_link String')

#engine.execute('alter table historia add column image_link String')


#Base = sqlalchemy.ext.declarative.declarative_base()

column = sqlalchemy.Column('image_link', sqlalchemy.String(500), primary_key=False)
column_name = column.compile(dialect=engine.dialect)
column_type = column.type.compile(engine.dialect)
engine.execute(f'ALTER TABLE historia ADD COLUMN {column_name} {column_type}')

#ths has not yet worked...
#engine.execute('alter table historia drop image_link')

for col in insp.get_columns("historia"):
    print(col)
    
# [SQL: ALTER TABLE historia ADD COLUMN prompt_tokens INTEGER NOT NULL]

#sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such column: historia.image_link
# [SQL: SELECT historia.id AS historia_id, historia.titulo AS historia_titulo, historia.autor AS historia_autor, historia."AIinspiration" AS "historia_AIinspiration", historia.prompt AS historia_prompt, historia.tokens_usados AS historia_tokens_usados, historia.prompt_tokens AS historia_prompt_tokens, historia.historia AS historia_historia, historia.fecha AS historia_fecha, historia.image_link AS historia_image_link, historia.sesion_id AS historia_sesion_id
# FROM historia]

#finally it seems to work! although didn't make it to the final file...
