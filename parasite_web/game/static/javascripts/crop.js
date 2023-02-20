const image = document.getElementById('gameImage');
const button = document.getElementById('cropButton');
const parasites = document.getElementById('parasites');
//const csrf = document.getElementsByName('csrfmiddlewaretoken');

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

button.addEventListener('click', ()=>{
  cropper.getCroppedCanvas().toBlob((blob) => {

    const url = URL.createObjectURL(blob);
    parasites.innerHTML = `<image src="${url}" width="150px" class="margin"/>`;


    /**const formData = new FormData();
  
    formData.append('csrfmiddlewaretoken', csrf[0].value)
    formData.append('croppedImage', blob, 'example.png' );
  
    $.ajax('/media/images', {
      method: 'POST',
      data: formData,
      processData: false,
      contentType: false,
      success() {
        console.log('Upload success');
      },
      error() {
        console.log('Upload error');
      },
    });*/
  });
});

