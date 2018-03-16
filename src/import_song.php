<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=2">
	<title>CAN!</title>
	<link rel="stylesheet" type="text/css" href="static/css/bootstrap.css">
	<link rel="stylesheet" type="text/css" href="static/css/snackbar.css">
	<link rel="stylesheet" type="text/css" href="static/css/loader.css">
	<script type="text/javascript" src="static/js/jquery-3.3.1.js"></script>
	<script type="text/javascript" src="static/js/bootstrap.js"></script>
	<script type="text/javascript" src="static/js/snackbar.js"></script>
	<script type="text/javascript" src="static/js/import_song.js"></script>
	<?php
	$songId = $_GET['id'];
	$editurl = "view_song.php?" . http_build_query(array('id' => $songId, 'action' => 'edit'));
	$viewurl = "view_song.php?" . http_build_query(array('id' => $songId, 'action' => 'view'));

	$database = new SQLite3('db/can.sqlite') or die('Unable to open database');
	$stmt = $database->prepare("SELECT content, label from songs WHERE songId=:id");
	$stmt->bindValue(':id', $songId, SQLITE3_INTEGER);
	$song = $stmt->execute()->fetchArray();
	$songLabel = $song['label'];
	$query = $_GET['query'];
	$command = escapeshellcmd('./search.py')
	 			. " " . escapeshellarg('ultimateguitar')
	 			. " " . escapeshellarg($query);
	$output = shell_exec($command);
	$result_items = json_decode($output, true);
	?>
	<script type="text/javascript">
		$(document).ready(function() {
			$("#search-chords-button").click(function () {
				var query = $("#search-chord-input").val();
				query = "query=" + encodeURIComponent(query) + "&action=search&id=" + encodeURIComponent("" + <?=$songId?>)
				url = "http://localhost/can/import_song.php?" + query;
				$("#results-pane").html("<div class='loader'></div>")
				window.location.assign(url)
			});
			$(".song-row").click(function() {
				window.location = $(this).data("href");
			});
		});
	</script>
</head>
<body>
	<nav class="navbar navbar-expand-lg navbar-dark bg-primary">
		<button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#mainMenu" aria-controls="mainMenu" aria-expanded="false" aria-label="Toggle navigation">
			<span class="navbar-toggler-icon"></span>
		</button>
		<a class="navbar-brand" href="index.php">CAN</a>
		<div class="collapse navbar-collapse" id="mainMenu">
			<ul class="navbar-nav mr-auto">
				<li class="nav-item">
					<a class="nav-link" href="#" onclick="import(); return false;">Import</a>
				</li>
				<li class="nav-item">
					<a class="nav-link" href="<?=$viewurl?>">Cancel</a>
				</li>
			</ul>
		</div>
	</nav>

	<div class="input-group">
		<input type="text" class="form-control" id="search-chord-input" placeholder="Search for..." value="<?=$query?>">
		<span class="input-group-btn">
			<button class="btn btn-secondary" id="search-chords-button" type="button">Go!</button>
		</span>
	</div>

	<div id='results-pane'>
		<?php
		if ($result_items['status'] != 'success') {
			echo "<div> Request Failed! Status: " . $result_items['status'] . "</div>";
		} else {
			$result_items = $result_items['data'];
			echo "<table class='table table-dark'>";
			echo "<thead style='display:none'>";
			echo "<th scope='col'>Song</th>";
			echo "<th scope='col'>Artist</th>";
			echo "<th scope='col'>rating</th>";
			echo "</thead>";
			echo "<tbody>";
			foreach ($result_items as $item) {
				$url = "import_song_preview.php?" 
					. http_build_query(array(
						"source-url" => $item['url'],
						"id" => $songId
					));
				echo "<tr class='song-row' data-href='" . $url . "'>";
				echo "<td>" . $item['song_name'] . "</td>";
				echo "<td>" . $item['artist_name'] . "</td>";
				echo "<td>" . $item['rating'] . "</td>";
				echo "</tr>";
			}
			echo "</tbody>";
			echo "</table>";
		}
		?>
	</div>
</body>
</html>
 