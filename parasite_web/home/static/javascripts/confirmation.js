const buttonDelete = document.getElementById('delete_buttom');
const formDelete = document.getElementById('delete_form')

// Show confirm message
buttonDelete.addEventListener('click', (e)=>{
    e.preventDefault();
    var confirmed = confirm("Are you sure you want to delete the user?");
    if (confirmed) formDelete.submit();
});