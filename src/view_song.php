
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=2">
	<title>CAN!</title>
	<script type="text/javascript" src="./static/js/jquery-3.3.1.js"></script>
	<script type="text/javascript" src="./static/js/bootstrap.js"></script>
	<script type="text/javascript" src="./static/js/snackbar.js"></script>
	<link rel="stylesheet" href="./static/css/bootstrap.css">
	<link rel="stylesheet" href="./static/css/snackbar.css">
	<link rel="stylesheet" href="./static/css/contenteditable_placeholder.css">
	<link rel="stylesheet" href="./static/css/chordeditarea.css">

	<?php
	$action = $_GET['action'];
	$songId = $_GET['id'];
	$editurl = "view_song.php?" . http_build_query(array('id' => $songId, 'action' => 'edit'));
	$viewurl = "view_song.php?" . http_build_query(array('id' => $songId, 'action' => 'view'));	

	$database = new SQLite3('db/can.sqlite') or die('Unable to open database');
	$stmt = $database->prepare("SELECT content, label from songs WHERE songId=:id");
	$stmt->bindValue(':id', $songId, SQLITE3_INTEGER);
	$song = $stmt->execute()->fetchArray();
	$songLabel = $song['label'];
	$songContent = $song['content'];

	switch ($action) {
		case "edit":
		case "create":
			$contentPlaceholder = "placeholder='Enter Chords'";
			$labelPlaceholder = "placeholder='Enter Song Label'";
			$contenteditable = "contenteditable='true'";
			break;
		case "view":
			$labelPlaceholder = "";
			$contentPlaceholder = "";
			$contenteditable = "";
			if ($songContent == "") {
				$songContent = "empty";
			}
			if ($songLabel == "") {
				$songLabel = "Unnamed Song";
			}
			break;
	}
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
				"content": $("#contentArea").val()
			}, function() {
				window.location = '<?=$viewurl;?>';
			}).fail(function() {
			});
		}
		function remove() {
			$.post('update_song.php', {
				"action": "remove",
				"id": "<?=$songId;?>",
			}, function(msg) {
				window.location = 'index.php';
			});
		}
		function importSong() {
			var query = $("#songLabel").text();
			query = "query=" + encodeURIComponent(query) 
					+ "&action=search"
					+ "&id=" + encodeURIComponent("<?=$songId?>");
			var importsongurl = "import_song.php?" + query
			window.location = importsongurl;
		}
		window.onload = function () {
			// no line break in song-label
			$("#songLabel").keypress(function(e){ return e.which != 13; });
		}
		openAlert = function () {
			$('#passwordsNoMatchRegister').slideDown();
		}
		$(function($){
		    $("[contenteditable]").focusout(function(){
		        var element = $(this);        
		        if (!element.text().trim().length) {
		            element.empty();
		        }
		    });
		});
		function auto_grow(element) {
			element.style.height = "5px";
			element.style.height = (element.scrollHeight + 10)+"px";
		}
		$("document").ready(function() {
			auto_grow($('#contentArea')[0])
		});


	</script> 
</head>
<body>
	<nav class="navbar navbar-expand-lg navbar-dark bg-primary">
		<button class="navbar-toggler navbar-toggler-right" type="button" data-toggle="collapse" data-target="#mainMenu" aria-controls="mainMenu" aria-expanded="false" aria-label="Toggle navigation">
			<span class="navbar-toggler-icon"></span>
		</button>
		<a class="navbar-brand" href="index.php">
			<?php
				switch ($action) {
					case 'edit':
						echo "Edit";
						break;
					case 'create':
						echo "Create";
						break;
					case 'view':
						echo "View";
						break;
					default:
						alert("error");
				}
			?>
		</a>

		<div class="collapse navbar-collapse" id="mainMenu">
			<ul class="navbar-nav mr-auto mt-2 mt-md-0">
			<?php
				switch ($action) {
					case 'edit':
						echo <<< EOD
						<li class="nav-item">
							<a class="nav-link" href="#" onclick="submit(); return false;">Submit</a>
						</li>
						<li class="nav-item">
							<a class="nav-link" href="{$viewurl}">Cancel</a>
						</li>
						<li class="nav-item">
							<a class="nav-link" href="#" onclick="remove();">Remove</a>
						</li>
						<li class="nav-item">
							<a class="nav-link" href="#" onclick="importSong(); return false">Import</a>
						</li>
EOD;
						break;
					case 'create':
						echo <<< EOD
						<li class="nav-item">
							<a class="nav-link" href="#" onclick="submit(); return false;">Submit</a>
						</li>
						<li class="nav-item">
							<a class="nav-link" href="#" onclick="remove(); return false;">Cancel</a>
						</li>
						<li class="nav-item">
							<a class="nav-link" href="#" onclick="importSong(); return false";">Import</a>
						</li>
EOD;
						break;
					case 'view':
						echo <<< EOD
						<li class="nav-item">
							<a class="nav-link" href={$editurl}>Edit</a>
						</li>
EOD;
						break;
					default:
						alert("error");
				}
			?>
			</ul>
		</div>
	</nav>

	<div class='panel panel-default'>
		<!-- do not introduce whitespace or newline -->
		<h1 id='songLabel' <?=$contenteditable?> <?=$labelPlaceholder?>><?=$songLabel?></h1>
	</div>
	<hr>
	<div class='panel panel-default'><?php
			if ($action === 'view') {
				$command = escapeshellcmd('./format_pattern.py')
					. " " . escapeshellarg($songContent);
				$output = shell_exec($command);
				echo $output;
			} else {
			    // do not introduce whitespace or newline
				echo "<textarea type='text' class='chordeditarea' id='contentArea' onkeyup='auto_grow(this)'>" . $songContent . "</textarea>";
			}
			?></div>

</body>
</html>

