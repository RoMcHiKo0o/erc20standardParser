import psycopg2

from psycopg2.extras import execute_values

# file with db interaction


# connect to db
def connect():
    dbname = "postgres"
    username = "postgres"
    password = "admin"
    host = "localhost"
    port = 5432
    try:
        connection = psycopg2.connect(
            dbname=dbname, user=username, password=password, host=host, port=port
        )

        return connection

    except Exception as e:
        print("connection error:", e)


# returns
# def get_contracts(connection):
#   cursor = connection.cursor()
#   sql = "SELECT * FROM contract"

#   cursor.execute(sql)

#   records = cursor.fetchall()

#   return records


# insert one contract
def insert_contract(connection, contract_data):
    cursor = connection.cursor()
    sql = """
  INSERT INTO contract (contract_address, source_code)
  VALUES (%s, %s)
  """
    cursor.execute(sql, contract_data)
    connection.commit()


# update status to "processing" of records. ids — list of id of this records
def update_status_to_processing(connection, ids):
    cursor = connection.cursor()

    sql = f"""UPDATE contract
      SET status = 'processing' where contract_address IN  {tuple(ids)}"""
    cursor.execute(sql)
    connection.commit()


# method selects records that have status "waits processing"
def get_wait_processing_contracts(connection, amount=100):
    cursor = connection.cursor()
    sql = f"SELECT contract_address, source_code FROM contract where status = 'waits processing' LIMIT {amount}"

    cursor.execute(sql)

    records = cursor.fetchall()
    return records


# updates records
def update_records(connection, records):
    cursor = connection.cursor()

    sql = """UPDATE contract
          SET is_erc20=data.is_erc20,
              erc20_version=data.version,
              status='processed' FROM (VALUES %s) as data(id,is_erc20,version)
              WHERE contract.contract_address = data.id"""

    execute_values(cursor, sql, records)
    connection.commit()
