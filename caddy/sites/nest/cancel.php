<?php
require_once('creds.php');
require_once('nest-php-api.php');

$date = new DateTime();
$str_date = $date->format('Y-m-d H:i:s');
// Check if a key has been sent?
if (empty($_GET['key'])) {
	$return = json_encode( array("error"=>array( "code"=>401, "text"=>"Access Denied", "message"=>"The key was missing" )));
}
// If it has check if it is correct
else if ($_GET['key']==$access_key) {
	$nest = new Nest($nest_username,$nest_password);
	$return = $nest->setHotWaterBoost(0);
}
//If not correct one has been passed but it is wrong
else {
	$return = json_encode( array("error"=>array( "code"=>401, "text"=>"Access Denied", "message"=>"The key was wrong" )));
}

// return json response and log to testing file
echo $return;
