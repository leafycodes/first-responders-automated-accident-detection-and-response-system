<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $location = $_POST['location'];
    $severity = $_POST['severity'];
    $timestamp = date("Y-m-d H:i:s");

    $report = "Location: $location | Severity: $severity | Timestamp: $timestamp\n";

    $filePath = "../data/reports.txt";

    $absolutePath = realpath($filePath);
    echo "Debug: Absolute Path: " . $absolutePath . "<br>";

    if (file_exists($filePath) && is_writable($filePath)) {
        file_put_contents($filePath, $report, FILE_APPEND);
        header("Location: dashboard.php?message=Report%20Submitted");
        exit();
    } else {
        echo "Error: Unable to write to the file. Check file permissions or path.";
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Submit Report</title>
    <link rel="stylesheet" href="../assets/css/report.css">
</head>
<body>

    <header>
        <h2>Accident Response System</h2>
        <a href="../actions/logout_action.php" class="logout-btn">Logout</a>
    </header>

    <div class="container">
        <h1>Submit Accident Report</h1>
        <form action="" method="POST">
            <label>Location:</label>
            <input type="text" name="location" required>
            
            <label>Severity:</label>
            <select name="severity" required>
                <option value="Low">Low</option>
                <option value="Medium">Medium</option>
                <option value="High">High</option>
            </select>
            
            <button type="submit" class="btn confirm">Submit Report</button>
        </form>

        <a href="dashboard.php" class="btn back-btn">Go Back to Dashboard</a>
    </div>

</body>
</html>