<?php
session_start();
session_destroy();
header("Location: ../pages/index.php?success=Logged out successfully!");
exit();
?>
