<!DOCTYPE html>
<html>
<head>
	<title>Отчетность</title>
    <link rel="stylesheet" type="text/css" href="style.css">
    <link rel="stylesheet" type="text/css" href="input.css">
    <meta content="text/csv"; charset="utf-8">
</head>
<body>
    <div id="wrapper">
        <div id="header"></div>
        <div id="menu">
            <a href="report.html">К ВЫБОРУ</a> &nbsp; &nbsp; &nbsp; &nbsp; 
        </div>
        <div id="main">
            <form action="" method="post">
                <p>Введите период отчетности:</p>
                <input type="datetime-local" id="localdate" name="date_start"/> -
                <input type="datetime-local" id="localdate" name="date_end"/>
                <p>Выберите направление звонка:</p>
                <p><input type="radio" name="in"/> Входящий</p>
                <p><input type="radio" name="out"/> Исходящий</p>
                <p><input type="radio" name="inter"/> Внутренний</p>
                <p><input type="radio" name="callb"/> Callback</p>
                <p>Выберите статус завершения:</p>
                <p><input type="radio" name="end"/> Завершён</p>
                <p><input type="radio" name="transf"/> Переведён</p>
                <p><input type="radio" name="dum"/> Сброшен</p>
                <p><input type="submit" value="Enter"/></p>
            </form>
        </div>
        <?php
            if(!empty($_POST["date_start"]) & !empty($_POST["date_end"]) & (isset($_POST["in"]) || isset($_POST["out"]) || isset($_POST["inter"]) || isset($_POST["callb"])) & (isset($_POST["end"]) || isset($_POST["transf"]) || isset($_POST["dum"]) )) {
                include ('connection.php');
                //$link = mysqli_connect($host, $user, $password, $database) or die("Ошибка подключения к базе данных" . mysqli_error($link));
                $link = pg_connect($host, $user, $password, $database) or die("Ошибка подключения к базе данных" . pg_result_error($link));
                if(isset($_POST["in"])) {     $direction=1;    }
                elseif (isset($_POST["out"])) {    $direction=2;    }
                elseif (isset($_POST["inter"])) {    $direction=3;    }
                else {  $direction=4;    }
                if(isset($_POST["end"])) {    $status=1;    }
                elseif (isset($_POST["transf"])) {    $status=2;    }
                else {  $status=3;  }
                $sql = pg_query($link, 
                "SELECT rec.id_record, rec.title_mp3, rec.transcript, dt.date_time_accept, dt.date_time_start, dt.date_time_end, dt.duration, inf.direction_call, inf.status_ending, op.id_operator, op.name, t.name, cl.phone_number, cl.blacklist, m.mark_client, m_insp.mark_inspector, m_insp.date_time_mark_inspector, insp.name, m_insp.comment, m_insp.file_logs, m_syst.mark_system, m_syst.date_time_mark_system, m_syst.file_logs
                    FROM date_time dt
                    LEFT JOIN information inf ON inf.id_date_time=dt.id_date_time
                    LEFT JOIN record rec ON rec.id_information=inf.id_information
                    LEFT JOIN operator op ON op.id_operator=inf.id_operator
                    LEFT JOIN team t ON t.id_team=op.id_team
                    LEFT JOIN client cl ON cl.id_client=inf.id_client
                    LEFT JOIN mark m ON rec.id_mark=m.id_mark
                    LEFT JOIN mark_inspector m_insp ON m.id_mark_inspector=m_insp.id_mark_inspector
                    LEFT JOIN inspector insp ON m_insp.id_inspector=insp.id_inspector
                    LEFT JOIN mark_system m_syst ON m_syst.id_mark_system=m.id_mark_system
                WHERE date_time_accept > '{$_POST['date_start']}' AND date_time_accept < '{$_POST['date_end']}' AND inf.direction_call=$direction AND inf.status_ending=$status;");
                if ($sql) {
                    include( 'reportInCsv.php');
                    ReportInCsv($sql);
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
