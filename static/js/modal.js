// //modal//
 var modal = document.getElementById("modal-container")
 var openBtn = document.getElementById("openImg")
 var closeBtn = document.getElementById("closeBtn");
 var funcs = [];

 function Modal(num) {
     return function () {
         openBtn[num].onclick = function () {
             modal[num].style.display = "flex"
             console.log(num);

         };
         closeBtn[num].onclick = function () {
             modal[num].style.display = "none";
         };

     };
 }
for(let i = 0; i< openBtn.length; i++) {
    funcs[i] = Modal(i);
}
for(let j = 0; j<openBtn.length; j++){
    funcs[j]();
}

window.onclick = function (event) {
    if (event.target.id == "modal-container")
    {
        event.target.style.display="none";
    }
};
//
// function openModal(){
//     const OpenModal = document.querySelector("#modal-container")
//     OpenModal.classList.add("OpenModal");
// }


// const modal = document.querySelector("#modal-container");
// const img = document.querySelector(".openImg");
// const modal_img = document.querySelector(".modalImg");
// const close = document.querySelector("#closeBtn");
//
// img.addEventListener('click', ()=>{
//   modal.style.display="flex";
//   modal_img.src = img.src;
// });
// close.addEventListener('click', ()=>{
//   modal.style.display="none";
// });
// modal.addEventListener('click', ()=>{
//   modal.style.display="none";
// });
// function modalDisplay(text){
//   modal.style.display = text;
// }
