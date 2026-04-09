<?php
$secret_key = '$2b$12$Uxhp07rn8gcbay2ncjffgOAv7BrAw55lQcCQw.LTSNHHvcByEui3W'; //da cambiare per ogni cliente

if(!isset($_GET['key']) || $_GET['key'] !== $secret_key){
    header('HTTP/1.1 403 Forbidden');
    exit('Access Denied');
}


$report = [
    "status" => "OK",
    "php_version" => PHP_VERSION,
    "disk_free"=>round(disk_free_space("/")),
    "disk_total"=>round(disk_total_space("/")),
    "db_status"=>"Not Checked"
];

header('Content-Type: application/json');
echo json_encode($report);