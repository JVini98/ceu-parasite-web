const image = document.getElementById('gameImage');
const buttonCrop = document.getElementById('cropButton');
const buttonSave = document.getElementById('saveButton');
const buttonSend = document.getElementById('sendButton');
const parasitesForm = document.getElementById('parasitesForm');
const jsonForm = document.getElementById('jsonForm');
const parasitesResponse = document.getElementById('parasitesResponse');
const annotationForm = document.getElementById('annotation');
const csrf = document.getElementsByName("csrfmiddlewaretoken");

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
  parasitesResponse.innerHTML += `<image src="${url}" width="150px" class="margin"/>`
                               + `<p>${annotationSave}</p>`
                               // + `<p>x:${imagePosition.x}; y:${imagePosition.y}; width:${imagePosition.width}; height:${imagePosition.height}
  parasitesList.push(createParasiteObj(annotationSave, imagePosition.x, imagePosition.y, imagePosition.width, imagePosition.height));
  annotationForm.value="";
  showbuttonSave(parasitesResponse.innerHTML);
});

// create parasite object
function createParasiteObj(pAnnotation, pCoordX, pCoordY, pWidth, pHeight){
  let parasite = {};
  parasite.url = image.src;
  parasite.annotation = pAnnotation;
  parasite.coordinateX = pCoordX;
  parasite.coordinateY = pCoordY;
  parasite.width = pWidth;
  parasite.height = pHeight;
  return parasite;
}

// change state button according to input value
buttonSave.disabled=true;

annotationForm.addEventListener("input", ()=>{
  if (annotationForm.value === "" || annotationForm.value === " ") {
    buttonSave.disabled = true; 
  } else {
    buttonSave.disabled = false; 
  }
});

// control of sending data to the server
buttonSend.style.visibility = 'hidden';

function showbuttonSave(parasitesSelected){
  if (parasitesSelected !== "") buttonSend.style.visibility = 'visible';
}

// generate and send JSON
buttonSend.addEventListener('click', ()=>{
  let json = JSON.stringify(parasitesList)
  console.log("Antes de entrar en Ajax" + json);
  
  $(document).ready(function () {
      var formData = new FormData();
      formData.append('csrfmiddlewaretoken', csrf[0].value);
      formData.append('file', json);
  
      $.ajax({
          url: jsonForm.action,
          type: "POST",
          data: formData,
          processData: false,
          contentType: false,
          success: function (response) {
              console.log("AJAX: " + response);
          },
          error: function (error) {
            console.log(error);
          }
      });
  });
});
  



