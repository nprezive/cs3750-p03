<?php
	require 'Connection.php';
	$login = new Connection;
	$xToggle = $POST_['xCord']; 
	$yToggle = $POST_['yCord']; 
	connect($xToggle, $yToggle);
	

    $con;
	   
    function connect($xToggle, $yToggle)
    {
		global $login;
        $con = new mysqli($login->host,$login->username,$login->password,$login->db);
        if(!$con)
        {
            echo mysqli_error($con);
        }

        $sql=mysqli_query($con,"INSERT INTO CommitQueue(xCord, yCord) VALUES('$xToggle', '$yToggle')");
        if(!$sql)
        {
            echo mysqli_error($con);
        }
    }
	
?>	