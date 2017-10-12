<?php
	require 'Connection.php';
	$login = new Connection;

	$sql = "SELECT * FROM GameMap";

	$rows = 5;
	$cols = 5;

	$gameRows = array();
	
	for($r = 0; $r < $rows; $r++){
		$gameRows[$r] = array();	
	}

	$con = mysqli_connect($login->host,$login->username,$login->password,$login->db);	
	
	$result = $con->query($sql);

	while($row = $result->fetch_assoc()){
		$cell = new Cell;
		$cell->xCord = $row["xCord"];
		$cell->yCord = $row["yCord"];
		$cell->toggled;
		if($row["cellAlive"] == 0)
			$cell->toggled = false;
		else
			$cell->toggled = true;
		$gameRows[$row["yCord"]][$row["xCord"]] = $cell;
	}
	echo json_encode($gameRows);


	class Cell{
		public $xCord;
		public $yCord;
		public $toggled;
	}
	
?>
