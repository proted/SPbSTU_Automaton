import psycopg2
def ConnectDataBase():
    """
        :return: сon - переменная для работы с подключенной базой данных
    """
    con = psycopg2.connect(
      database="magnit",
      user="postgres",
      password="12345",
      host="localhost",
      port="5432"
    )
    return con
