<?php

$commend = escapeshellcmd('./main.py');
$output = shell_exec("python3 $commend 66a6873ddb104e19921f39510df1810b");
echo $output;

?>