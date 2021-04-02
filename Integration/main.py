#Модуль os для работы с операционной системой
import os
from queries import *
from connection import *
from errors import *
from recognition import recognition
from dialog_analysis import analysis

# Подключение к базе данных
con = ConnectDataBase()
cursor = con.cursor()

#Директория необработанных файлов txt
UnprDirTxt = "D:\\TxtFiles\\unprocessed\\"
#Директория обработанных файлов txt
PrDirTxt = "D:\\TxtFiles\\processed\\"
#Директория обработанных файлов mp3
UnprDirMp3 = "D:\\mp3Files\\unprocessed\\"
#Директория обработанных файлов mp3
PrDirMp3 = "D:\\mp3Files\\processed\\"


# Цикл по всем элементам в этой папке
while True:
     # Выбор директории, где лежат необработанные mp3 файлы
     os.chdir(UnprDirMp3)
     if len(os.listdir()) != 0:
          #Выбор последнего файла в папке c mp3 файлами
          curFileMp3 = os.listdir().pop()
          #Запуск системы оценивания
          recognition(curFileMp3)
          #Перенос файла из папки "необработанные" в "обработанные"
          os.replace(curFileMp3, PrDirMp3 + curFileMp3)


     # Выбор директории, где лежат необработанные txt файлы
     os.chdir(UnprDirTxt)

     if len(os.listdir()) != 0:
          # Выбор последнего файла в папке с txt файлами
          curFileTxt = os.listdir().pop()

          # По файлу txt находи id нужной записи
          id_record = IdRecord_query(cursor, curFileTxt)

          # Если id не нашли, то выводить ошибку
          CheckErrWithID(id_record)

          # Запуск функции анализа диалога
          mark, log, topics = analysis(curFileTxt, str(id_record))

          # Заполнение базы данных полученными данными
          FillingTableMarkSystem(cursor, mark, log)

          # Получение id нужной нам строки в таблице 'marksystem'
          id_MarkSystem = IdMarkSystem_query(cursor, log)
          # Если id не нашли, то выводить ошибку
          CheckErrWithID(id_MarkSystem)

          # Добавление в таблицу 'mark' id строки в таблице, где записаны данные об оценке системы
          InsertIdMarkSystem(cursor, id_MarkSystem)

          # Получение id нужной строки в таблице 'mark', где записана оценка системы
          id_Mark = IdMark_query(cursor, id_MarkSystem)

          # Добавление тем разговора
          InsertTopics(cursor, topics, id_record)

          # Добавление связи таблиц 'record' и 'mark'
          UpdateRecord(cursor, id_Mark, id_record)

          # Применение изменений, которые внесли в базу данных
          con.commit()

          # Перенос файла из папки "необработанные" в "обработанные"
          os.replace(curFileTxt, PrDirTxt + curFileTxt)
