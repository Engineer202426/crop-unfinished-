<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Run Machine Learning Script</title>
</head>
<body>
    <h1>Run Machine Learning Script</h1>
    <button onclick="runScript()">Run Script</button>

    <div id="result"></div>

    <script>
        function runScript() {
            var xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function () {
                if (xhr.readyState == 4 && xhr.status == 200) {
                    // Display the output in the 'result' div
                    document.getElementById("result").innerHTML = xhr.responseText;
                }
            };
            xhr.open("GET", "run_machine_learning_script.php", true);
            xhr.send();
        }
    </script>
</body>
</html>
