<?php
session_start();

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = trim($_POST["username"]);
    $password = trim($_POST["password"]);

    if (empty($username) || empty($password)) {
        header("Location: ../pages/login.php?error=All fields are required!");
        exit();
    }

    $file_path = "../data/users.txt";

    if (!file_exists($file_path)) {
        header("Location: ../pages/login.php?error=Invalid username or password!");
        exit();
    }

    $users = file($file_path, FILE_IGNORE_NEW_LINES);
    foreach ($users as $user) {
        list($stored_username, $stored_password) = explode("|", $user);
        if ($stored_username === $username && password_verify($password, $stored_password)) {
            $_SESSION["username"] = $username;  
            header("Location: ../pages/dashboard.php"); 
            exit();
        }
    }

    header("Location: ../pages/login.php?error=Invalid username or password!");
    exit();
} else {
    header("Location: ../pages/login.php");
    exit();
}
?>
