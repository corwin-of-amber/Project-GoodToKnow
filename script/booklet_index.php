<?php include 'chapters_c.php'; ?>
<?php
$current_chapter = -1;
$total_chapters = count($chapters);
$disabled["all"] = true;
$disabled["prev"] = true;


?>
<?php include '../includes/header_starter.php'; ?>
<?php echo '<title>'.$title.'</title>' ?>
<?php include '../includes/header_ender.php'; ?>
<?php include '../includes/nav.php'; ?>
<?php echo '<h1>'.$title.'</h1>'; ?>
<?php include '../includes/pager.php'; ?>
<?php //include '../includes/regular_collapsees.php' ; ?>
<?php //include '../includes/collapse.php';?>
<?php
$c = array(); //title => file name
$c["<span class=\"fa fa-book\"></span> כל החוברת"] = $pdf_file;
$c["<span class=\"fa fa-list\"></span> פרקים"] = $chapters;
$c["<span class=\"fa fa-info\"></span> נספחים"] = "adds_c.php";
?>

		<div class="accordion" id="accordionExample">
		<?php
		foreach ($c as $c_title => $c_content)
		{
		echo  //button was inside h5
		'
			<div class="card">
			<button class="btn btn-link" type="button" data-toggle="collapse" data-target="#'.$c_content.'" aria-expanded="true" aria-controls="'.$c_content.'">
				<div class="card-header" id="headingOne">
				<h5 class="mb-0">
					'
						.$c_title.
					'
				</h5>
				</div>
			</button>
			';
			
			echo '				<div id="'.$c_content.'" class="collapse" aria-labelledby="headingOne" data-parent="#accordionExample">
				<div class="card-body">';
			if ($c_content == $chapters){
				$i = 0;
				foreach($chapters as $chapter){
					echo '<a class="list-group-item list-group-item-action" href="chapter_'.$i.'.php">'.$chapter.'</a>';
				$i = $i + 1;
				}
			}
			if($c_content == $pdf_file){
				echo '<object data="'.$pdf_file.'" type="application/pdf" width="100%" height="800px"> 
  <p>להורדה לחץ מטה. לקריאה באפליקציה דפדף ברשימת הפרקים<a href="'.$pdf_file.'"><br/>הורדה</a></p>  
 </object>
 ';
			}
				echo '					</div>
				</div>';

		
		}		
		?>
		</div>
<?php include '../includes/pager.php'; ?>
<?php include '../includes/footer.php'; ?>

