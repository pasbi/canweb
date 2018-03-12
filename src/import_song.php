
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=2">
	<title>CAN!</title>
	<script src="static/js/jquery-3.3.1.js"></script>
	<script src="static/js/bootstrap.js"></script>
	<link rel="stylesheet" href="static/css/bootstrap.css">

	<?php
	$songId = $_GET['id'];
	$editurl = "view_song.php?" . http_build_query(array('id' => $songId, 'action' => 'edit'));

	$database = new SQLite3('db/can.sqlite') or die('Unable to open database');
	$stmt = $database->prepare("SELECT content, label from songs WHERE songId=:id");
	$stmt->bindValue(':id', $songId, SQLITE3_INTEGER);
	$song = $stmt->execute()->fetchArray();
	$songLabel = $song['label'];
	?>
</head>
<body>
	<nav class="navbar navbar-expand-lg navbar-light bg-faded">
		<button class="navbar-toggler navbar-toggler-right" type="button" data-toggle="collapse" data-target="#mainMenu" aria-controls="mainMenu" aria-expanded="false" aria-label="Toggle navigation">
			<span class="navbar-toggler-icon"></span>
		</button>
		<a class="navbar-brand" href="index.php">CAN</a>

		<div class="collapse navbar-collapse" id="mainMenu">
			<ul class="navbar-nav mr-auto mt-2 mt-md-0">
				<li class="nav-item active">
					<a class="nav-link" href="#" onclick="import(); return false;">Import</a>
				</li>
				<li class="nav-item active">
					<a class="nav-link" href="{$editurl}">Cancel</a>
				</li>
			</ul>
		</div>
	</nav>

	<h1 id='songLabel'>
		<?=$songLabel?>
	</h1>
	<div class="input-group"> 
		<input class="form-control py-2 border-right-0 border" type="search" placeholder="<?=$songLabel;?>"> 
		<div class="input-group-append"> 
			<div class="input-group-text" id="btnGroupAddon2" onclick="alert('search');">
				<i class="glyphicon glyphicon-search"></i>
			</div>
		</div> 
	</div>
	<div class="input-group">
		<input class="form-control"
		placeholder="<?=$songLabel;?>">
		<div class="input-group-addon" ><i class="fa fa-search"></i></div>
	</div>
</body>
</html>
