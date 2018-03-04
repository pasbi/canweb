
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
	$action = $_GET['action'];
	$songId = $_GET['id'];
	$editurl = "view_song.php?" . http_build_query(array('id' => $songId, 'action' => 'edit'));
	$viewurl = "view_song.php?" . http_build_query(array('id' => $songId, 'action' => 'view'));	
	$removeurl = "update_song.php?" . http_build_query(array('id' => $songId, 'action' => 'remove'));

	$database = new SQLite3('db/can.sqlite') or die('Unable to open database');
	$stmt = $database->prepare("SELECT content, label from songs WHERE songId=:id");
	$stmt->bindValue(':id', $songId, SQLITE3_INTEGER);
	$song = $stmt->execute()->fetchArray();
	$songLabel = $song['label'];
	$songContent = $song['content'];
	$contentEditable = $action === 'edit' ? 'contenteditable="true"' : '';

	?>

	<script> 
		$(function(){
			$("#myNavbar").load("navbar_edit_song.html"); 
		});
		function submit() {
			$.post('update_song.php', {
				"action": "edit",
				"label": $("#songLabel").text(),
				"id": "<?php echo $songId;?>",
				"content": $("#contentArea").html()
			}, function(msg) {
				window.location = '<?=$viewurl;?>';
			});
		}
		function remove() {
			$.post('update_song.php', {
				"action": "remove",
				"id": "<?php echo $songId;?>",
			}, function(msg) {
				window.location = 'index.php';
			});
		}
	</script> 
</head>
<body>

	<nav class="navbar navbar-expand-lg navbar-light bg-faded">
		<button class="navbar-toggler navbar-toggler-right" type="button" data-toggle="collapse" data-target="#mainMenu" aria-controls="mainMenu" aria-expanded="false" aria-label="Toggle navigation">
			<span class="navbar-toggler-icon"></span>
		</button>
		<a class="navbar-brand" href="index.php">CAN</a>

		<div class="collapse navbar-collapse" id="mainMenu">
			<ul class="navbar-nav mr-auto mt-2 mt-md-0">
			<?php
				if ($action == 'edit') {
					echo <<< EOD
					<li class="nav-item active">
						<a class="nav-link" href="#" onclick="submit(); return false;">Submit</a>
					</li>
					<li class="nav-item active">
						<a class="nav-link" href="{$viewurl}">Cancel</a>
					</li>
					<li class="nav-item active">
						<a class="nav-link" href="#" onclick="remove(); return false;">Remove</a>
					</li>
					<li class="nav-item active">
						<a class="nav-link" href="#" onclick="import(); return false;">Import</a>
					</li>
EOD;
				} else {					
					echo <<< EOD
					<li class="nav-item active">
						<a class="nav-link" href={$editurl}>Edit</a>
					</li>
EOD;
				}
			
			?>
			</ul>
		</div>
	</nav>

	<h1 id='songLabel' <?=$contentEditable;?>>
		<?=$songLabel?>
	</h1>
	<div id='contentArea' <?=$contentEditable;?>>
		<?=$songContent;?>
	</div>

</body>
</html>

