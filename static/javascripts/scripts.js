const inputPass1 = document.getElementById("password1");
const inputPass2 = document.getElementById("password2");
const error = document.getElementById("error");

//Form Validation
const form = document.getElementById("signup-form") || document.getElementById("password-form");

form.addEventListener("submit", (e) =>{
    const password1 = document.getElementById("password1").value;
    const password2 = document.getElementById("password2").value;

    if (password1 != password2){
        e.preventDefault(); 
        inputPass1.style.borderColor="red";
        inputPass2.style.borderColor="red";
        error.innerHTML="The passwords do not match. Plase make sure you typed them correctly."
    }

})
