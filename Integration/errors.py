def CheckErrWithID(id):
    """
        :param id: int - id для проверки
        :return: Если id не подходит, пишет ошибку и закрывает программу
    """
    if (id == None):
        print('Error with ID in DataBase')
        exit()
