<?php
	echo "HELLO";
	$database = new SQLite3('db/can.sqlite') or die('Unable to open database');
	echo $_POST['action'];

	if ($_POST['action'] === 'edit') {
		echo "kkk";
		// define expected keys and types.
		// You may want to add custom pairs here
		// remeber that $key must be a column in the database
		// also, $key should be a key in $_POST
		$song_set_keys = [
			'label' => SQLITE3_TEXT, 
			'content' => SQLITE3_TEXT 
		];

		// filter $_POST according to the whitelist above.
		// This is 1st for security reasons and 2nd to filter
		// the command ('action' => 'edit')
		$values = array_filter(
			$_POST, 
			function ($key) use ($song_set_keys) {
				return array_key_exists($key, $song_set_keys);
			},
			ARRAY_FILTER_USE_KEY
		);

		// $values = [
		// 	'content' => 'some content Em',
		// 	'label' => 'new label'
		// ];
	
		// build the statement
		$stmt = array();
		foreach ($values as $key => $value) {
			array_push($stmt, $key . "=:" . $key);
		}
		$stmt = "UPDATE songs SET " . implode(", ", $stmt) . " WHERE songId=:id";
		$stmt = $database->prepare($stmt);
		foreach ($values as $key => $value) {
			$stmt->bindValue(":" . $key, $value, $song_set_keys[$key]);
		}
		$stmt->bindValue(':id', $_POST['id'], SQLITE3_INTEGER);

		// exec the statement
		$result = $stmt->execute();

	} else if ($_POST['action'] === 'remove') {
		echo "A";
		$stmt = $database->prepare("DELETE FROM songs WHERE songId=:id");
		echo "B";
		$stmt->bindValue(':id', $_POST['id'], SQLITE3_INTEGER);
		echo "C";
		$result = $stmt->execute();
		echo "D";
	}
?>