import psycopg2
import datetime

def IdRecord_query(cursor, curFileTxt):
    """
        :param cursor: объект курсора
        :param curFileTxt: str  -  название файла с расшифровкой разговора
        :return: id[0] int - id строки в таблице 'record', соответствующей заданному имени файла
    """
    cursor.execute('SELECT id_record FROM record WHERE transcript_txt = %s', (curFileTxt,))
    id = cursor.fetchone()
    if (id == None):
        return None
    else:
        return id[0]

def FillingTableMarkSystem(cursor, mark, log):
    """
        :param cursor: объект курсора
        :param mark: int  -  оценка
        :param log: str  -  название файла с логами
    """
    day_time = datetime.datetime.now()
    cursor.execute('INSERT INTO mark_system (date_time_mark_system, mark_system, file_logo) VALUES (%s, %s, %s)', (day_time, mark, log))

def IdMarkSystem_query(cursor, log):
    """
        :param cursor: объект курсора
        :param log: str  -  название файла с логами
        :return: id[0] int - id строки в таблице 'mark_system', соответствующей заданному имени файла логов
    """
    cursor.execute('SELECT id_mark_system FROM mark_system WHERE file_logo = %s', (log,))
    id = cursor.fetchone()
    if (id == None):
        return None
    else:
        return id[0]

def IdMark_query(cursor, id_system):
    """
        :param cursor: объект курсора
        :param id_system: int  -  id строки в таблице 'mark_system'
        :return: id[0] int - id строки в таблице 'mark', соответствующей заданному id таблицы 'mark_system'
    """
    cursor.execute('SELECT id_mark FROM mark WHERE id_mark_system = %s', (id_system,))
    id = cursor.fetchone()
    if (id == None):
        return None
    else:
        return id[0]

def InsertIdMarkSystem(cursor, id):
    """
        :param cursor: объект курсора
        :param id: int  -  id строки в таблице 'mark_system'
    """
    cursor.execute('INSERT INTO mark (id_mark_system) VALUES (%s)', (id,))

def InsertTopics(cursor, topics, id_record):
    """
        :param cursor: объект курсора
        :param topics: list  -  список тем разговора
        :param id_record: int  -  id строки в таблице 'record'
    """
    for TopicName in topics:
        cursor.execute('SELECT id_topic FROM topic WHERE name = %s', (TopicName,))
        topic_id = cursor.fetchone()
        if (topic_id == None):
            cursor.execute('INSERT INTO topic (name) VALUES (%s)', (TopicName,))
            cursor.execute('SELECT id_topic FROM topic WHERE name = %s', (TopicName,))
            topic_id = cursor.fetchone()[0]
        else:
            topic_id = topic_id[0]
        cursor.execute('INSERT INTO record_topic (id_record, id_topic) VALUES (%s, %s)', (id_record, topic_id))
def UpdateRecord(cursor, mark_id, record_id):
    """
        :param cursor: объект курсора
        :param mark_id: int  -  id строки в таблице 'mark'
        :param id_record: int  -  id строки в таблице 'record'
    """
    cursor.execute('UPDATE record set id_mark = %s where id_record = %s', (mark_id, record_id))
