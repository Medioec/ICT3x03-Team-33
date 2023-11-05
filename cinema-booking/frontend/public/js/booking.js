
document.addEventListener("DOMContentLoaded", function () {
  
    const showtimeId = document.getElementById('stIdLbl').textContent;
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

    let ticketPrice = 10.50; // Assuming a default price per ticket
    let selectedSeatsCount = 0;
    let selectedSeatId = null; 
    let bookedSeats;


    console.log('showtimeId: ', showtimeId);

    getAllBookedSeats(showtimeId)
      .then(data => {
        bookedSeats = data;
        // Now you can use bookedSeats safely
        if (bookedSeats.length > 0) {
          bookedSeats.forEach((bookedSeat) => {
            const seatElement = document.getElementById(bookedSeat.seatId);
    
            if (seatElement) {
              seatElement.classList.remove('seat');
              seatElement.classList.add('seat-sold');
            }
          });
        } else {
            console.log('No booked seats');        
        }
      })
      .catch(error => {
        console.error('Error fetching booked seats', error);
      });

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


    const resetButton = document.getElementById('resetButton');
    resetButton.addEventListener('click', () => {
        const selectedSeat = container.querySelector('.seat.selected');
        if (selectedSeat) {
            selectedSeat.classList.remove('selected');
        }
        updateSelectedCount();
    });
    console.log('showtimeId: ', showtimeId);

    checkoutButton.addEventListener('click', () => {
        if (loggedIn === 'true') {            
            // Check if a seat is selected using the selectedSeatId variable
            console.log('showtimeId: ', showtimeId);

            if (selectedSeatId) {
                // Construct the URL with selected seat ID and showtime ID as query parameters
                const paymentURL = `/payment?seat=${encodeURIComponent(selectedSeatId)}&showtimeId=${encodeURIComponent(showtimeId)}`;
                
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
});

  ///////////////////////////////////////////////////////////////////////////////////////////////////////////
                    // API CALLS  TO LOAD BOOKED SEATS DYNAMICALLY AND MOVIE DATA //
  ///////////////////////////////////////////////////////////////////////////////////////////////////////////

  async function getAllBookedSeats(showtimeId) {
    try {
      const response = await fetch('/getAllBookedSeats', {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(showtimeId),
      });
  
      if (!response.ok) {
        console.error('Response not OK. Status:', response.status);
        throw new Error('Failed to get booked seats');
      } else {
        // Handle the case when the response is not in the expected format
        console.error('Invalid response format:', data);
      }
      return response.json();  
    } 
    catch (error) {
      console.error('Error in getAllBookedSeats:', error);
      throw error;
    }
  }
  

  