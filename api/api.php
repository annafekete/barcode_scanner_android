<?php
header('Content-Type: application/json');

// DB kapcsolat
$conn = new mysqli("localhost", "root", "", "raktar_db");
if ($conn->connect_error) {
    echo json_encode(["error" => "DB kapcsolat hiba"]);
    exit;
}

// vonalkód paraméter lekérése
$barcode = $_GET['barcode'] ?? '';

if (empty($barcode)) {
    echo json_encode(["error" => "Hiányzó vonalkód"]);
    exit;
}

// lekérdezés
$sql = "SELECT name, owner FROM products WHERE barcode = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("s", $barcode);
$stmt->execute();
$result = $stmt->get_result();

if ($row = $result->fetch_assoc()) {
    echo json_encode([
        "found" => true,
        "name" => $row['name'],
        "owner" => $row['owner']
    ]);
} else {
    echo json_encode(["found" => false]);
}

$stmt->close();
$conn->close();
