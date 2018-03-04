<?php
	$database = new SQLite3('db/can.sqlite') or die('Unable to open database');
	$stmt = $database->prepare("INSERT INTO songs (label) VALUES (null);");
	$result = $stmt->execute();

	$id = $database->lastInsertRowID();
	$query = array( 'id' => $id, 
					'action' => 'edit' );
	$url = "view_song.php?" . http_build_query($query);
	header('Location: ' . $url);


?>