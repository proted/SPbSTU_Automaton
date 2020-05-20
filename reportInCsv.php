<?php
function ReportInCsv ($sql) {
    include ('connection.php');
    $link = pg_connect(host=$host, port=$port, dbname=$database, user=$user, password=$password) or die("Ошибка подключения к базе данных" . mysqli_error($link));
	//$rows = mysqli_num_rows($sql);
    $rows=pg_num_rows($sql);
    $blackList=0; # черный список
    $markClient=0; # оценка клиента
    $markInspector=0; # оценка инспектора
    $markSystem=0; # оценка системы
    $enteringCall=0; # входящий звонок
    $outgoingCall=0; # исходящий звонок
    $internalCall=0; # внутренний звонок
    $callback=0; # callback
    $complitedCall=0; # звонок завершен
    $transferedCall=0; # звонок переведен
    $resetCall=0; # звонок сброшен
    if($rows!=0) {
        $fp=fopen('test.csv', 'w');
        #fputs($fp, chr(0xEF) . chr(0xBB) . chr(0xBF));
        $title=array("Id записи", "Имя mp3", "Имя расшифровки", "Дата/время принятие звонка", "Дата/время начала диалога", "Дата/время окончания диалога", "Продолжительность диалога", "Id оператора", "Название команды", "Номер клиента","Черный список", "Направление звонка", "Статус окончания", "Оценка клиента", "Оценка инспектора", "Комментарий", "Имя инспектора", "Дата/время выставления оценки", "Файл лог", "Оценка системы", "Дата/время выставления оценки", "Файл лог", "Тема диалога и ее вес");
        fputcsv($fp, $title, ';');
        echo "<div id=main>
        <p>Количество записей за данный период: $rows</p>";
        $flag=0;
        $count=0;
        for($i=1;$i<=$rows;++$i) {
            //$row=mysqli_fetch_row($sql);
            $row=pg_fetch_row($sql);
            # направление звонка
            if($row[7]==1) {    $enteringCall++;    $row[7] = 'Входящий';   }
            elseif ($row[7]==2) {    $outgoingCall++;    $row[7] = 'Исходящий'; }
            elseif ($row[7]==3) {    $internalCall++;    $row[7] = 'Внутренний';  }
            else {  $callback++;    $row[7] = 'Callback';}
            # статус завершения
            if($row[8]==1) {    $complitedCall++;   $row[8] = 'Завершён';}
            elseif ($row[8]==2) {   $transferedCall++;  $row[8] = 'Переведен';  }
            else {  $resetCall++;  $row[8] = 'Сброшен';}
            # черный список
            if($row[12]==1) {    $blackList++;    $row[12] = 'В черном списке'; }
            else {  $row[12] = '-';}
            # оценки
            $markClient=$markClient+$row[13];
            $markInspector=$markInspector+$row[14];
            $markSystem=$markSystem+$row[19];
            if($row[0]!=$id) {
                $flag=0;
            }
            if($flag==0) {
                $flag=1;
                $id=$row[0];
                $sql1=pg_query($link, "SELECT t.name, rec_top.priority FROM topic t LEFT JOIN record_topic rec_top ON rec_top.id_topic=t.id_topic  WHERE rec_top.id_record=$id;");
                $rows1 = pg_num_rows($sql1);
                for($k=1;$k<=$rows1;$k++) {
                    $row_top=pg_fetch_row($sql1);
                    $t="$row_top[0]";
                    $p="$row_top[1]";
                    $l=$l.$t.' ('.$p.') ';
                }
                array_push($row, $l);
                $l='';
            }
            fputcsv($fp, $row, ';');
        }
        $markClient=$markClient/$rows;
        $markInspector=$markInspector/$rows;
        $markSystem=$markSystem/$rows;
        echo "<p>Входящих - $enteringCall</p>";
        echo "<p>Исходящих - $outgoingCall</p>";
        echo "<p>Внутренних - $internalCall</p>";
        echo "<p>Callback - $callback</p>";
        echo "<p>Завершено - $complitedCall</p>";
        echo "<p>Переведено - $transferedCall</p>";
        echo "<p>Сброшено - $resetCall</p>";
        echo "<p>Средняя оценка клиентов: $markClient</p>";
        echo "<p>Средняя оценка инспекторов: $markInspector</p>";
        echo "<p>Средняя оценка системы: $markSystem</p>";
        echo "<p>Количество звонков от клиентов в черном списке: $blackList</p>";
        echo "</div>";
        fclose($fp);
    }
    else {
        echo "<div id=main><p>Записей в данный период не найдено</p></div>";
    }
}
?>
