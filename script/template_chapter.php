<?php
$current_chapter = replace_num
$total_chapters = replace_total
$booklet_name = "booklet_name";
$chapter_name = "replace_name"
?>
<?php include '../includes/header_starter.php'; ?>
<link href="css/idGeneratedStyles.css" rel="stylesheet" type="text/css" />
<?php
echo '<title> ??? '.$current_chapter.' - '.$chapter_name.'</title>';
?>
<?php include '../includes/header_ender.php'; ?>
<?php include '../includes/nav.php'; ?>
<?php include '../includes/pager.php'; ?>
<div class="container">
<?php include 'content_chapter '.$current_chapter.'.php'; ?>
</div>
<?php include '../includes/pager.php'; ?>
<?php include '../includes/footer.php'; ?>
