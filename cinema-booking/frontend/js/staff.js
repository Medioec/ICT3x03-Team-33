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

    const Showtimes = [
        {
            showtimeId: 1,
            cinemaId: 1,
            theaterId: '5A',
            movieId: 1,
            showDate: '01-11-2023',
            showTime: '10:15 PM',
        },
        {
            showtimeId: 2,
            cinemaId: 1,
            theaterId: '4A',
            movieId: 1,
            showDate: '01-11-2023',
            showTime: '03:40 PM',
        },
        {
            showtimeId: 3,
            cinemaId: 1,
            theaterId: '1B',
            movieId: 1,
            showDate: '01-11-2023',
            showTime: '09:35 AM',
        },
        {
            showtimeId: 4,
            cinemaId: 1,
            theaterId: '4B',
            movieId: 1,
            showDate: '01-11-2023',
            showTime: '12:00 PM',
        }
        // change to load from db
    ];

    // Function to update the showtime content row based on the search input
    function updateContent(searchText) {
        const showtimeContentRow = document.getElementById('showtimeContent');
        showtimeContentRow.innerHTML = '';

        for (const showtime of Showtimes) {
            if (
                showtime.showtimeId.toString().includes(searchText) ||
                showtime.cinemaId.toString().includes(searchText) ||
                showtime.theaterId.toString().includes(searchText) ||
                showtime.movieId.toString().includes(searchText) ||
                showtime.showDate.includes(searchText) ||
                showtime.showTime.includes(searchText)
            ) {
                const newRow = document.createElement('div');
                newRow.classList.add('row');

                newRow.innerHTML = `
            <div class="row" id="showtimeContentRow">
                <div class="col-md-2">
                    <div class="row">
                        <a>${showtime.showtimeId}</a>
                    </div>
                </div>
                <div class="col-md-2">
                    <div class="row">
                        <a>${showtime.cinemaId}</a>
                    </div>
                </div>
                <div class="col-md-1">
                    <div class="row">
                        <a>${showtime.theaterId}</a>
                    </div>
                </div>
                <div class="col-md-1">
                    <div class="row">
                        <a>${showtime.movieId}</a>
                    </div>
                </div>
                <div class="col-md-2">
                    <div class="row">
                        <a>${showtime.showDate}</a>
                    </div>
                </div>
                <div class="col-md-2">
                    <div class="row">
                        <a>${showtime.showTime}</a>
                    </div>
                </div>
                <div class="col-md-2">
                    <div class="row">
                        <button id="editShowtimes" class="btn btn-primary">Edit</button>
                        <button id="deleteShowtimes" class="btn btn-danger">Delete</button>
                    </div>
                </div>
            </div>
            `;

                showtimeContentRow.appendChild(newRow);
            }
        }
    }

    document.getElementById('searchButton').addEventListener('click', function () {
        const searchText = document.getElementById('searchInput').value.toLowerCase();
        updateContent(searchText);
    });

    // Initial load
    updateContent(''); // Display all showtimes on initial load


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


