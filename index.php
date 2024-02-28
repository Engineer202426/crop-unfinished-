<?php
# Initialize the session
session_start();

# If user is not logged in then redirect him to login page
if (!isset($_SESSION["loggedin"]) || $_SESSION["loggedin"] !== TRUE) {
  echo "<script>" . "window.location.href='./login.php';" . "</script>";
  exit;
}
?>

<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>User login system</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous">
  <link rel="stylesheet" href="./css/main.css">
  <link rel="shortcut icon" href="./img/l1.gif" type="image/x-icon">
</head>

<body>
<?php include 'sidebar.php'; ?>

<!-- Your main content goes here -->
<div class="main-content">
  
<!-- GLORI!!!!!!!!!!!!! DIDTOY KA AG ARAMID NEW CONTENT -->
































</div>

<!-- Optionally, include your JavaScript here -->
<script src="script.js"></script>
</body>

</html>
<style>
    .main-content {
    margin-left: 250px; /* Same as the width of your sidebar */
    padding: 1em;
}

@media screen and (max-width: 768px) {
    .main-content {
        margin-left: 0; /* On smaller screens, the sidebar could be hidden or toggleable */
    }
}
</style>