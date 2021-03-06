function readSpec(type) {
    contents = "";

    var file = document.querySelector("." + type).files[0];
    var reader = new FileReader();

    reader.addEventListener("load", function() {
        contents = reader.result;
        drawFromJSON(contents, type);
    }, false);

    if (file) {
        reader.readAsText(file);
    }

}

function addLine(point1, point2, color) {
    var svg = document.getElementById("visualization");

    var x1 = point1[0];
    var x2 = point2[0];
    var y1 = -point1[1];
    var y2 = -point2[1];

    var line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    line.setAttribute('x1', x1);
    line.setAttribute('y1', y1);
    line.setAttribute('x2', x2);
    line.setAttribute('y2', y2);
    line.setAttribute('stroke', color);
    line.setAttribute('stroke-width', 0.005);
    svg.appendChild(line);
}

function addCircle(point, color) {
    var svg = document.getElementById("visualization");

    console.log(point);

    var x = point[0];
    var y = -point[1];

    var dot = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    dot.setAttribute('cx', x);
    dot.setAttribute('cy', y);
    dot.setAttribute('r', 0.01);
    dot.setAttribute('stroke', color);
    dot.setAttribute('stroke-width', 0.001);
    dot.setAttribute('fill', color);
    svg.appendChild(dot);
}

function clearVisualization() {
    var svg = document.getElementById("visualization");
    while (svg.firstChild)
        svg.removeChild(svg.firstChild);

    rightest_x = Number.MIN_VALUE;
    uppest_y = Number.MIN_VALUE;
    leastright_x = Number.MAX_VALUE;
    leastup_y = Number.MAX_VALUE;
}

function adjustViewport(leastright_x, leastup_y, rightest_x, uppest_y) {
    console.log([leastright_x, leastup_y, rightest_x, uppest_y]);
    var viewbox = [leastright_x - 0.01, (-uppest_y) - 0.01,
                   (rightest_x - leastright_x) + 0.02,
                   (uppest_y - leastup_y) + 0.02].join(" ");
    console.log(viewbox);
    var svg = document.getElementById("visualization");
    svg.setAttribute("viewBox", viewbox);

}

rightest_x = Number.MIN_VALUE;
uppest_y = Number.MIN_VALUE;
leastright_x = Number.MAX_VALUE;
leastup_y = Number.MAX_VALUE;

function drawFromJSON(jsonString, type) {
    if (type === 'problem') {
        clearVisualization();

        problem = JSON.parse(jsonString);
        var skeleton = problem["skeleton"]
        var polygons = problem;
        delete polygons["skeleton"] // destructive!

        // draw skeleton
        for (var i in skeleton) {
            var endpoints = skeleton[i];
            addLine(endpoints[0], endpoints[1], "lightgrey")
        }

        // draw silhouette
        for (var polygon_id in polygons) {
            var points = polygons[polygon_id];

            for (var point in points) {
                x_coord = parseFloat(points[point][0]);
                y_coord = parseFloat(points[point][1]);

                rightest_x = Math.max(x_coord, rightest_x);
                uppest_y = Math.max(y_coord, uppest_y);
                leastright_x = Math.min(x_coord, leastright_x);
                leastup_y = Math.min(y_coord, leastup_y);
            }

            for (var point = 1; point < points.length; point++) {
                addLine(points[point], points[point - 1], "black");
            }
            addLine(points[points.length - 1], points[0], "black");
        }
    }

    if (type === 'solution') {
        solution = JSON.parse(jsonString);
        console.log("the solution");
        console.log(solution);

        for (var i in solution) {
            console.log("a point")
            addCircle(solution[i], "deepskyblue");
            x_coord = parseFloat(solution[i][0]);
            y_coord = parseFloat(solution[i][1]);

            console.log(x_coord)
            console.log(y_coord)

            rightest_x = Math.max(x_coord, rightest_x);
            uppest_y = Math.max(y_coord, uppest_y);
            leastright_x = Math.min(x_coord, leastright_x);
            leastup_y = Math.min(y_coord, leastup_y);
        }
    }

    adjustViewport(leastright_x, leastup_y, rightest_x, uppest_y);
} 
