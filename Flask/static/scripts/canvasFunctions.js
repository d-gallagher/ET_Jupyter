
    // Set up canvas variables
    var canvas, ctx, flag = false,
        prevX = 0,
        currX = 0,
        prevY = 0,
        currY = 0,
        radius = 5,
        dot_flag = false;

    var x = "black",
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
            document.getElementById("MNISTCanvas").style.display = "none";
        }
    }

    // Save the image for use in NN Model
    function getData() {
        
        var canvas = document.getElementById("MNISTCanvas");
        console.log(canvas.toDataURL());
        // var imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        // var data = imageData.data;
        // var outputData = []
        // for(var i = 0; i < data.length; i += 4) {
        // var brightness = 0.34 * data[i] + 0.5 * data[i + 1] + 0.16 * data[i + 2];
        // outputData.push(brightness);
        // }
        // $.post( "/postmethod", {
        // canvas_data: JSON.stringify(outputData)
        // });
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

