import psycopg2
from config import config

class db(object):
    def __init__(self):
        self.params = config()
        self.connection = None
        self.cursor = None
        if self.connect():
            print('PostgreSQL database version:')
            self.cursor.execute('SELECT version()')
            # display the PostgreSQL database server version
            db_version = self.cursor.fetchone()
            print(db_version)

    def connect(self):
        try:
            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            self.connection = psycopg2.connect(**self.params)
            self.cursor = self.connection.cursor()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            #self.disconnect()

    def disconnect(self):
        # close the communication with the PostgreSQL
        self.cursor.close()
        self.connection.close()
        print('Database connection closed.')


    def insert_record(self, _table_name, _record_object):
        if self.connect():           
            try:
                
                _value_keys = self.clean_array_text(str([i for i in _record_object]))
                _value_count = self.clean_array_text(str(["%s" for i in _record_object]))
                sql = "INSERT INTO {table_name} ({value_keys}) VALUES ({value_count});".format(table_name = _table_name, value_keys=_value_keys, value_count=_value_count)
                values = tuple([_record_object[i] for i in _record_object])
                print("Inserting values: "+str(values))
                self.cursor.execute(sql, values)
                self.connection.commit()
                print("Sucess")
                self.disconnect()
                return True

            except Exception as e:
                print("Insert Record error: "+str(e))
        self.disconnect()
        return False

    def get_all_records(self, _table_name, _value_keys):
        if self.connect():           
            try:
                sql = 'SELECT * FROM {table_name}'.format(table_name = _table_name)
                self.cursor.execute(sql)
                print("The number of parts: ", self.cursor.rowcount)
                row = self.cursor.fetchone()
                return_list = []
                while row is not None:
                    return_list.append(dict(zip(_value_keys, row)))
                    row = self.cursor.fetchone()
                    
                self.disconnect()
                return return_list

            except Exception as e:
                print("Insert Record error: "+str(e))
        self.disconnect()
        return False

    def get_records_between(self, _table_name, _value_keys, _field, _start, _end):
        if self.connect():           
            try:
                sql = "SELECT * FROM {table_name} WHERE {field} BETWEEN '{start}' AND '{end}'".format(table_name = _table_name, field=_field, start=_start, end=_end)
                self.cursor.execute(sql)
                print("The number of parts: ", self.cursor.rowcount)
                row = self.cursor.fetchone()
                return_list = []
                while row is not None:
                    return_list.append(dict(zip(_value_keys, row)))
                    row = self.cursor.fetchone()
                    
                self.disconnect()
                return return_list

            except Exception as e:
                print("Insert Record error: "+str(e))
        self.disconnect()
        return False


    def clean_array_text(self, _input):
        clean = ["'", "[", "]"]
        for x in clean:
            _input = _input.replace(x, "")
        return _input