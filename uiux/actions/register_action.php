<?php
session_start();

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = trim($_POST["username"]);
    $password = trim($_POST["password"]);

    if (empty($username) || empty($password)) {
        header("Location: ../pages/register.php?error=All fields are required!");
        exit();
    }

    $file_path = "../data/users.txt";

    if (file_exists($file_path)) {
        $users = file($file_path, FILE_IGNORE_NEW_LINES);
        foreach ($users as $user) {
            list($existing_username, ) = explode("|", $user);
            if ($existing_username === $username) {
                header("Location: ../pages/register.php?error=Username already taken!");
                exit();
            }
        }
    }

    $hashed_password = password_hash($password, PASSWORD_DEFAULT);

    file_put_contents($file_path, "$username|$hashed_password\n", FILE_APPEND);

    header("Location: ../pages/login.php?success=Registration successful! Please log in.");
    exit();
} else {
    header("Location: ../pages/register.php");
    exit();
}
?>
