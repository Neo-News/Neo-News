
// profile user 이미지 업로드 기능
const $uploadImgInput = document.querySelector('.profile-upload-img-input');
const $uploadPreviewImg = document.querySelector('.profile-upload-preview-img');

$uploadImgInput.onchange = (e) => {
// document.querySelector('.upload-img-div').innerHTML='';
let image = event.target.files[0]
  let reader = new FileReader();
  reader.onload = function (event) {
    $uploadPreviewImg.setAttribute('src', event.target.result);
  }

  reader.readAsDataURL(image);
}



function UploadImg(event){
$uploadImgInput.click();
}
function changePwd(event){
  event.preventDefault();
}