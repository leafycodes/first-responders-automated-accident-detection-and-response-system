<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register</title>
    <link rel="stylesheet" href="../assets/css/register.css">
</head>
<body>

    <div class="container">
        <h2>REGISTER</h2>
        <?php if (isset($_GET['error'])) { ?>
            <p class="error"><?php echo htmlspecialchars($_GET['error']); ?></p>
        <?php } ?>
        <form action="../actions/register_action.php" method="POST">
            <input type="text" name="username" placeholder="Username" required>
            <div class="password-container">
                <input type="password" name="password" id="password" placeholder="Password" required>
                <span id="togglePassword">🔒</span>
            </div>
            <button type="submit">Register</button>
        </form>
        <p>Already have an account? <a href="login.php">Login here</a></p>
    </div>

    <script src="../assets/js/togglePassword.js"></script>
</body>
</html>
