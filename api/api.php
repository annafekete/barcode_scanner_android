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

// vonalkód paraméter lekérése
$barcode = $_GET['ALKAT'] ?? '';

if (empty($barcode)) {
    echo json_encode(["error" => "Hiányzó vonalkód"]);
    exit;
}

// lekérdezés
$sql = "SELECT HNEV, TAZ FROM teszo WHERE ALKAT = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("s", $barcode);
$stmt->execute();
$result = $stmt->get_result();

$results = [];
while ($row = $result->fetch_assoc()) {
    $results[] = [
        "name" => $row['HNEV'],
        "id" => $row['TAZ']
    ];
}
if (count($results) > 0) {
    echo json_encode([
        "found" => true,
        "items" => $results
    ]);
} else {
    echo json_encode(["found" => false]);
}


$stmt->close();
$conn->close();