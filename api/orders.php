<?php
header('Content-Type: application/json');

$host = 'microc.dyndns.org';
$user = 'newuser1';
$password = 'A1024a';
$database = 'luxor';
$port = 35353;

$conn = new mysqli($host, $user, $password, $database, $port);

// ellenorzes
if ($conn->connect_error) {
    die("Kapcsolódási hiba: " . $conn->connect_error);
}

$sql = "SELECT TAZ, ALKAT, HNEV FROM teszo LIMIT 100";
$stmt = $conn->prepare($sql);
if (!$stmt) {
    echo json_encode(["error" => "Hibás lekérdezés: " . $conn->error]);
    exit;
}

$stmt->execute();
$result = $stmt->get_result();

$orders = [];
while ($row = $result->fetch_assoc()) {
    $orders[] = $row;
}

echo json_encode(["orders" => $orders]);

$stmt->close();
$conn->close();
?>