<?php
$host = 'microc.dyndns.org';
$port = 35353;
$user = 'newuser1';
$password = 'A1024a';
$database = 'raktar_db';  // majd ide kerul az adatb neve

$conn = new mysqli($host, $user, $password, $database, $port);

// ellenorzes
if ($conn->connect_error) {
    die("Kapcsolódási hiba: " . $conn->connect_error);
}

echo "Sikeres kapcsolat!";
$conn->close();
?>
