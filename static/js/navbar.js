const toggleButton = document.getElementsByClassName('toggleButton')[0];
const navBarLinks = document.getElementsByClassName('navBarRight')[0];


toggleButton.addEventListener('click', ()=>
{
    navBarLinks.classList.toggle('active')
});
