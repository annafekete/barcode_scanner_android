<?php
header('Content-Type: application/json');

// DB kapcsolat
$conn = new mysqli("localhost", "root", "", "raktar_db");
if ($conn->connect_error) {
    echo json_encode(["error" => "DB kapcsolat hiba"]);
    exit;
}

// paraméter ellenőrzés
$direction = $_GET['direction'] ?? 'outgoing';

// lekérdezés
$sql = "SELECT barcode, name, owner FROM products WHERE direction = ? AND status = 'pending'";
$stmt = $conn->prepare($sql);
$stmt->bind_param("s", $direction);
$stmt->execute();
$result = $stmt->get_result();

$orders = [];
while ($row = $result->fetch_assoc()) {
    $orders[] = $row;
}

echo json_encode(["orders" => $orders]);

$stmt->close();
$conn->close();