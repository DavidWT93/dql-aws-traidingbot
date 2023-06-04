from sqlalchemy import create_engine, DDL,text,table
import config


def load_data_to_rds(df, tableName, keyColumn,createTable=False):
    sqlEngine = create_engine(
        f'mysql+pymysql://{config.AWS_RDS_USER}:{config.AWS_RDS_PASSWORD}@{config.AWS_RDS_HOST}/{config.AWS_RDS_DB}')
    dbConnection = sqlEngine.connect()

    if createTable:
        df.to_sql(tableName, sqlEngine, if_exists='append', index=False)
        #dbConnection.execute(DDL(f"ALTER TABLE {tableName} ADD PRIMARY KEY ({keyColumn}(100));"))

        unique_constraint = f'ALTER TABLE {tableName} ADD CONSTRAINT unique_keyColumn UNIQUE ({keyColumn}(100))'
        dbConnection.execute(DDL(text(unique_constraint)))

    else:

        for _, row in df.iterrows():
            formatted_list = [repr(item) for item in row.values]
            input = ', '.join(formatted_list)
            print(input)
            print(f'INSERT IGNORE INTO {tableName} VALUES ({input})')
            dbConnection.execute(DDL(f'INSERT IGNORE INTO {tableName} VALUES ({input})'))

    dbConnection.close()