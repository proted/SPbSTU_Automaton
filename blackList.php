<!DOCTYPE html>
<html>
<head>
	<title>Черный список</title>
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
        <?php
        require_once 'connection.php';
        //$link = mysqli_connect($host, $user, $password, $database) or die("Ошибка подключения к базе данных" . mysqli_error($link));
        $link = pg_connect(host=$host, port=$port, dbname=$database, user=$user, password=$password) or die("Ошибка подключения к базе данных" . pg_result_error($link));
        $sql = pg_query($link, 
        "SELECT cl.id_client, cl.phone_number
        FROM client cl
        WHERE cl.blacklist = 1;");
        if ($sql) {
            //$rows = mysqli_num_rows($sql);
            $rows = pg_num_rows($sql);
            if($rows!=0) {
                echo "<table  border=1  cellspacing=0 cellpading=0>
                <tread>
                <tr>
                <td>Id клиента</sup></td>
                <td>Номер телефона</td>
                </tr>
                <tread>";
                echo "<tbody>";
                for($i=1;$i<=$rows;++$i) {
                    //$row=mysqli_fetch_row($sql);
                    $row=pg_fetch_row($sql);
                    echo "<tr>";
                    for ($j=0; $j<2; ++$j) {
                        echo "<td>$row[$j]</td>";
                    }
                    echo "</tr>";
                }
                echo "</tbody>";
                echo "</table>";
            }
            else {
                echo "<div id=main><p>Черный список пуст</p></div>";
            }
            //mysqli_free_result($sql);
            pg_free_result($sql);
        }
        //mysqli_close($link);
        pg_close($link);
        ?>
    </div>
  <div id="footer"> <a href="http://test1.ru/opd/index.html">Home</a> &copy;2020 </div>
</div>
</body>
</html>
