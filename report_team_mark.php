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
                <p>Введите Id команды:</p>
                <p><input type="number" name="id"/></p>
                <p>Выберите вид оценки</p>
                <p><input type="radio" name="client"/> Оценка клиента</p>
                <p><input type="radio" name="system"/> Оценка системы</p>
                <p><input type="radio" name="inspector"/> Оценка инспектора</p>
                <p>Введите оценку:</p>
                <p><input type="number" name="mark"/></p>
                <p><input type="submit" value="Enter"/></p>
            </form>
        </div>
        <?php
            if(!empty($_POST["date_start"]) & !empty($_POST["date_end"]) & (isset($_POST["client"]) || isset($_POST["system"]) || isset($_POST["inspector"]) ) & !empty($_POST["mark"])) {
                include ('connection.php');
                //$link = mysqli_connect($host, $user, $password, $database) or die("Ошибка подключения к базе данных" . mysqli_error($link));
                $link = pg_connect(host=$host, port=$port, dbname=$database, user=$user, password=$password) or die("Ошибка подключения к базе данных" . pg_result_error($link));
                if(isset($_POST["client"])) {
                    $sql = pg_query($link, 
                    "SELECT rec.id_record, rec.title_mp3, rec.transcript_txt, dt.date_time_accept, dt.date_time_start, dt.date_time_end, dt.duration, inf.direction_call, inf.status_ending, op.id_operator, t.name, cl.phone_number, cl.blacklist, m.mark_client, m_insp.mark_inspector, m_insp.date_time_mark_inspector, insp.name, m_insp.comment, m_insp.file_logo, m_syst.mark_system, m_syst.date_time_mark_system, m_syst.file_logo
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
                    WHERE date_time_accept > '{$_POST['date_start']}' AND date_time_accept < '{$_POST['date_end']}' AND m.mark_client='{$_POST['mark']}' AND t.id_team='{$_POST['id']}';");
                }
                elseif (isset($_POST["system"])) {
                    $sql = pg_query($link, 
                    "SELECT rec.id_record, rec.title_mp3, rec.transcript_txt, dt.date_time_accept, dt.date_time_start, dt.date_time_end, dt.duration, inf.direction_call, inf.status_ending, op.id_operator, t.name, cl.phone_number, cl.blacklist, m.mark_client, m_insp.mark_inspector, m_insp.date_time_mark_inspector, insp.name, m_insp.comment, m_insp.file_logo, m_syst.mark_system, m_syst.date_time_mark_system, m_syst.file_logo
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
                    WHERE date_time_accept > '{$_POST['date_start']}' AND date_time_accept < '{$_POST['date_end']}' AND m_syst.mark_system='{$_POST['mark']}' AND t.id_team='{$_POST['id']}';");
                }
                else {
                    $sql = pg_query($link, 
                    "SELECT rec.id_record, rec.title_mp3, rec.transcript_txt, dt.date_time_accept, dt.date_time_start, dt.date_time_end, dt.duration, inf.direction_call, inf.status_ending, op.id_operator, t.name, cl.phone_number, cl.blacklist, m.mark_client, m_insp.mark_inspector, m_insp.date_time_mark_inspector, insp.name, m_insp.comment, m_insp.file_logo, m_syst.mark_system, m_syst.date_time_mark_system, m_syst.file_logo
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
                    WHERE date_time_accept > '{$_POST['date_start']}' AND date_time_accept < '{$_POST['date_end']}' AND m_insp.mark_inspector='{$_POST['mark']}' AND t.id_team='{$_POST['id']}';");
                }
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
