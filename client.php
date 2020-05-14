<!DOCTYPE html>
<html>
<head>
	<title>Поиск по клиенту</title>
    <link rel="stylesheet" type="text/css" href="table.css">
    <link rel="stylesheet" type="text/css" href="style.css">
    <link rel="stylesheet" type="text/css" href="input.css">
</head>
<body>
    <div id="wrapper">
        <div id="header"></div>
        <div id="menu">
            <a href="record.html">К ВЫБОРУ</a> &nbsp; &nbsp; &nbsp; &nbsp; 
        </div>
        <div id="main">
            <form action="" method="post">
                <p>Введите номер клиента:</p>
                <input type="number" name="number"/>
                <p><input type="submit" value="Enter"></p>
            </form>
        </div>
        <?php
            if(!empty($_POST["number"])){
                require_once 'connection.php';
                //$link = mysqli_connect($host, $user, $password, $database) or die("Ошибка подключения к базе данных" . mysqli_error($link));
                $link = pg_connect($host, $user, $password, $database) or die("Ошибка подключения к базе данных" . pg_result_error($link));
                /*$sql = mysqli_query($link, 
                "SELECT dt.date_time_accept, cl.phone_number, op.operator_team, top.name
                FROM client cl
                LEFT JOIN information inf ON cl.id_client = inf.id_client
                LEFT JOIN date_time dt ON dt.id_date_time = inf.id_date_time
                LEFT JOIN record rec ON rec.id_information = inf.id_information
                LEFT JOIN operator op ON op.id_operator = inf.id_operator
                LEFT JOIN record_topic rec_t ON rec_t.id_record=rec.id_record
                LEFT JOIN topic top ON top.id_topic=rec_t.id_topic
                WHERE phone_number= '{$_POST['number']}';");*/
                $sql = pg_query($link, 
                "SELECT dt.date_time_accept, cl.phone_number, op.operator_team, top.name
                FROM client cl
                LEFT JOIN information inf ON cl.id_client = inf.id_client
                LEFT JOIN date_time dt ON dt.id_date_time = inf.id_date_time
                LEFT JOIN record rec ON rec.id_information = inf.id_information
                LEFT JOIN operator op ON op.id_operator = inf.id_operator
                LEFT JOIN record_topic rec_t ON rec_t.id_record=rec.id_record
                LEFT JOIN topic top ON top.id_topic=rec_t.id_topic
                WHERE phone_number= '{$_POST['number']}';");
                if ($sql) {
                    //$rows = mysqli_num_rows($sql);
                    $rows = pg_num_rows($sql);
                    if($rows!=0) {
                        echo "<table  border=1  cellspacing=0 cellpading=0>
                        <tread>
                        <tr>
                        <td>Дата принятия вызова</sup></td>
                        <td>Номер клиента</td>
                        <td>Команда оператора</td>
                        <td>Тема разговора</td>
                        </tr>
                        <tread>";
                        echo "<tbody>";
                        for($i=1;$i<=$rows;++$i) {
                            //$row=mysqli_fetch_row($sql);
                            $row=pg_fetch_row($sql);
                            echo "<tr>";
                            for ($j=0; $j<4; ++$j) {
                                echo "<td>$row[$j]</td>";
                            }
                            echo "</tr>";
                        }
                        echo "</tbody>";
                        echo "</table>";
                    }
                    else {
                         echo "<div id=main><p>Клиентов с данным номером не найдено</p></div>";
                    }
                    //mysqli_free_result($sql);
                    pg_free_result($sql);
                }
                //mysqli_close($link);
                pg_close($link);
            }
        ?>
    </div>
    <div id="footer"> <a href="http://test1.ru/opd/index.html">Home</a> &copy;2020 </div>
</div>
</body>
</html>
