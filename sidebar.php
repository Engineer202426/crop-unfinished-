
<div id="sidebar" class="sidebar">
    <div class="sidebar-header">
        <h3>Crop Calendar</h3>
    </div>
    <ul class="sidebar-menu">
        <li><a href="sensor.php">Sensor</a></li>
        <li><a href="analytical.php">Analytical</a></li>
        <li><a href="calendar.php">Calendar</a></li>
        <li><a href="deploy.php">Settings</a></li>
        <li><a href="logout.php">Logout</a></li>
    </ul>
</div>

<style>
    /* Sidebar styles */
.sidebar {
    height: 100%;
    width: 250px;
    position: fixed;
    left: 0;
    top: 0;
    z-index: 1;
    background-color: #111;
    overflow-x: hidden;
    padding-top: 20px;
}

.sidebar-header {
    padding: 10px;
    background: forestgreen;
    color: white;
    text-align: center;
}

.sidebar-menu {
    list-style-type: none;
    padding: 0;
}

.sidebar-menu li a {
    padding: 10px 15px;
    text-decoration: none;
    font-size: 18px;
    color: #ddd;
    display: block;
}

.sidebar-menu li a:hover {
    color: #fff;
    background-color: forestgreen;
}

</style>