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

// uncomment the following line to populate the UI with the cached selected seat ID
populateUI();

let ticketPrice = 10.50; // Assuming a default price per ticket
let selectedSeatsCount = 0;
let selectedSeatId = null; 

function updateSelectedCount() {
    const selectedSeat = document.querySelector('.row .seat.selected');
    const selectedSeatId = selectedSeat ? selectedSeat.id : null;
    // This affects the caching of the selected seat ID in localStorage
    // localStorage.setItem('selectedSeat', JSON.stringify(selectedSeatId));
    selectedSeatsCount = selectedSeat ? 1 : 0;

    count.innerText = selectedSeatsCount;
    total.innerText = selectedSeatsCount * ticketPrice;

    // Display selected seat ID in the selectedSeatsDisplay element
    selectedSeatsDisplay.innerText = selectedSeatId ? selectedSeatId : '';
}

function populateUI() {
    const selectedSeat = JSON.parse(localStorage.getItem('selectedSeat'));

    if (selectedSeat !== null) {
        seats.forEach(seat => {
            if (seat.id === selectedSeat) {
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
        // Deselect any existing selected seat
        const currentSelected = container.querySelector('.seat.selected');
        if (currentSelected && currentSelected !== e.target) {
            currentSelected.classList.remove('selected');
        }
        
        // Toggle the clicked seat
        e.target.classList.toggle('selected');
        updateSelectedCount();
        
        // Update the selectedSeatId variable
        selectedSeatId = e.target.classList.contains('selected') ? e.target.id : null;
    }
});


// Add an event listener to the reset button
const resetButton = document.getElementById('resetButton');
resetButton.addEventListener('click', () => {
    const selectedSeat = container.querySelector('.seat.selected');
    if (selectedSeat) {
        selectedSeat.classList.remove('selected');
    }
    updateSelectedCount();
});

checkoutButton.addEventListener('click', () => {
    if (loggedIn === 'true') {
        // User is logged in, continue with checkout logic
        
        // Check if a seat is selected using the selectedSeatId variable
        if (selectedSeatId) {
            const showtimeDetailsId = showtimeDetails.showtimeId; // Get the showtime ID from showtimeDetails

            // Construct the URL with selected seat ID and showtime ID as query parameters
            const paymentURL = `/payment?seat=${encodeURIComponent(selectedSeatId)}&showtimeId=${encodeURIComponent(showtimeDetailsId)}`;
            
            // Navigate to the payment page with selected seat ID and showtime ID as query parameters
            window.location.href = paymentURL;
        } else {
            // Handle the case where no seat is selected
            alert('Please select a seat before proceeding to checkout.');
        }
    } else {
        // User is not logged in, display the login modal
        loginModal.style.display = 'block';
        modalOverlay.style.display = 'block';
    }
});


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



