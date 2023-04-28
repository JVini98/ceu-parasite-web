const image = document.getElementById('gameImage');
const buttonCrop = document.getElementById('cropButton');
const buttonSave = document.getElementById('saveButton');
const buttonSend = document.getElementById('sendButton');
const parasitesForm = document.getElementById('parasitesForm');
const jsonForm = document.getElementById('jsonForm');
const annotationForm = document.getElementById('annotation');
const alertBox = document.getElementById('alertBox');
const imageID = document.getElementById('imageID');
const csrf = document.getElementsByName("csrfmiddlewaretoken");

// working with the slider
slider = document.querySelector('.slider');
sliderButtonLeft = document.querySelector('.slider-button-left');
sliderButtonRight = document.querySelector('.slider-button-right');
let slides;
let slideWidth = 0;

let currentPosition = 0;
slider.style.transform = `translateX(${currentPosition}px)`;

let url;
let imagePosition;
let annotationSave;
let parasitesList = [];

// cropper properties
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

// crop image on click
buttonCrop.addEventListener('click', ()=>{
  cropper.getCroppedCanvas().toBlob((blob) => {
    imagePosition = cropper.getData();
    url = URL.createObjectURL(blob);
    parasitesForm.innerHTML = `<image src="${url}" width="150px" class="imageCentered marginBotton"/>`;
  });
});

// temporary save image on click
buttonSave.addEventListener('click', ()=>{
  annotationSave = annotationForm.value;
  // Adding new slide to the slider dynamically
  slider.innerHTML += `<div class="slide">`
                    + `<image src="${url}" width="150px" class="margin"/>`
                    + `<p class="textCenter">${annotationSave}</p>`
                    + `</div>`
  slides = document.querySelectorAll('.slide');
  // alert("The number of slides are " + slides.length)
  slideWidth = slides[0].clientWidth + 30;
  // List with all the parasites selected by the user
  parasitesList.push(createParasiteObj(annotationSave, imagePosition.x, imagePosition.y, imagePosition.width, imagePosition.height));
  showbuttonSave(slider.innerHTML);
});

// create parasite object
function createParasiteObj(pAnnotation, pCoordX, pCoordY, pWidth, pHeight){
  let parasite = {};
  parasite.imageID = imageID.innerHTML;
  parasite.annotation = pAnnotation;
  parasite.coordinateX = pCoordX;
  parasite.coordinateY = pCoordY;
  parasite.width = pWidth;
  parasite.height = pHeight;
  return parasite;
}

// control of sending data to the server
buttonSend.style.visibility = 'hidden';

function showbuttonSave(parasitesSelected){
  if (parasitesSelected !== "") buttonSend.style.visibility = 'visible';
}

// generate and send JSON
buttonSend.addEventListener('click', ()=>{
  let json = JSON.stringify(parasitesList)
  
  $(document).ready(function () {
      var formData = new FormData();
      formData.append('csrfmiddlewaretoken', csrf[0].value);
      formData.append('json', json);
  
      $.ajax({
          url: jsonForm.action,
          method: "POST",
          data: formData,
          processData: false,
          contentType: false,
          success: function (response) {
            console.log(response);
            alertBox.innerHTML = `<div id="alertBox" class="alert alert-success" role="alert">${response["message"]}</div>`;
            // reload page to display another image
            setTimeout(function(){
              window.location.reload();
            }, 3000);
          },
          error: function (error) {
            console.log(error);
            alertBox.innerHTML = `<div class="alert alert-danger" role="alert">${error}</div>`;
          }
      });
  });
});

// Move images in the slider
sliderButtonLeft.addEventListener('click', () => {
  currentPosition += slideWidth;
  if (currentPosition > 0) {
    currentPosition = -(slides.length - 1) * slideWidth;
  }
  slider.style.transform = `translateX(${currentPosition}px)`;
});

sliderButtonRight.addEventListener('click', () => {
  currentPosition -= slideWidth;
  if (currentPosition < -(slides.length - 1) * slideWidth) {
    currentPosition = 0;
  }
  slider.style.transform = `translateX(${currentPosition}px)`;
});



