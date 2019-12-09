/* 
This script contains all the variables and functions for the Canvas.
Resources Used:
https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API
https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Drawing_shapes
*/
// Set up Canvas variables, variables to track mouse position, flags for draw continuous/draw a dot.
var canvas, ctx, flag = false,
    prevX = 0,
    currX = 0,
    prevY = 0,
    currY = 0,
    radius = 5,
    dot_flag = false;

// Drawing colour and line width
var x = "white",
    y = 2;

// Init the canvas, add listeners to catch mouse function
function init() {
    // Find the canvas on the mage by it's ID
    canvas = document.getElementById('MNISTCanvas');
    // Set the context 
    ctx = canvas.getContext("2d");
    // Set width and Height
    w = canvas.width;
    h = canvas.height;

    // Listeners for drawing on the canvas with the mouse
    // We use Findxy to assign functionality here depending on the mouse event
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

// Draw to canvas, called on canvas while mouse is clicked
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
    ctx.clearRect(0, 0, w, h);    
}


// Find mouse (x,y) position takes listener and event
function findxy(res, e) {
    // If the mouse event is mousedown set mouse coordinates
    if (res == 'down') {
        prevX = currX;
        prevY = currY;
        currX = e.clientX - canvas.offsetLeft;
        currY = e.clientY - canvas.offsetTop;

        // Enable continuous drawing flag
        flag = true;
        // dotFLag - draw a dot on click/release
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
    // Update the mouse position while mousedown and within canvas bounds
    if (res == 'move') {
        if (flag) {
            prevX = currX;
            prevY = currY;
            currX = e.clientX - canvas.offsetLeft;
            currY = e.clientY - canvas.offsetTop;
            // Draw on the canvas
            draw();
        }
    }
} // end findxy

