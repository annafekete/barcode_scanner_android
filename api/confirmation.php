<?php
header('Content-Type: application/json');

//DB kapcsolat
$conn = new mysqli("localhost", "root", "", "raktar_db");
if ($conn->connect_error) {
    echo json_encode(["success"=> false , "error" => "DB kapcsolat hiba"]);
    exit;
}

$barcode = $_POST['barcode'] ?? '';

if (empty($barcode)) {
    echo json_encode(["success" => false , "error" => "Hiányzó vonalkód"]);
    exit;
}

$stmt = $conn->prepare("UPDATE products SET status = 'done' WHERE barcode = ?");
$stmt->bind_param("s", $barcode);
$success = $stmt->execute();

if ($success && $stmt->affected_rows > 0) {
    echo json_encode(["success" => true]);
} else {
    echo json_encode(["success" => false, "error" => "Nem található vagy már kész"]);
}

$stmt->close();
$conn->close();