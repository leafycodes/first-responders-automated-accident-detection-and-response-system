<?php
session_start();
if (!isset($_SESSION["username"])) {
    header("Location: ../pages/login.php");
    exit();
}

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $location = trim($_POST["location"]);
    $severity = trim($_POST["severity"]);

    if (empty($location) || empty($severity)) {
        header("Location: ../pages/dashboard.php?error=Please fill in all fields");
        exit();
    }

    $report_data = "Location: $location | Severity: $severity | Submitted by: " . $_SESSION["username"] . PHP_EOL;
    file_put_contents("../data/reports.txt", $report_data, FILE_APPEND);

    header("Location: ../pages/dashboard.php");
    exit();
}
?>
