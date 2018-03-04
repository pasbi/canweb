<?php
	$database = new SQLite3('db/can.sqlite') or die('Unable to open database');
	// , content=:content, youtubeid=:yid, spotifyid:sid 
	if ($_POST['action'] == 'edit') {
		$stmt = $database->prepare("UPDATE songs SET label=:label, content=:content WHERE songId=:id");
		$stmt->bindValue(':id', $_POST['id'], SQLITE3_INTEGER);
		$stmt->bindValue(':label', $_POST['label'], SQLITE3_TEXT);
		$stmt->bindValue(':content', $_POST['content'], SQLITE3_TEXT);
		$result = $stmt->execute();
	} else if ($_POST['action'] == 'remove') {
		$stmt = $database->prepare("DELETE FROM songs WHERE songId=:id");
		$stmt->bindValue(':id', $_POST['id'], SQLITE3_INTEGER);
		$result = $stmt->execute();
	}
	echo "hjkuy";
?>