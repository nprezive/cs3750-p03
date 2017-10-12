<?php
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
            echo mysqli_error();
        }
		$result=mysqli_query($con,"SELECT MAX(xCord) AS maxX FROM GameMap");
        if(!$result)
        {
            echo mysql_error();
        }
		echo "{\"xCord\":";
		echo $result->fetch_object()->maxX;
		echo ",\"yCord\":";
		$result=mysqli_query($con,"SELECT MAX(yCord) AS maxY FROM GameMap");
        if(!$result)
        {
            echo mysql_error();
        }
		
		echo $result->fetch_object()->maxY;
		echo "}";
		
    }
	
	
	
	
	
	//saved work just in case the above doesn't work
	/*
	function connectX()
    {
		global $login;
        $con = new mysqli($login->host,$login->username,$login->password,$login->db);
        if(!$con)
        {
            echo mysqli_error();
        }
		$result=mysqli_query($con,"SELECT MAX(xCord) AS maxX FROM GameMap");
        if(!$result)
        {
            echo mysql_error();
        }
		
		echo $result->fetch_object()->maxX;
		
    }
	
	function connectY()
    {
		global $login;
        $con = new mysqli($login->host,$login->username,$login->password,$login->db);
        if(!$con)
        {
            echo mysqli_error();
        }
		$result=mysqli_query($con,"SELECT MAX(yCord) AS maxY FROM GameMap");
        if(!$result)
        {
            echo mysql_error();
        }
		
		echo $result->fetch_object()->maxY;
		
    }
	*/
    
	
?>
