const inputPass1 = document.getElementById("password1");
const inputPass2 = document.getElementById("password2");
const error = document.getElementById("error");

//Form Validation
const form = document.getElementById("signup-form") || document.getElementById("password-form");

form.addEventListener("submit", (e) =>{
    const password1 = inputPass1.value;
    const password2 = inputPass2.value;
    const checkboxPolicy = document.getElementById("accept-policy");
    const checkboxTerms = document.getElementById("accept-terms");

    if (password1 != password2){
        e.preventDefault(); 
        inputPass1.style.borderColor="red";
        inputPass2.style.borderColor="red";
        error.innerHTML="The passwords do not match. Please make sure you typed them correctly."
    }

    else if (!checkboxPolicy.checked || !checkboxTerms.checked){
        e.preventDefault();
        checkboxPolicy.style.outlineColor = "red";
        checkboxPolicy.style.outlineWidth = "1px";
        checkboxPolicy.style.outlineStyle = "solid";
        checkboxTerms.style.outlineColor = "red";
        checkboxTerms.style.outlineWidth = "1px";
        checkboxTerms.style.outlineStyle = "solid";
        error.innerHTML="To be registered you need to click on the two previous checkboxes.";
    }

})
