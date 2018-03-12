
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=2">
	<title>CAN!</title>
	<link rel="stylesheet" type="text/css" href="static/css/bootstrap.css">
	<link rel="stylesheet" type="text/css" href="static/css/snackbar.css">
	<script src="static/js/jquery-3.3.1.js"></script>
	<script src="static/js/bootstrap.js"></script>
	<script src="static/js/snackbar.js"></script>

	<script> 
		function viewSong(songId) {
			window.location = "view_song.php?" + $.param({ "id": songId, "action": "view" });
		}
	</script>
</head>
<body>

	<nav class="navbar navbar-expand-lg navbar-dark bg-primary">
		<button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarColor01" aria-controls="navbarColor01" aria-expanded="false" aria-label="Toggle navigation">
			<span class="navbar-toggler-icon"></span>
		</button>
		<a class="navbar-brand" href="index.php">CAN</a>
		<div class="collapse navbar-collapse" id="mainMenu">
			<ul class="navbar-nav mr-auto">
				<li class="nav-item">
					<a class="nav-link" href="create_song.php">New Song</a>
				</li>
				<li class="nav-item">
					<a class="nav-link" href="#" onclick="showSnackbar('snackbar');">TEST</a>
				</li>
			</ul>
		</div>
	</nav>

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

