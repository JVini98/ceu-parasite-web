// const close = document.querySelector(".message-close");
// const message = document.querySelector(".messages");
const inputPass1 = document.getElementById("password1");
const inputPass2 = document.getElementById("password2");
const error = document.getElementById("error");

//Close Error/Success Message
// if (close && message){
//     close.addEventListener("click", () =>{
//         message.style.display = "none";
//     })
// }

//Form Validation
const signupForm = document.getElementById("signup-form");

signupForm.addEventListener("submit", (e) =>{
    
    // const title = document.querySelector(".message-title");
    // const messageParagraph = document.querySelector(".message-paragraph");
    const password1 = document.getElementById("password1").value;
    const password2 = document.getElementById("password2").value;

    if (password1 != password2){
        e.preventDefault(); 
        // message.style.display = "flex";
        // title.textContent = "Invalid Password!";
        // messageParagraph.textContent = "Make sure to confirm your password.";
        inputPass1.style.borderColor="red";
        inputPass2.style.borderColor="red";
        error.innerHTML="The passwords do not match. Plase make sure you typed them correctly."
    }

})
