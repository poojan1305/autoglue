from glue import createddl 
import boto3
athena = boto3.client('athena')
database_og = 'e_ukba_db'

database_tocreate_inside = f'{database_og}_2'


def gettables(database):
    glue = boto3.client('glue')
    response = glue.get_tables(DatabaseName=database)
    table_list = response['TableList']
    for table in table_list:
        print(f"Table Name: {table['Name']}")
        ddl_to_trigger = createddl(database_og, table['Name'], database_tocreate_inside)
        executeddl(ddl_to_trigger, database_tocreate_inside)
        
        


def checkdatabase(database_tocreate_inside):
    glue = boto3.client('glue')
    try:
        response = glue.get_database(Name=database_tocreate_inside)
        return True  
    except glue.exceptions.EntityNotFoundException:
        return False 
    
def startdatabase(database_tocreate_inside):
    glue = boto3.client('glue')
    response = glue.create_database(
        DatabaseInput={
            'Name': database_tocreate_inside,
            'Description': 'Database created for Athena queries',
            'LocationUri': f's3://playingwithstorage3/{database_tocreate_inside}/'
        }
    )
    return response

def executeddl(ddl_to_trigger, database_tocreate_inside):

    if not checkdatabase(database_tocreate_inside):
        startdatabase(database_tocreate_inside)
        execute_ddl(ddl_to_trigger, database_tocreate_inside)
    else:
        print(f"Database '{database_tocreate_inside}' already exists. Executing DDL statement.")
        execute_ddl(ddl_to_trigger, database_tocreate_inside)
        
        
def execute_ddl(ddl_to_trigger, database_tocreate_inside):
        
        response = athena.start_query_execution(
    QueryString=ddl_to_trigger,
    QueryExecutionContext={
        'Database': database_tocreate_inside 
        
    },
    ResultConfiguration={
        'OutputLocation': 's3://playingwithstorage3/query-results/'  
    },
    WorkGroup='primary'  
)
        
if __name__ == "__main__":
    try:
 
        gettables(database_og)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Execution completed.")
