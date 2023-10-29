$(document).ready(function(){
    $(".dropdown").hover(function(){
        var dropdownMenu = $(this).children(".dropdown-menu");
        if(dropdownMenu.is(":visible")){
            dropdownMenu.parent().toggleClass("open");
        }
    });

    const shop =document.querySelector(".dropdown");
    shop.addEventListener('click',()=>{
        window.location.replace("./shop.html")
    });
});