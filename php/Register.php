<?php
	$con = mysqli_connect("localhost", "root", "438520", "fbtpduf");	
	
	$userID = $_POST["userID"];
	$userPassword = $_POST["userPassword"];
	$userDepartment = $_POST["userDepartment"];

	
	$statement = mysqli_prepare($con, "INSERT INTO user VALUES (?,?,?)");
	mysqli_stmt_bind_param($statement, "sss", $userID, $userPassword, $userDepartment);
	mysqli_stmt_execute($statement);
	
	$response = array();
	$response["success"] = true;
	
	echo json_encode($response);
?>
	