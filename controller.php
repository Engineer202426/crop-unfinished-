<?php
// Filename: controller.php

$filename = 'interval_setting.txt';


// Function to convert hours to milliseconds
function hoursToMilliseconds($hours) {
    return $hours * 3600000;
}


// If it's a POST request, update the interval setting
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['interval'])) {
    $interval = intval($_POST['interval']);
    // Ensure the interval is within the allowed range (1 min to 8 hours)
    $interval = max(60000, min($interval, 28800000));
    file_put_contents($filename, $interval);

    // Redirect back to the slider interface after setting the interval
    header('Location: deploy.php');
    exit();
}

// For a GET request, return the current interval
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    if (file_exists($filename)) {
        $currentInterval = intval(file_get_contents($filename));
    } else {
        // Default to 1 minute if not set
        $currentInterval = 60000;
    }
    echo $currentInterval;

    // Setting default interval based on the GET parameter 'default'
    if (isset($_GET['default'])) {
        $defaultInterval = intval($_GET['default']);
        if ($defaultInterval >= 1 && $defaultInterval <= 8) {
            $currentInterval = hoursToMilliseconds($defaultInterval);
            file_put_contents($filename, $currentInterval);
        }
    }
}
?>
