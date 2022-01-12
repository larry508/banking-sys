import os



#############################
#    DATABASE CONNECTION    #
#############################
USERNAME = os.environ.get('MSSQL_USERNAME')
PASSWORD = os.environ.get('MSSQL_PASSWORD')
HOST = os.environ.get('MSSQL_HOST')
DATABASE=os.environ.get('MSSQL_DATABASE')
CONSTR=os.environ.get('MSSQL_CONSTR')


DB_URI = CONSTR % (USERNAME, PASSWORD, HOST, DATABASE)