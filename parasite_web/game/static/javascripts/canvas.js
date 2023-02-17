let canvas = document.getElementById("myCanvas");
let ctx = canvas.getContext("2d");
        
let img = new Image();
img.src = "../static/images/ameba.jpg";
ctx.drawImage(img, 0, 0, canvas.width, canvas.height); 