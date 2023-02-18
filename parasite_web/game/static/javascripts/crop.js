/*let canvas = document.getElementById("myCanvas");
let ctx = canvas.getContext("2d");
        
let img = new Image();
img.src = "../static/images/ameba.jpg";
ctx.drawImage(img, 0, 0, canvas.width, canvas.height); */

const image = document.getElementById('gameImage');

const cropper = new Cropper(image, {
  aspectRatio: 16 / 9,
  crop(event) {
    console.log(event.detail.x);
    console.log(event.detail.y);
    console.log(event.detail.width);
    console.log(event.detail.height);
    console.log(event.detail.rotate);
    console.log(event.detail.scaleX);
    console.log(event.detail.scaleY);
  },
});