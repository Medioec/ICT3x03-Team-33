// Define a function to check if all registration fields and the form are valid
function checkRegistrationFields() {
    const $emailInput = $("#email");
    const $userNameInput = $("#userName");
    const isFormValid = $("#register-form").valid(); // Check overall form validity
  
    // Sanitize input values using DOMPurify
    const email = DOMPurify.sanitize($emailInput.val());
    const username = DOMPurify.sanitize($userNameInput.val());
  
    // Return true if all fields are filled correctly and the form is valid
    return email && username && isFormValid;
  }
  
  // Define the onSuccess function to handle the captcha callback
  function onSuccess() {
    const $registerButton = $("#create-staff-button");
    if (checkRegistrationFields() && grecaptcha.getResponse()) {
      $registerButton.prop("disabled", false);
    } else {
      $registerButton.prop("disabled", true);
    }
  }
  
  document.addEventListener("DOMContentLoaded", function () {
    const $registerButton = $("#create-staff-button");
    const $emailInput = $("#email");
    const $userNameInput = $("#userName");
  
    $emailInput.on("input", function () {
      if (checkRegistrationFields()) {
        onSuccess(); 
      } else {
        $("#register-button").prop("disabled", true);
      }
    });
  
    $userNameInput.on("input", function () {
      if (checkRegistrationFields()) {
        onSuccess(); 
      } else {
        $("#register-button").prop("disabled", true);
      }
    });
  
    $registerButton.click(async function (event) {
      event.preventDefault();
  
      if ($("#register-form").valid()) {
        const email = DOMPurify.sanitize($emailInput.val());
        const username = DOMPurify.sanitize($userNameInput.val());
  
        const data = {
          email: email,
          username: username
        };
  
        if (grecaptcha.getResponse()) { // Check if reCAPTCHA is completed
          await fetch("/createStaffRequest", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Accept": "application/json"
            },
            body: JSON.stringify(data),
          })
          .then(response => 
          {
            // redirect to login if registration successful
            if (response.ok) {
              window.location.href = "/login";
            }
          });
        } else {
          document.getElementById("error-message").textContent = "Please complete the reCAPTCHA.";
        }
      }
    });
  });
  
  (function($) {
    $('.palceholder').click(function() {
      $(this).siblings('input').focus();
    });
  
    $('.form-control').focus(function() {
      $(this).parent().addClass("focused");
    });
  
    $('.form-control').blur(function() {
      var $this = $(this);
      if ($this.val().length == 0)
        $(this).parent().removeClass("focused");
    });
    $('.form-control').blur();  
  
    $.validator.setDefaults({
      errorElement: 'span',
      errorClass: 'validate-tooltip'
    });
  
    $("#register-form").validate({
      rules: {
        email: {
          required: true,
          customEmailValidation: true,
        },
        username: {
          required: true,
          minlength: 3,
          customUsernameValidation: true
        }
      },
      messages: {
        email: {
          required: "Please enter your email address.",
          customEmailValidation: "Please provide a valid email address."
        },
        username: {
          required: "Please enter your username.",
          minlength: "Username must be at least 3 characters.",
          customUsernameValidation: "Please provide a valid username."
        }
      }
    });
  
    $.validator.addMethod("customEmailValidation", function(value, element) {
      var emailPattern = /^[A-Za-z0-9_!#$%&'*+\/=?^_`{|}~.-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
      return emailPattern.test(value);
    }, "Please provide a valid email address.");
  
    $.validator.addMethod("customUsernameValidation", function(value, element) {
      var usernamePattern = /^[a-zA-Z0-9]{3,16}$/;
      return usernamePattern.test(value);
    }, "Please provide a valid username.");
  })(jQuery);
  

// document.addEventListener('DOMContentLoaded', () => {
//     const deleteModal = document.getElementById("delete-modal");
//     const editModal = document.getElementById("edit-modal");
//     const closeDeleteModalButton = document.getElementById("close-delete-modal");
//     const closeEditModalButton = document.getElementById("close-edit-modal");
//     const confirmDeleteButton = document.getElementById("confirm-delete");
//     const confirmEditButton = document.getElementById("confirm-edit");
//     const cancelDeleteButton = document.getElementById("cancel-delete");
//     const cancelEditButton = document.getElementById("cancel-edit");


//     const editUserEmailInput = document.getElementById('editUserEmail');
//     const editUserUsernameInput = document.getElementById('editUserUsername');
//     const userEmailPlaceholder = document.getElementById('userEmailPlaceholder');
//     const userUsernamePlaceholder = document.getElementById('userUsernamePlaceholder');

//     ////////////////////////// to close modal //////////////////////////
//     closeDeleteModalButton.addEventListener("click", () => {
//         deleteModal.style.display = "none";
//     });

//     closeEditModalButton.addEventListener("click", () => {
//         editModal.style.display = "none";
//     });

//     cancelDeleteButton.addEventListener("click", () => {
//         deleteModal.style.display = "none";
//     });

//     cancelEditButton.addEventListener("click", () => {
//         editModal.style.display = "none";
//     });
//     //////////////////////////       end       //////////////////////////

//     confirmDeleteButton.addEventListener("click", () => {
//         deleteModal.style.display = "none";
//         // TODO: Delete user
//     });

//     confirmEditButton.addEventListener("click", () => {
//         editModal.style.display = "none";
//         // TODO: Modify email and username fields 
//     });

//     window.addEventListener("click", (event) => {
//         if (event.target === deleteModal) {
//             deleteModal.style.display = "none";
//         } else if (event.target === editModal) {
//             editModal.style.display = "none";
//         }
//     });

//     const users = [
//         {
//             userID: 1,
//             email: 'user1@example.com',
//             username: 'user1',
//             role: 'Admin',
//         },
//         {
//             userID: 2,
//             email: 'user2@example.com',
//             username: 'user2',
//             role: 'User',
//         },
//     ];
//     // replace with actual contents from db

//     // Function to update the user content row based on the search input
//     function updateContent(searchText) {
//         const userContentRow = document.getElementById('userContent');
//         userContentRow.innerHTML = '';
//         for (const user of users) {
//             if (
//                 user.userID.toString().includes(searchText) ||
//                 user.email.includes(searchText) ||
//                 user.username.includes(searchText) ||
//                 user.role.includes(searchText)
//             ) {
//                 const newRow = document.createElement('div');
//                 newRow.classList.add('row');

//                 newRow.innerHTML = `
//             <div class="row" id="userContentRow">
//               <div class="col-md-2">
//                 <div class="row">
//                   <a>${user.userID}</a>
//                 </div>
//               </div>
//               <div class="col-md-3">
//                 <div class="row">
//                 <a id="userEmailPlaceholder">${user.email}</a>
//                 </div>
//               </div>
//               <div class="col-md-3">
//                 <div class="row">
//                 <a id="userUsernamePlaceholder">${user.username}</a>
//                 </div>
//               </div>
//               <div class="col-md-1">
//                 <div class="row">
//                   <a>${user.role}</a>
//                 </div>
//               </div>
//               <div class="col-md-3">
//                 <div class="row">
//                   <button id="editUser" class="btn btn-primary">Edit User</button>
//                   <button id="deleteUser" class="btn btn-danger">Delete User</button>
//                 </div>
//               </div>
//             </div>
//             `;
//                 userContentRow.appendChild(newRow);
//             }
//         }

//         console.log('userEmailPlaceholder text content:', userEmailPlaceholder.textContent);
//         console.log('userUsernamePlaceholder text content:', userUsernamePlaceholder.textContent);


//     }


//     document.getElementById('searchButton').addEventListener('click', function () {
//         const searchText = document.getElementById('searchInput').value.toLowerCase();
//         updateContent(searchText);
//     });

//     // Initial load
//     updateContent(''); // Display all users on initial load


//     function openDeleteModal() {
//         deleteModal.style.display = "block";
//         // TODO: logic for deleting user
//     }

//     function openEditModal(email, username) {
//         const editUserEmailInput = document.getElementById('editUserEmail');
//         const editUserUsernameInput = document.getElementById('editUserUsername');

//         editUserEmailInput.value = email;
//         editUserUsernameInput.value = username;

//         editModal.style.display = "block";
//     }
    
//     document.getElementById('userContent').addEventListener('click', (event) => {
//         const target = event.target;

//         console.log('userEmailPlaceholder text content:', userEmailPlaceholder.textContent);
//         console.log('userUsernamePlaceholder text content:', userUsernamePlaceholder.textContent);

//         // TODO: fix edit modal, it doesn't display the correct email and username

//         if (target.id === 'editUser') {
//             const parentRow = target.closest('.row');
//             const email = parentRow.querySelector('#userEmailPlaceholder').textContent;
//             const username = parentRow.querySelector('#userUsernamePlaceholder').textContent;
//             openEditModal(email, username);
//         } else if (target.id === 'deleteUser') {
//             openDeleteModal();
//         }
//     });
// });


