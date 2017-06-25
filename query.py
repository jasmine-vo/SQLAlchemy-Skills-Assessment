"""

This file is the place to write solutions for the
skills assignment called skills-sqlalchemy. Remember to
consult the exercise instructions for more complete
explanations of the assignment.

All classes from model.py are being imported for you
here, so feel free to refer to classes without the
[model.]User prefix.

"""

from model import *

init_app()


# -------------------------------------------------------------------
# Part 2: Discussion Questions


# 1. What is the datatype of the returned value of
# ``Brand.query.filter_by(name='Ford')``?

"""
The datatype returned is flask_sqlalchemy.BaseQuery, which is a SQL query.

    In [13]: ford = Brand.query.filter_by(name='Ford')
    In [14]: type(ford)
    Out[14]: flask_sqlalchemy.BaseQuery
    In [15]: print ford
    SELECT brands.brand_id AS brands_brand_id, brands.name AS brands_name, brands.founded AS brands_founded, brands.headquarters AS brands_headquarters, brands.discontinued AS brands_discontinued 
    FROM brands 
    WHERE brands.name = :name_1
"""


# 2. In your own words, what is an association table, and what type of
# relationship (many to one, many to many, one to one, etc.) does an
# association table manage?

"""
An association table manages a many to many relationship between two
tables/classes.  For example, lets consider the two tables, Video Games
and Genre.  A video game can have multiple genres and a single genre can have
many video games.  The association table would have two columns referencing the
primary keys from the Video Game and Genre tables as foreign keys; game_id
and genre_id.  The association table allows us to link the two tables.
"""


# -------------------------------------------------------------------
# Part 3: SQLAlchemy Queries


# Get the brand with the brand_id of ``ram``.
q1 = Brand.query.filter_by(brand_id='ram').one()

# Get all models with the name ``Corvette`` and the brand_id ``che``.
q2 = Model.query.filter_by(name='Corvette', brand_id='che').all()

# Get all models that are older than 1960.
q3 = Model.query.filter(Model.year < 1960).all()

# Get all brands that were founded after 1920.
q4 = Brand.query.filter(Brand.founded > 1920).all()

# Get all models with names that begin with ``Cor``.
q5 = Model.query.filter(Model.name.like('Cor%')).all()

# Get all brands that were founded in 1903 and that are not yet discontinued.
q6 = Brand.query.filter_by(founded=1903, discontinued=None).all()

# Get all brands that are either 1) discontinued (at any time) or 2) founded
# before 1950.
q7 = Brand.query.filter((Brand.discontinued!=None) | (Brand.founded<1950)).all()

# Get all models whose brand_id is not ``for``.
q8 = Model.query.filter(Model.brand_id!='for').all()



# -------------------------------------------------------------------
# Part 4: Write Functions


def get_model_info(year):
    """Takes in a year and prints out each model name, brand name, and brand
    headquarters for that year using only ONE database query."""

    model_info = (db.session.query(Model.name,
                                   Brand.name,
                                   Brand.headquarters)
                .join(Brand)
                .filter(Model.year==year)
                .order_by(Model.name, Brand.name, Brand.headquarters)
                .all()
    )

    # Iterate over each row in model_info query.  Prints the model name, brand
    # name, and headquarters.
    for model in model_info:
        print model[0].upper()
        print "\tBRAND: {}".format(model[1])
        print "\tHQ: {}\n".format(model[2])


def get_brands_summary():
    """Prints out each brand name (once) and all of that brand's models,
    including their year, using only ONE database query."""

    brands = (db.session.query(Brand.name,
                               Model.year,
                               Model.name)
            .join(Model)
            .order_by(Brand.name, Model.year, Model.name)
            .all()
    )

    brand_names = {}

    # iterates over each row in brands query.  Checks if the brand name is a 
    # key in the dictionary.  If not adds the brand name as a new key, and sets
    # the first value for that key.  If the key exists, adds value to the
    # existing key.
    for brand in brands:
        if brand[0] not in brand_names:
            brand_names[brand[0]] = [(brand[1], brand[2])]
        else:
            brand_names[brand[0]] += [(brand[1], brand[2])]

    # iterates over each key, value item in the dictionary.  Prints the brand
    # name once, followed by the models.
    for brand, model_info in brand_names.items():
        print "\n{}".format(brand.upper())
        for m in model_info:
            print "\t{} {}".format(m[0], m[1])


def search_brands_by_name(mystr):
    """Returns all Brand objects corresponding to brands whose names include
    the given string."""

    return Brand.query.filter(Brand.name.like('%{}%'.format(mystr))).all()


def get_models_between(start_year, end_year):
    """Returns all Model objects corresponding to models made between
    start_year (inclusive) and end_year (exclusive)."""

    return Model.query.filter(Model.year >= start_year,
                              Model.year < end_year).all()

