<?php
// sensor.php

// Include the database configuration file using require_once
require_once 'config.php';

// Function to get the latest average sensor data for all sensors
function getLatestSensorData() {
    global $link; // Use the database connection from config.php
    $sensorData = [];

    for ($sensorId = 1; $sensorId <= 3; $sensorId++) {
        $sql = "SELECT * FROM `rawsensor{$sensorId}` ORDER BY `reading_time` DESC LIMIT 1";
        $result = mysqli_query($link, $sql);

        if ($result) {
            $sensorData[$sensorId] = mysqli_fetch_assoc($result);
        } else {
            $sensorData[$sensorId] = null; // Handle the case where there is no data
        }
    }

    return $sensorData;
}

// Get the data for all sensors
$allSensorData = getLatestSensorData();
?>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sensors</title>
 
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
  <link rel="stylesheet" href="./css/main.css">
  <link rel="shortcut icon" href="./img/l1.gif" type="image/x-icon">
</head>
<body style="background-image: url('./image/b1.jpg'); background-size: contain; background-position: center;">
<?php include 'sidebar.php'; ?>

<!-- Your main content goes here -->
<div class="main-content">
    
    <h2 class="mb-4">Sensor Data</h2>
    <table class="table table-bordered">
        <thead class="thead-dark">
            <tr>
                <th scope="col">Sensor</th>
                <th scope="col">Nitrogen</th>
                <th scope="col">Phosphorus</th>
                <th scope="col">Potassium</th>
                <th scope="col">Air Temp</th>
                <th scope="col">Soil Temp</th>
            </tr>
        </thead>
        <tbody>
            <?php foreach ($allSensorData as $sensorId => $data): ?>
                <tr>
                    <th scope="row">BED <?php echo $sensorId; ?></th>
                    <td><?php echo $data ? htmlspecialchars($data['nitrogen']) : 'N/A'; ?></td>
                    <td><?php echo $data ? htmlspecialchars($data['phosphorus']) : 'N/A'; ?></td>
                    <td><?php echo $data ? htmlspecialchars($data['potassium']) : 'N/A'; ?></td>
                    <td><?php echo $data ? htmlspecialchars($data['air_temp']) : 'N/A'; ?></td>
                    <td><?php echo $data ? htmlspecialchars($data['soil_temperature']) : 'N/A'; ?></td>
                </tr>
            <?php endforeach; ?>
        </tbody>
    </table>
</div>

<!-- Bootstrap JS, Popper.js, and jQuery -->
<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>

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