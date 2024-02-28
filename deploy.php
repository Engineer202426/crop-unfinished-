<!DOCTYPE html>
<html>
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

  <h2 class="text-center mb-4">Controller</h2>

  <div class="container-fluid">
  <div class="row">
    <div class="container">

      <!-- Form -->
      <form action="controller.php" method="post" onsubmit="return confirmChange()">
        <label for="intervalSelect">Set Time (1 hour - 8 hours):</label>
        <select class="custom-select" id="intervalSelect" name="interval">
          <option value="3600000" <?php if (isset($currentInterval) && $currentInterval == 3600000) echo 'selected'; ?>>1 hour</option>
          <option value="7200000" <?php if (isset($currentInterval) && $currentInterval == 7200000) echo 'selected'; ?>>2 hours</option>
          <option value="10800000" <?php if (isset($currentInterval) && $currentInterval == 10800000) echo 'selected'; ?>>3 hours</option>
          <option value="14400000" <?php if (isset($currentInterval) && $currentInterval == 14400000) echo 'selected'; ?>>4 hours</option>
          <option value="18000000" <?php if (isset($currentInterval) && $currentInterval == 18000000) echo 'selected'; ?>>5 hours</option>
          <option value="21600000" <?php if (isset($currentInterval) && $currentInterval == 21600000) echo 'selected'; ?>>6 hours</option>
          <option value="25200000" <?php if (isset($currentInterval) && $currentInterval == 25200000) echo 'selected'; ?>>7 hours</option>
          <option value="28800000" <?php if (isset($currentInterval) && $currentInterval == 28800000) echo 'selected'; ?>>8 hours</option>
        </select>
        <input type="submit" class="btn btn-primary mt-2 mb-4" value="Set Interval">
      </form>
      
      <!-- Text field for adjustable times -->
      <div class="input-group mb-3">
        <input type="number" class="form-control" id="adjustableTime" placeholder="Adjustable Time" aria-label="Adjustable Time" aria-describedby="adjustableTimeAddon">
        <div class="input-group-append">
          <button class="btn btn-outline-secondary" type="button" onclick="setAdjustableTime()">Set</button>
        </div>
      </div>
    </div>
  </div>
</div>




</div> 

<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.4.2/dist/umd/popper.min.js"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
<script>
  // Function to confirm the interval change
  function confirmChange() {
    return confirm("Are you sure you want to set the interval?");
  }

  // Function to confirm setting the adjustable time
  function setAdjustableTime() {
    if (confirmChange()) {
  
      alert("Adjustable time is set!");
    }
  }

  // Function to increase time
  function increaseTime() {
    var adjustableTimeField = document.getElementById("adjustableTime");
    adjustableTimeField.stepUp();
  }

  // Function to decrease time
  function decreaseTime() {
    var adjustableTimeField = document.getElementById("adjustableTime");
    adjustableTimeField.stepDown();
  }
</script>

</body>
</html>
<style>
    body {
      background-color: #f4f4f4; /* Light background */
  
    }
    .container {
      padding: 20px;
      max-width: 600px; /* Responsive width */
      margin: auto;
      background: white; /* Clear distinction from the background */
      border-radius: 8px; /* Softened edges */
      box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
    }
    .custom-select {
      cursor: pointer; /* Indicates interactivity */
    }
    .custom-select:focus {
      outline: none; /* Removes default focus outline */
      box-shadow: none; /* Removes default focus shadow */
    }
    .output {
      color: #FF0000; 
      font-weight: bold; 
    }
  </style>
