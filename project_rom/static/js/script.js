const headOne = document.getElementById('headOne');

headOne.addEventListener('mouseover', () =>{
    headOne.style.color = 'blue';
    headOne.innerHTML = "Have a great day!";
});

headOne.addEventListener('mouseout', () => {
    headOne.style.color = 'darkcyan';
});

window.onload = () => {
    alert("Welcome to Dashboard!");
}
window.onresize = () => {
    alert("I am resized");
}