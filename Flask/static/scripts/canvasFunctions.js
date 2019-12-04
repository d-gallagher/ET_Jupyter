
    // Set up canvas variables
    var canvas, ctx, flag = false,
        prevX = 0,
        currX = 0,
        prevY = 0,
        currY = 0,
        radius = 5,
        dot_flag = false;

    var x = "blue",
        y = 2;

    // Init the canvas, add lesteners to catch mouse function
    function init() {
        canvas = document.getElementById('MNISTCanvas');
        ctx = canvas.getContext("2d");
        w = canvas.width;
        h = canvas.height;

        canvas.addEventListener("mousemove", function (e) {
            findxy('move', e)
        }, false);
        canvas.addEventListener("mousedown", function (e) {
            findxy('down', e)
        }, false);
        canvas.addEventListener("mouseup", function (e) {
            findxy('up', e)
        }, false);
        canvas.addEventListener("mouseout", function (e) {
            findxy('out', e)
        }, false);
    }

    // Draw to canvas, called on canvas click
    function draw() {
        ctx.beginPath();
        ctx.lineTo(currX, currY);
        ctx.strokeStyle = x;
        ctx.lineWidth = y;
        ctx.stroke();
        ctx.beginPath();
        ctx.arc(currX, currY, radius, 0, Math.PI * 2);
        ctx.fill();
        ctx.beginPath();
        ctx.moveTo(prevX, prevY);
    }

    // Clear the canvas
    function clearCanvas() {
        var m = confirm("Erase the Canvas?");
        if (m) {
            ctx.clearRect(0, 0, w, h);
        }
    }

    // Handles Data from html to flask and returnData from flask
    function getData() {
        // grab the canvas on the page
        var canvas = document.getElementById("MNISTCanvas");
        // get base 64 encoded image
        var canvasUrl = canvas.toDataURL();
        // split the text from the url
        var imgData = canvasUrl.split(',')[1];
        // console.log(canvasUrl);
        console.log(imgData);

        // Data obj for the canvas
        let canvasEntry = {
            data: imgData
        }

        // https://pythonise.com/series/learning-flask/flask-and-fetch-api
        fetch(`${window.origin}/postmethod`, {
            method: "POST",
            credentials: "include",
            body: JSON.stringify(canvasEntry),
            cache: "no-cache",
            headers: new Headers({
                "content-type": "application/json"
            })
            })
            .then(function (response) {
                if (response.status !== 200) {
                console.log(`Looks like there was a problem. Status code: ${response.status}`);
                return;
                }
                response.json().then(function (data) {
                console.log(data);
                // document.getElementById("imageUrl").innerText = data.returnData;
                document.getElementById("numberprediction").innerText = data.returnData;
                });
            })
            .catch(function (error) {
                console.log("Fetch error: " + error);
            });

    }

    // Find mouse (x,y) position takes listener and event
    function findxy(res, e) {
        if (res == 'down') {
            prevX = currX;
            prevY = currY;
            currX = e.clientX - canvas.offsetLeft;
            currY = e.clientY - canvas.offsetTop;

            flag = true;
            dot_flag = true;
            if (dot_flag) {
                ctx.beginPath();
                ctx.fillStyle = x;
                ctx.fillRect(currX, currY, 2, 2);
                ctx.closePath();
                dot_flag = false;
            }
        }
        // Mouseup or leave canvas, stop drawing
        if (res == 'up' || res == "out") {
            flag = false;
        }
        if (res == 'move') {
            if (flag) {
                prevX = currX;
                prevY = currY;
                currX = e.clientX - canvas.offsetLeft;
                currY = e.clientY - canvas.offsetTop;
                draw();
            }
        }
    } // end findxy

