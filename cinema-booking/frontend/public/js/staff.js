document.addEventListener('DOMContentLoaded', () => {
    const deleteModal = document.getElementById("delete-modal");
    const editModal = document.getElementById("edit-modal");
    const closeDeleteModalButton = document.getElementById("close-delete-modal");
    const closeEditModalButton = document.getElementById("close-edit-modal");
    const confirmDeleteButton = document.getElementById("confirm-delete");
    const confirmEditButton = document.getElementById("confirm-edit");
    const cancelDeleteButton = document.getElementById("cancel-delete");
    const cancelEditButton = document.getElementById("cancel-edit");

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
        // TODO: Delete showtime
    });

    confirmEditButton.addEventListener("click", () => {
        editModal.style.display = "none";
        // TODO: Modify showDate and showTime fields 
    });

    window.addEventListener("click", (event) => {
        if (event.target === deleteModal) {
            deleteModal.style.display = "none";
        } else if (event.target === editModal) {
            editModal.style.display = "none";
        }
    });

    // causes inline js, will change to getelementbyid
    // function openTab(evt, tabName) {
    //     var i, tabcontent, tablinks;
    //     tabcontent = document.getElementsByClassName("tabcontent");
    //     for (i = 0; i < tabcontent.length; i++) {
    //         tabcontent[i].style.display = "none";
    //     }
    //     tablinks = document.getElementsByClassName("tablinks");
    //     for (i = 0; i < tablinks.length; i++) {
    //         tablinks[i].className = tablinks[i].className.replace(" active", "");
    //     }
    //     document.getElementById(tabName).style.display = "block";
    //     evt.currentTarget.className += " active";
    // }

    document.getElementById('searchButton').addEventListener('click', function () {
        const searchText = document.getElementById('searchInput').value.toLowerCase();
        updateContent(searchText);
    });

    function openDeleteModal() {
        deleteModal.style.display = "block";
        // TODO: logic for deleting user
    }

    function openEditModal() {
        editModal.style.display = "block";
        // TODO: logic for editing showtime
    }

    document.getElementById('userContent').addEventListener('click', (event) => {
        const target = event.target;

        // TODO: make modal show the selected showdate and showtime

        if (target.id === 'showtimeContent') {
            openEditModal(email, username);
        } else if (target.id === 'deleteShowtimes') {
            openDeleteModal();
        }
    });
});


