<?php 

$command = escapeshellcmd('python ApiWorked.py');
$output = shell_exec($command);
echo $output;

?>
