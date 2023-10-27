document.addEventListener('DOMContentLoaded', () => {
    const deleteModal = document.getElementById("delete-modal");
    const editModal = document.getElementById("edit-modal");
    const closeDeleteModalButton = document.getElementById("close-delete-modal");
    const closeEditModalButton = document.getElementById("close-edit-modal");
    const confirmDeleteButton = document.getElementById("confirm-delete");
    const confirmEditButton = document.getElementById("confirm-edit");
    const cancelDeleteButton = document.getElementById("cancel-delete");
    const cancelEditButton = document.getElementById("cancel-edit");


    const editUserEmailInput = document.getElementById('editUserEmail');
    const editUserUsernameInput = document.getElementById('editUserUsername');
    const userEmailPlaceholder = document.getElementById('userEmailPlaceholder');
    const userUsernamePlaceholder = document.getElementById('userUsernamePlaceholder');

    ////////////////////////// to close modal //////////////////////////
    closeDeleteModalButton.addEventListener("click", () => {
        deleteModal.style.display = "none";
    });

    closeEditModalButton.addEventListener("click", () => {
        editModal.style.display = "none";
    });

    cancelDeleteButton.addEventListener("click", () => {
        deleteModal.style.display = "none";
    });

    cancelEditButton.addEventListener("click", () => {
        editModal.style.display = "none";
    });
    //////////////////////////       end       //////////////////////////

    confirmDeleteButton.addEventListener("click", () => {
        deleteModal.style.display = "none";
        // TODO: Delete user
    });

    confirmEditButton.addEventListener("click", () => {
        editModal.style.display = "none";
        // TODO: Modify email and username fields 
    });

    window.addEventListener("click", (event) => {
        if (event.target === deleteModal) {
            deleteModal.style.display = "none";
        } else if (event.target === editModal) {
            editModal.style.display = "none";
        }
    });

    const users = [
        {
            userID: 1,
            email: 'user1@example.com',
            username: 'user1',
            role: 'Admin',
        },
        {
            userID: 2,
            email: 'user2@example.com',
            username: 'user2',
            role: 'User',
        },
    ];
    // replace with actual contents from db

    // Function to update the user content row based on the search input
    function updateContent(searchText) {
        const userContentRow = document.getElementById('userContent');
        userContentRow.innerHTML = '';
        for (const user of users) {
            if (
                user.userID.toString().includes(searchText) ||
                user.email.includes(searchText) ||
                user.username.includes(searchText) ||
                user.role.includes(searchText)
            ) {
                const newRow = document.createElement('div');
                newRow.classList.add('row');

                newRow.innerHTML = `
            <div class="row" id="userContentRow">
              <div class="col-md-2">
                <div class="row">
                  <a>${user.userID}</a>
                </div>
              </div>
              <div class="col-md-3">
                <div class="row">
                <a id="userEmailPlaceholder">${user.email}</a>
                </div>
              </div>
              <div class="col-md-3">
                <div class="row">
                <a id="userUsernamePlaceholder">${user.username}</a>
                </div>
              </div>
              <div class="col-md-1">
                <div class="row">
                  <a>${user.role}</a>
                </div>
              </div>
              <div class="col-md-3">
                <div class="row">
                  <button id="editUser" class="btn btn-primary">Edit User</button>
                  <button id="deleteUser" class="btn btn-danger">Delete User</button>
                </div>
              </div>
            </div>
            `;
                userContentRow.appendChild(newRow);
            }
        }

        console.log('userEmailPlaceholder text content:', userEmailPlaceholder.textContent);
        console.log('userUsernamePlaceholder text content:', userUsernamePlaceholder.textContent);


    }


    document.getElementById('searchButton').addEventListener('click', function () {
        const searchText = document.getElementById('searchInput').value.toLowerCase();
        updateContent(searchText);
    });

    // Initial load
    updateContent(''); // Display all users on initial load


    function openDeleteModal() {
        deleteModal.style.display = "block";
        // TODO: logic for deleting user
    }

    function openEditModal(email, username) {
        const editUserEmailInput = document.getElementById('editUserEmail');
        const editUserUsernameInput = document.getElementById('editUserUsername');

        editUserEmailInput.value = email;
        editUserUsernameInput.value = username;

        editModal.style.display = "block";
    }
    
    document.getElementById('userContent').addEventListener('click', (event) => {
        const target = event.target;

        console.log('userEmailPlaceholder text content:', userEmailPlaceholder.textContent);
        console.log('userUsernamePlaceholder text content:', userUsernamePlaceholder.textContent);

        // TODO: fix edit modal, it doesn't display the correct email and username

        if (target.id === 'editUser') {
            const parentRow = target.closest('.row');
            const email = parentRow.querySelector('#userEmailPlaceholder').textContent;
            const username = parentRow.querySelector('#userUsernamePlaceholder').textContent;
            openEditModal(email, username);
        } else if (target.id === 'deleteUser') {
            openDeleteModal();
        }
    });
});


