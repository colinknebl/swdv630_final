from sqlalchemy import create_engine, Column, Integer, String, Float, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class DB:

    class MultipleResultsError(Exception):
        pass

    Base = declarative_base()

    __instance = None

    def __dirty_session(self):
        return self.session.dirty

    dirty = property(__dirty_session, None, None)

    def __new_session(self):
        return self.session.new

    new = property(__new_session, None, None)

    def __new__(cls, *args, **kwargs):
        if cls.__instance == None:
            instance = object.__new__(cls)
            # set instance attributes
            engine = create_engine('sqlite:///', echo=False)
            instance.engine = engine
            cls.Base.metadata.create_all(engine)
            instance.session = sessionmaker(bind=engine)()
            cls.__instance = instance
        return cls.__instance

    @staticmethod
    def __split_key_val_pair(string):
        """
            Splits a string with n key/val pairs

            @param {string} a string with key val pairs, each pair must be seperated with a comma, and each key/val must be separated with '='
                    @example 'name=Scarf, color=blue'
            
            @return {tuple[]} an array of tuples representing key/val pairs
                    @example [('name', 'Scarf'), ('color', 'blue')]
        """

        pairs = []
        split = string.split(',')
        for key_val_pair in split:
            stripped_pair = key_val_pair.strip()
            key, val = stripped_pair.split('=')
            pairs.append((key.strip(), val.strip()))
        return pairs

    @staticmethod
    def __build_query(cls, params):
        """
            Builds a query filter statement

            @param {class} cls = the class type to search
            @param {tuple[]} params = an array of tuples representing key/val pairs
                    @example [('name', 'Scarf'), ('color', 'blue')]
            
            @returns {object[]}
        """
        
        query = []
        for key, val in params:
            query.append(getattr(cls, key) == val)
        return query

    def __get_query(self, cls, key_val_pair_string):
        """Facilitates the generation of a DB query"""

        return self.__build_query(
            cls, 
            self.__split_key_val_pair(key_val_pair_string)
        )

    def query(self, cls, key_val_pair_string):
        """
            Query a specific item in the DB.

            @param {class} cls = the class type to search
            @param {string} key_val_pair_string = the key val pair string 
                        example: 'foo=bar, charlie=brown'

            Example Usage: 
                item1 = db.query(<class>, 'name=Pants, color=blue')
        """

        items = None

        try:
            if cls == None or key_val_pair_string == None:
                return

            query = self.__get_query(cls, key_val_pair_string)
        
            items = self.session.query(cls).filter(*query).all()
            
            # if multiple items were returned, warn the user
            if len(items) > 1:
                raise DB.MultipleResultsError()

        except DB.MultipleResultsError: 
            # catch the exception if multiple items were returned from the query and print a warning message 
            print('Multiple results returned: type = %r, query = %r; returning first result. %r' % (cls, key_val_pair_string, items[0]))

        return items[0] if len(items) > 0 else None

    def query_all(self, cls):
        """
            Query all items of a specific type

            @param {class} cls = the class type to search

            Example Usage:
                items = db.query_all(<class>)
        """

        if cls == None:
            return
        return self.session.query(cls).all()

    def insert(self, item, commit=False):
        """Add an item to the DB"""

        self.session.add(item)
        if commit:
            self.commit()

    def insert_many(self, items, commit=False):
        """Add multiple items to the DB"""

        self.session.add_all(items)
        if commit:
            self.commit()

    def commit(self):
        """Commit updates to the DB"""

        self.session.commit()

    def cancel_update(self):
        """Cancel updates to the DB"""

        self.session.rollback()

    def delete(self, item):
        """Delete an item from the DB, commit not necessary"""

        self.session.delete(item)