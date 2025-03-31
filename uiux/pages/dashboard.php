<?php
session_start();
if (!isset($_SESSION['username'])) {
    header("Location: login.php");
    exit();
}

$reportFile = "../data/reports.txt";
$reports = [];

if (file_exists($reportFile)) {
    $reports = file($reportFile, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
}

function parseReport($report)
{
    $parts = explode(" | ", $report);
    return [
        'location'  => isset($parts[0]) ? substr($parts[0], 9) : "N/A",
        'severity'  => isset($parts[1]) ? substr($parts[1], 10) : "N/A",
        'timestamp' => isset($parts[2]) ? substr($parts[2], 10) : "N/A",
    ];
}

$incident = !empty($reports) ? parseReport(end($reports)) : ['location' => "N/A", 'severity' => "N/A", 'timestamp' => "N/A"];
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
    <link rel="stylesheet" href="../assets/css/dashboard.css">
    <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
</head>
<body>

<header>
    <h2>Accident Response System</h2>
    <a href="../actions/logout_action.php" class="logout-btn">Logout</a>
</header>

<div class="container">
    <h1 class="dashboard-title">Dashboard</h1>
    <p class="welcome-msg">Welcome, <b><?php echo $_SESSION['username']; ?></b></p>

    <div class="grid">
        <div class="left-column">
            <div class="card">
                <h3>Accident Details</h3>
                <p><strong>Location:</strong> <?php echo $incident['location']; ?></p>
                <p><strong>Severity:</strong> <?php echo $incident['severity']; ?></p>
                <p><strong>Timestamp:</strong> <?php echo $incident['timestamp']; ?></p>
            </div>

            <div class="card">
                <h3>Live Accident Updates</h3>
                <div id="map"></div>
            </div>
        </div>

        <div class="right-column">
            <div class="card">
                <h3>Actions</h3>
                <button onclick="confirmIncident()" class="btn blue">Confirm Incident</button>
                <form action="../actions/dismiss_action.php" method="POST">
                    <button type="submit" class="btn blue">Dismiss False Positive</button>
                </form>
            </div>

            <div class="card">
    <h3>Recent Reports</h3>
    <ul class="report-list">
        <?php
        foreach ($reports as $report) {
            echo "<li>$report</li>";
        }
        ?>
    </ul>
</div>

            <div class="card">
                <h3>Emergency Contact Info</h3>
                <p>Helpline: 112 | Local Authorities: 100</p>
                <a href="report.php" class="btn blue" style="text-decoration:none;">Submit Report</a>
            </div>

            <div class="card">
                <h3>Video Section</h3>
                <a href="video.php" class="btn blue" style="text-decoration:none;">Go to Videos</a>
            </div>
        </div>
    </div>
</div>

<script>
    function confirmIncident() {
        alert("Incident has been confirmed!");
    }

    var map = L.map('map').setView([20.2961, 85.8245], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);
</script>

</body>
</html>
