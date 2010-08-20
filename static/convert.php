<?php

$svg = $_POST['svg'];
$fh = fopen('/tmp/tmp.svg', 'w');
fwrite($fh, $svg);
fclose($fh);

system('perl convert.pl');
