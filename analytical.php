<?php
// Include the database configuration file
require_once 'config.php';

// Initialize arrays to hold the data for each column
$all_air_temp = array();
$all_soil_temperature = array();
$all_nitrogen = array();
$all_phosphorus = array();
$all_potassium = array();

// Query the database to get the data for all columns
$query = "SELECT all_air_temp, all_soil_temperature, all_nitrogen, all_phosphorus, all_potassium FROM overall_data";
$result = $link->query($query);

if ($result) {
    // Fetch the data and store it in their respective arrays
    while ($row = $result->fetch_assoc()) {
        $all_air_temp[] = $row['all_air_temp'];
        $all_soil_temperature[] = $row['all_soil_temperature'];
        $all_nitrogen[] = $row['all_nitrogen'];
        $all_phosphorus[] = $row['all_phosphorus'];
        $all_potassium[] = $row['all_potassium'];
    }
    $result->free();
}

$link->close();

// Now you can pass these arrays to JavaScript as before and use them to create Highcharts
?>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Analyticals</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous">
  <link rel="stylesheet" href="./css/main.css">
  <link rel="shortcut icon" href="./img/l1.gif" type="image/x-icon">
    
    <script src="https://code.highcharts.com/highcharts.js"></script>
</head>
<body>
<?php include 'sidebar.php'; ?>

<div class="main-content">
    <!-- Container for the Highcharts graph -->

    <div class="row">
        <div class="col-lg-4">
            <div id="airTempChart" style="height: 400px;" class="chart-container"></div> 
        </div>

        <div class="col-lg-4">
            <div id="soilTempChart" style="height: 400px;" class="chart-container"></div> 
        </div>
        <div class="col-lg-4">
            <div id="nitrogenChart" style="height: 400px;" class="chart-container"></div> 
        </div>
        <div class="col-lg-4">
            <div id="phosphorusChart" style="height: 400px;" class="chart-container"></div> 
        </div>
        <div class="col-lg-4">
            <div id="potassiumChart" style="height: 400px;" class="chart-container"></div> 
        </div>
        
    </div>

    <script>
    // Pass PHP array to JavaScript
    var airTempData = <?php echo json_encode($all_air_temp); ?>;
    
    Highcharts.chart('airTempChart', {
        chart: {
            type: 'line'
        },
        title: {
            text: 'Air Temperature Over Time'
        },
        xAxis: {
            // Optionally, add categories or labels if necessary, e.g., timestamps
        },
        yAxis: {
            title: {
                text: 'Temperature (°C)'
            }
        },
        series: [{
            name: 'Air Temperature',
            data: airTempData.map(Number) // Ensure data is in Number format
        }]
    });


    var soilData = <?php echo json_encode($all_soil_temperature); ?>;
    
    Highcharts.chart('soilTempChart', {
        chart: {
            type: 'line'
        },
        title: {
            text: ' Soil Temperature Over Time'
        },
        xAxis: {
            // Optionally, add categories or labels if necessary, e.g., timestamps
        },
        yAxis: {
            title: {
                text: 'Temperature (°C)'
            }
        },
        series: [{
            name: 'Soil Temperature',
            data: soilData.map(Number) // Ensure data is in Number format
        }]
    });

    var nitrogenData = <?php echo json_encode($all_nitrogen); ?>;
    
    Highcharts.chart('nitrogenChart', {
        chart: {
            type: 'line'
        },
        title: {
            text: ' Nitrogen Over Time'
        },
        xAxis: {
            // Optionally, add categories or labels if necessary, e.g., timestamps
        },
        yAxis: {
            title: {
                text: 'N:'
            }
        },
        series: [{
            name: 'Nitrogen',
            data: nitrogenData.map(Number) // Ensure data is in Number format
        }]
    });

    var phosphorusData = <?php echo json_encode($all_phosphorus); ?>;
    
    Highcharts.chart('phosphorusChart', {
        chart: {
            type: 'line'
        },
        title: {
            text: ' Phosphorus Over Time'
        },
        xAxis: {
            // Optionally, add categories or labels if necessary, e.g., timestamps
        },
        yAxis: {
            title: {
                text: 'P:'
            }
        },
        series: [{
            name: 'Phosphorus',
            data: phosphorusData.map(Number) // Ensure data is in Number format
        }]
    });

    
    var potassiumData = <?php echo json_encode($all_potassium); ?>;
    
    Highcharts.chart('potassiumChart', {
        chart: {
            type: 'line'
        },
        title: {
            text: ' Potassium Over Time'
        },
        xAxis: {
            // Optionally, add categories or labels if necessary, e.g., timestamps
        },
        yAxis: {
            title: {
                text: 'K:'
            }
        },
        series: [{
            name: 'Potassium',
            data: potassiumData.map(Number) // Ensure data is in Number format
        }]
    });
    </script>
</div>

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
.chart-container {
    border: 1px solid #ddd; /* Add a border */
    padding: 10px;
    background-color: #fff; /* Add a background color if you like */
    margin-bottom: 20px; /* Add some space between the rows of charts */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Optional: Adds a subtle shadow to make the charts 'pop' a bit */
}

/* Highcharts specific styling */
.highcharts-figure, .highcharts-data-table table {
    min-width: 320px; /* Adjust minimum width as needed */
    max-width: 660px; /* Adjust maximum width as needed */
    margin: 1em auto;
}

@media (max-width: 768px) {
    .main-content {
        margin-left: 0;
    }
    .sidebar {
        width: auto;
    }
    .chart-container {
        margin-bottom: 0;
    }
    .highcharts-figure, .highcharts-data-table table {
        min-width: 100%;
        max-width: 100%;
    }
}
</style>