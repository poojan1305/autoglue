import boto3

glue = boto3.client('glue')

# response = glue.get_tables(
#     DatabaseName='e_ukba_db'
# )
# # print(response['TableList'])  # Print the response directly

# for table in response['TableList']:
# #     # print(f"Table Name: {table['Name']}")
#     print(table['Name'])
#     # print(f"Table Type: {table['TableType']}")
#     # print(f"Storage Descriptor: {table['StorageDescriptor']}")
#     # print(f"Columns: {table['StorageDescriptor']['Columns']}")
#     # print(f"Parameters: {table['Parameters']}")
#     print("-" * 40)  # Separator for readability

database_og='e_ukba_db'
# tableval_og='tehacct'
# database_tocreate_inside='e_ukba_db_2'


def createddl(database,table_value,database_tocreate_inside):
    
    response = glue.get_table(
    DatabaseName=database,
    Name=table_value
)
    table=response['Table']
    # print(response['Table']['StorageDescriptor'])  # Print the response directly
    value=table['StorageDescriptor']['Columns']
    # for val in value:
    #     print(val['Name'],val['Type'])
        
    columns = table['StorageDescriptor']['Columns']
    # print(columns)
    ddl=f"CREATE EXTERNAL TABLE `{database_tocreate_inside}`{'.'}`{table_value}` (\n"
    for column in columns:
        ddl+=f"  `{column['Name']}` {column['Type']},\n"
    ddl = ddl.rstrip(",\n") + "\n)"
    ddl+="\n STORED AS parquet "
    ddl+=f'\n Location "{"/".join(table["StorageDescriptor"]["Location"].split("/",3)[:3])}{"/"}{database}{"_2"}{"/"}{table_value}" '
    ddl+=f"\n TBLPROPERTIES ('classification'='parquet')"
    return ddl
# createddl(database_og,tableval_og,database_tocreate_inside)