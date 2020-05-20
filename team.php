<!DOCTYPE html>
<html>
<head>
	<title>Поиск по команде</title>
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
                <p>Введите команду оператора:</p>
                <input type="text" name="team"/>
                <p><input type="submit" value="Enter"></p>
            </form>
        </div>
        <?php
            if(!empty($_POST["team"])){
                require_once 'connection.php';
                //$link = mysqli_connect($host, $user, $password, $database) or die("Ошибка подключения к базе данных" . mysqli_error($link));
                $link = pg_connect($connection_string) or die("Ошибка подключения к базе данных" . pg_result_error($link));
                $sql = pg_query($link, 
                "SELECT rec.id_record, dt.date_time_accept, cl.phone_number, t.name
                FROM date_time dt 
                LEFT JOIN information inf ON dt.id_date_time = inf.id_date_time
                LEFT JOIN operator op ON op.id_operator = inf.id_operator
                LEFT JOIN team t ON t.id_team=op.id_team
                LEFT JOIN record rec ON rec.id_information = inf.id_information
                LEFT JOIN record_topic rec_t ON rec_t.id_record=rec.id_record
                LEFT JOIN topic top ON top.id_topic=rec_t.id_topic
                LEFT JOIN client cl ON cl.id_client=inf.id_client
                WHERE t.name='{$_POST['team']}';");
                if ($sql) {
                    //$rows = mysqli_num_rows($sql);
                    $rows=pg_num_rows($sql);
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
                        $k=0;
                        $id=0;
                        for($i=1;$i<=$rows;++$i) {
                            //$row=mysqli_fetch_row($sql);
                            $row=pg_fetch_row($sql);
                            if($row[0]!=$id){
                                $flag=0;
                            }
                            if($flag==0) {
                                $flag=1;
                                echo "<tr>";
                                for ($j=1; $j<4; ++$j) {
                                    echo "<td>$row[$j]</td>";
                                }
                                $id=$row[0];
                                //$sql1=mysqli_query($link, "SELECT t.name FROM topic t LEFT JOIN record_topic rec_top ON rec_top.id_topic=t.id_topic  WHERE rec_top.id_record='$row[0]';");
                                $sql1=pg_query($link, "SELECT t.name FROM topic t LEFT JOIN record_topic rec_top ON rec_top.id_topic=t.id_topic  WHERE rec_top.id_record='$row[0]';");
                                //$rows1 = mysqli_num_rows($sql1);
                                $rows1 = pg_num_rows($sql1);
                                echo "<td>";
                                for($k=1;$k<=$rows1;$k++) {
                                    //$row=mysqli_fetch_row($sql1);
                                    $row=pg_fetch_row($sql1);
                                    echo "$row[0], ";
                                }
                                echo "</td>";
                                echo "</tr>"; 
                            }
                        }
                        echo "</tbody>";
                        echo "</table>";
                    }
                    else {
                        echo "<div id=main><p>Записей данной команды не найдено</p></div>";
                    }
                    //mysqli_free_result($sql);
                    pg_free_result($sql);
                }
                //mysqli_close($link);
                pg_close($link);
            }
        ?>
    </div>
  <div id="footer"> <a href="index.html">Home</a> &copy;2020 </div>
</div>
</body>
</html>
