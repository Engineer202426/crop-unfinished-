<!DOCTYPE html>
<html>
<head>
    <title>Hybrid Algorithm Results</title>
</head>
<body>

<?php
// Disable output buffering
ob_end_flush();
?>

<script>
function runPythonScript() {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            document.getElementById('output').innerHTML = xhr.responseText;
        }
    };
    xhr.open('GET', 'run_python_script.php', true);
    xhr.send();
}
</script>

<button onclick='runPythonScript()'>Run Python Script</button>
<h2>Hybrid Algorithm Results</h2>
<div id='output'></div>

</body>
</html>
