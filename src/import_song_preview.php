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
	$sourceUrl = $_GET['source-url'];
	$editurl = "view_song.php?" . http_build_query(array('id' => $songId, 'action' => 'edit'));
	$viewurl = "view_song.php?" . http_build_query(array('id' => $songId, 'action' => 'view'));
	$command = escapeshellcmd('./get_pattern.py')
				. " " . escapeshellarg('ultimateguitar')
				. " " . escapeshellarg('get')
				. " " . escapeshellarg($sourceUrl);
	$output = shell_exec($command);
	$data = json_decode($output, true);
	$success = $data['status'] === 'success';
	$pattern = $data['data'];
	?>
	<script type="text/javascript">
		accept = function() {
			$.post('update_song.php', {
				"action": "edit",
				"id": "<?php echo $songId;?>",
				"content": <?php echo json_encode($pattern); ?>
			}, function() {
				window.location = '<?=$viewurl;?>';
			});
		};
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
					<a class="nav-link" href="#" onclick="accept(); return false;">Accept</a>
				</li>
				<li class="nav-item">
					<a class="nav-link" href="#" onclick="history.back();">Cancel</a>
				</li>
			</ul>
		</div>
	</nav>

	<div>
		<?php
		$command = escapeshellcmd('./format_pattern.py')
			. " " . escapeshellarg($pattern);
		$output = shell_exec($command);
		echo $output;
		?>
	</div>
</body>
</html>
 