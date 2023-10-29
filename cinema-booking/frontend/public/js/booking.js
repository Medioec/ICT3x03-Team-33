const container = document.querySelector('.seatContainer');
const seats = document.querySelectorAll('.row .seat:not(.occupied)');
const count = document.getElementById('count');
const total = document.getElementById('total');
const selectedSeatsDisplay = document.getElementById('selectedSeatsDisplay');
const checkoutButton = document.getElementById('checkoutButton');
const loginModal = document.getElementById('loginModal');
const modalOverlay = document.getElementById('modalOverlay');
const modalCloseBtn = document.getElementById('modalCloseBtn');
const modalCancelButton = document.getElementById('cancelButton');
const loggedIn = checkoutButton.getAttribute('data-loggedin');

populateUI();

let ticketPrice = 0;
let selectedSeatsCount = -1;

function updateSelectedCount() {
    selectedSeats = document.querySelectorAll('.row .seat.selected');
    const selectedSeatIds = [...selectedSeats].map(seat => seat.id);
    localStorage.setItem('selectedSeats', JSON.stringify(selectedSeatIds));
    selectedSeatsCount = selectedSeats.length;

    count.innerText = selectedSeatsCount;
    ticketPrice = selectedSeatsCount > 0 ? 10.50 : 0;
    total.innerText = selectedSeatsCount * ticketPrice;

    // Display selected seat IDs in the selectedSeatsDisplay element
    selectedSeatsDisplay.innerText = selectedSeatIds.join(', '); // Display as a comma-separated list
}

function populateUI() {
    const selectedSeats = JSON.parse(localStorage.getItem('selectedSeats'));

    if (selectedSeats !== null && selectedSeats.length > 0) {
        seats.forEach((seat, index) => {
            if (selectedSeats.indexOf(index) > -1) {
                seat.classList.add('selected');
            }
        });
    }
}

container.addEventListener('click', (e) => {
    if (
        e.target.classList.contains('seat') &&
        !e.target.classList.contains('sold') &&
        !e.target.classList.contains('reserved') &&
        !e.target.classList.contains('display')
    ) {
        e.target.classList.toggle('selected');
        updateSelectedCount();
    }
});

// Add an event listener to the reset button
const resetButton = document.getElementById('resetButton');
resetButton.addEventListener('click', () => {
    // Deselect all selected seats
    selectedSeats.forEach(seat => seat.classList.remove('selected'));

    // Clear the selected seats in the local storage
    localStorage.removeItem('selectedSeats');

    // Update the selected seat count, price, and display
    updateSelectedCount();
});

checkoutButton.addEventListener('click', () => {
    if (loggedIn === 'true') {
        // User is logged in, continue with checkout logic
    } else {
        // User is not logged in, show the modal
        loginModal.style.display = 'block';
        modalOverlay.style.display = 'block';
    }
});

// Close the modal when the close button or "Cancel" button is clicked
modalCloseBtn.addEventListener('click', () => {
    loginModal.style.display = 'none';
    modalOverlay.style.display = 'none';
});

modalCancelButton.addEventListener('click', () => {
    loginModal.style.display = 'none';
    modalOverlay.style.display = 'none';
});

modalOverlay.addEventListener('click', () => {
    loginModal.style.display = 'none';
    modalOverlay.style.display = 'none';
});

updateSelectedCount();



