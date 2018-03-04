
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=2">
	<title>CAN!</title>
	<script src="static/js/jquery-3.3.1.js"></script>
	<script src="static/js/bootstrap.js"></script>
	<link rel="stylesheet" href="static/css/bootstrap.css">

	<script> 
		$(function(){
			$("#myNavbar").load("navbar_index.html"); 
		});
		function viewSong(songId) {
			window.location = "view_song.php?" + $.param({ "id": songId, "action": "view" });
		}
	</script>
</head>
<body>
	<?php 
	$database = new SQLite3('db/can.sqlite') or die('Unable to open database');
	?>
	<div id="myNavbar"></div>
	<div class="container">
		<h1>Song Database:</h1>
		<ul class="list-group">
			<?php
			$stmt = $database->prepare("SELECT SongId, label FROM songs");
			$result = $stmt->execute();
			while ($row = $result->fetchArray()) {
				echo "<li class='list-group-item' 'clearfix' onclick='viewSong({$row['SongId']})'>{$row['label']}</li>\n";
			}
			?>
		</ul>
	</div>
</body>
</html>

