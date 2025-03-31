<?php
session_start();

$reportFile = "../data/reports.txt";
$reports = [];

if (file_exists($reportFile)) {
    $reports = file($reportFile, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
}

if (!empty($reports)) {
    array_pop($reports);
    file_put_contents($reportFile, implode("\n", $reports));
}

header("Location: ../pages/dashboard.php");
exit();
?>
