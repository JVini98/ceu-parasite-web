const image = document.getElementById('gameImage');
const buttonCrop = document.getElementById('cropButton');
const buttonSave = document.getElementById('saveButton');
const parasitesForm = document.getElementById('parasitesForm');
const annotation = document.getElementById('annotation');
let url;

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

buttonCrop.addEventListener('click', ()=>{
  cropper.getCroppedCanvas().toBlob((blob) => {
    url = URL.createObjectURL(blob);
    parasitesForm.innerHTML = `<image src="${url}" width="150px" class="imageCentered marginBotton"/>`;
  });
});

buttonSave.addEventListener('click', ()=>{
  parasitesResponse.innerHTML = `<image src="${url}" width="150px" class="margin"/>`;
});

buttonSave.disabled=true;

annotation.addEventListener("input", ()=>{
  if (annotation.value === "") {
    buttonSave.disabled = true; 
  } else {
    buttonSave.disabled = false; 
  }
});
