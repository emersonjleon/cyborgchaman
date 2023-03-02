# Here I learned how to add new columns to the database
import sqlalchemy
import sqlalchemy.ext.declarative
# from mynewapp import app, db, User, Sesion, 



#print(dir(insp))
#help(insp)

#this worked fine but created a numeric column instead of string field
#engine.execute('alter table historia add column image_link String')

#ths has not yet worked...
#engine.execute('alter table historia drop image_link')


def addColumn(column, engine, table_name):
    column_name = column.compile(dialect=engine.dialect)
    column_type = column.type.compile(engine.dialect)
    engine.execute(f'ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}')


if __name__=='__main__':
    #This is useful to inspect the database
    from sqlalchemy import create_engine, inspect
    
    engine = create_engine("sqlite:///quickstart_app.sqlite")
    insp = inspect(engine)
    print(insp.get_table_names())

    # This is one table in our engine
    table_name='historia'
    
    # This is the column we want to add: 
    column = sqlalchemy.Column('image_link', sqlalchemy.String(500), primary_key=False)
    # Here we add it:
    addColumn(column, engine, table_name)

    # Here we check that everything went fine
    for col in insp.get_columns(table_name):
        print(col)
    






##################
# [SQL: ALTER TABLE historia ADD COLUMN prompt_tokens INTEGER NOT NULL]

# Original problem:

#sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such column: historia.image_link
# [SQL: SELECT historia.id AS historia_id, historia.titulo AS historia_titulo, historia.autor AS historia_autor, historia."AIinspiration" AS "historia_AIinspiration", historia.prompt AS historia_prompt, historia.tokens_usados AS historia_tokens_usados, historia.prompt_tokens AS historia_prompt_tokens, historia.historia AS historia_historia, historia.fecha AS historia_fecha, historia.image_link AS historia_image_link, historia.sesion_id AS historia_sesion_id
# FROM historia]


