


<?php
	//return settings
	require_once 'Connection.php';
	$login = new Connection;
	connect();
	
    $con;
	$json_output;
	
	function connect()
    {
		global $login;
        $con = new mysqli($login->host,$login->username,$login->password,$login->db);
        if(!$con)
        {
            echo mysqli_error($con);
        }
		$result=mysqli_query($con,"SELECT MAX(xCord) AS maxX FROM GameMap");
        if(!$result)
        {
            echo mysqli_error($con);
        }
		
		$json_output = "{\"xCord\":";
		$json_output = $json_output . $result->fetch_object()->maxX;
		$json_output = $json_output . ",\"yCord\":";
		
		$result=mysqli_query($con,"SELECT MAX(yCord) AS maxY FROM GameMap");
        if(!$result)
        {
            echo mysqli_error($con);
        }
		
		$json_output = $json_output . $result->fetch_object()->maxY;
		$json_output = $json_output . "}";
		
		echo $json_output;
		
    }


	/*
	//return settings
	require 'Connection.php';
	$login = new Connection;
	connect();
	
    $con;
	
	function connect()
    {
		global $login;
        $con = new mysqli($login->host,$login->username,$login->password,$login->db);
        if(!$con)
        {
            echo mysqli_error($con);
        }
		$result=mysqli_query($con,"SELECT MAX(xCord) AS maxX FROM GameMap");
        if(!$result)
        {
            echo mysqli_error($con);
        }
		
		echo "{\"xCord\":";
		echo $result->fetch_object()->maxX;
		echo ",\"yCord\":";
		$result=mysqli_query($con,"SELECT MAX(yCord) AS maxY FROM GameMap");
        if(!$result)
        {
            echo mysqli_error($con);
        }
		
		echo $result->fetch_object()->maxY;
		echo "}";
		
    }
	*/
    
	
?>
