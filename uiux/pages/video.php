<?php
session_start();
if (!isset($_SESSION['username'])) {
    header("Location: login.php");
    exit();
}

$videoDir = "../../cctv/feeder_videos"; 
$absolutePath = realpath($videoDir); 

echo "Debug: Absolute Path: " . $absolutePath . "<br>"; 

$specificVideos = [
    'cam1_22032025_1_1718.mp4',
    'cam1_22032025_2_0228.mp4',
    'cam1_22032025_3_1752.mp4'
];

$videos = [];

if (is_dir($absolutePath)) {
    foreach ($specificVideos as $video) {
        $videoPath = $absolutePath . '/' . $video;
        if (file_exists($videoPath)) {
            $videos[] = $video;
        } else {
            echo "Debug: Video not found: " . $video . "<br>"; 
        }
    }
} else {
    echo "Debug: Directory does not exist: " . $absolutePath . "<br>"; 
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Section</title>
    <link rel="stylesheet" href="../assets/css/video.css">
</head>
<body>

<header>
    <h2>Accident Response System</h2>
    <a href="../actions/logout_action.php" class="logout-btn">Logout</a>
</header>

<div class="container">
    <h1 class="video-title">Video Section</h1>
    <p class="welcome-msg">Welcome, <b><?php echo $_SESSION['username']; ?></b></p>

    <a href="dashboard.php" class="btn back-btn">Go Back to Dashboard</a>

    <div class="video-grid">
        <?php if (!empty($videos)): ?>
            <?php foreach ($videos as $video): ?>
                <div class="video-card">
                    <div class="video-thumbnail">
                        <video controls width="100%">
                            <source src="<?php echo $videoDir . '/' . $video; ?>" type="video/mp4">
                            Your browser does not support the video tag.
                        </video>
                    </div>
                    <h3><?php echo $video; ?></h3>
                </div>
            <?php endforeach; ?>
        <?php else: ?>
            <p>No videos found in <?php echo $videoDir; ?>.</p>
        <?php endif; ?>
    </div>
</div>

</body>
</html>