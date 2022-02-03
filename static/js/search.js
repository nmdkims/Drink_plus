const title = document.querySelector(".title");
const subTitle = document.querySelector(".sub-title");


function TitleClick() {
    title.classList.toggle("titleClicked");
}
function subTitleClick() {
    subTitle.classList.toggle("subTitleClicked");
}

title.addEventListener("click", TitleClick);
subTitle.addEventListener("click", subTitleClick);