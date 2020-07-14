#Модуль os для работы с операционной системой
import os
#Директория необработанных файлов txt
UnprDirTxt = "D:\\TxtFiles\\unprocessed\\"
#Директория обработанных файлов txt
PrDirTxt = "D:\\TxtFiles\\processed\\"
#Директория обработанных файлов mp3
UnprDirMp3 = "D:\\mp3Files\\unprocessed\\"
#Директория обработанных файлов mp3
PrDirMp3 = "D:\\mp3Files\\processed\\"


#Цикл по всем элементам в этой папке
while True:
     # Выбор директории, где лежат необработанные mp3 файлы
     os.chdir(UnprDirMp3)
     if len(os.listdir()) != 0:
          #Выбор последнего файла в папке c mp3 файлами
          curFileMp3 = os.listdir().pop()
          #Запуск системы оценивания
          #TODO: добавить вызов функции для распознавания

          #Перенос файла из папки "необработанные" в "обработанные"
          os.replace(curFileMp3, PrDirMp3 + curFileMp3)

          # Выбор директории, где лежат необработанные txt файлы
     os.chdir(UnprDirTxt)
     if len(os.listdir()) != 0:
          # Выбор последнего файла в папке с txt файлами
          curFileTxt = os.listdir().pop()
          # Запуск системы оценивания
          # TODO: добавить вызов функции для оценивания

          # Перенос файла из папки "необработанные" в "обработанные"
          os.replace(curFileTxt, PrDirTxt + curFileTxt)





