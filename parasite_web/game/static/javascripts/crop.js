const image = document.getElementById('gameImage');
const buttonCrop = document.getElementById('cropButton');
const buttonSave = document.getElementById('saveButton');
const parasitesForm = document.getElementById('parasitesForm');
const annotationForm = document.getElementById('annotation');

let url;
let imagePosition;
let annotationSave;

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
  parasitesResponse.innerHTML = `<image src="${url}" width="150px" class="margin"/>
                                 <p>${annotationSave}</p>
                                 <p>x:${imagePosition.x}; y:${imagePosition.y}; width:${imagePosition.width}; height:${imagePosition.height}`;
  annotationForm.value="";
});

// change state button according to input value
buttonSave.disabled=true;

annotationForm.addEventListener("input", ()=>{
  if (annotationForm.value === "") {
    buttonSave.disabled = true; 
  } else {
    buttonSave.disabled = false; 
  }
});
