<?php
	require 'Connection.php';
	$login = new Connection;
	$xToggle = $POST_['xCord']; //int representing x cordinate to toggle
	$yToggle = $POST_['yCord']; //int representing y cordinate to toggle
	$n->connect();
	$n->insert($xToggle, $yToggle);
	

class db
{
    public $con;
	   
    public function connect()
    {
        $this->con = new mysqli($login->host,$login->username,$login->password,$login->db);
        if(!$this->con)
        {
            echo mysqli_error();
        }

    }
    public function insert($xToggle,$yToggle)
    {
        $sql=mysqli_query($this->con,"INSERT INTO CommitQueue(xCord, yCord) VALUES('$xToggle', '$yToggle')");
        if(!$sql)
        {
            echo mysql_error();
        }
    }
}
	
?>