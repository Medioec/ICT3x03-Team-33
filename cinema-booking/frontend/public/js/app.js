document.addEventListener("DOMContentLoaded", function () {
  var movieDropdown = document.getElementById("movieDropdown");
  var cinemaDropdown = document.getElementById("cinemaDropdown");
  var timingDropdown = document.getElementById("timingDropdown");
  var showtimesButton = document.getElementById("showtimes");
  var resetButton = document.getElementById("reset");

  var dropdownFlags = {
    movieSelected: false,
    cinemaSelected: false,
    timingSelected: false,
  };

  const cinemaMapping = {
    'Golden Village Tampines': 1,
    'Shaw JCube': 2,
    'Cathay AMK Hub': 3,
    'GV Suntec City': 4,
    'The Projector': 5,
  };

  function enableTimingDropdown() {
    if (dropdownFlags.cinemaSelected && dropdownFlags.movieSelected) {
      updateTimingDropdown();
      timingDropdown.removeAttribute("disabled");
      console.log("if enableTimingDropdown is true:", timingDropdown.textContent);
    } else {
      timingDropdown.setAttribute("disabled", "true");
      console.log("if enableTimingDropdown is false", timingDropdown.textContent); 
    }
  }

  function updateTimingDropdownValue(selectedValue) {
    timingDropdown.textContent = selectedValue;
    dropdownFlags.timingSelected = true;
    enableShowtimesButton();
    enableTimingDropdown();
  }

  function addTimingDropdownController(dropdownMenu) {
    var dropdownItems = dropdownMenu.querySelectorAll(".dropdown-item");
    dropdownItems.forEach(function (item) {
      item.addEventListener("click", function () {
        var selectedValue = item.textContent;
        updateTimingDropdownValue(selectedValue);
      });
    });
  }

// Declare the showtimeInfoArray as a global variable
const showtimeInfoArray = [];

  function updateTimingDropdown() {
    const selectedCinema = cinemaDropdown.textContent;
    const selectedMovieTitle = movieDropdown.textContent;

    const selectedCinemaId = cinemaMapping[selectedCinema];
    const selectedMovie = moviesData.find(movie => movie.title === selectedMovieTitle);

    // Clear the existing dropdown items
    const dropdownMenu = document.getElementById('timingInnerMenu');
    dropdownMenu.innerHTML = '';

    if (selectedCinemaId && selectedMovie) {
      const movieId = selectedMovie.movieId;

      const matchingShowtimes = showtimeData.filter(item => item.movieId === movieId && item.cinemaId === selectedCinemaId);

      // Sort matching showtimes by showDate and showTime
      matchingShowtimes.sort((a, b) => {
        const aDate = new Date(a.showDate + ' ' + a.showTime);
        const bDate = new Date(b.showDate + ' ' + b.showTime);
        return aDate - bDate;
      });

      // Clear the showtimeInfoArray before populating it
      showtimeInfoArray.length = 0;

      addTimingDropdownController(timingDropdown.nextElementSibling);

      matchingShowtimes.forEach(showtime => {
        const dropdownItem = document.createElement('li');
        const showtimeInfo = {
          showDate: showtime.showDate,
          showTime: showtime.showTime,
          showtimeId: showtime.showtimeId,
        };
        dropdownItem.innerHTML = `<a class="dropdown-item">${showtime.showDate}, ${showtime.showTime}</a>`;
        dropdownMenu.appendChild(dropdownItem);

        dropdownItem.addEventListener("click", function () {
          var selectedValue = `${showtime.showDate}, ${showtime.showTime}`;
          updateTimingDropdownValue(selectedValue);
        });

        // Push the showtime information to the global array
        showtimeInfoArray.push(showtimeInfo);
      });

    }
  }

  function addDropdownController(dropdownButton, dropdownMenu, flag) {
    var dropdownItems = dropdownMenu.querySelectorAll(".dropdown-item");
    dropdownItems.forEach(function (item) {
      item.addEventListener("click", function () {
        dropdownButton.textContent = item.textContent;
        dropdownFlags[flag] = true;
        enableShowtimesButton();
        enableTimingDropdown();
      });
    });
  }

  // Attach event listeners to the Bootstrap Select custom event "changed.bs.select"
  $(movieDropdown).on("changed.bs.select", function (e, clickedIndex, newValue, oldValue) {
    dropdownFlags.movieSelected = true;
    enableShowtimesButton();
    enableTimingDropdown();
  });

  $(cinemaDropdown).on("changed.bs.select", function (e, clickedIndex, newValue, oldValue) {
    dropdownFlags.cinemaSelected = true;
    enableShowtimesButton();
    enableTimingDropdown();
  });

    // Add event listeners for timingDropdown
  $(timingDropdown).on("changed.bs.select", function (e, clickedIndex, newValue, oldValue) {
    dropdownFlags.timingSelected = true;
    console.log("timingDropdown changed", dropdownFlags.timingSelected)
  });

  resetButton.addEventListener("click", function () {
    dropdownFlags.movieSelected = false;
    dropdownFlags.cinemaSelected = false;
    dropdownFlags.timingSelected = false;

    movieDropdown.textContent = "Select a Movie";
    cinemaDropdown.textContent = "Select a Cinema";
    timingDropdown.textContent = "Select a Timeslot";

    timingDropdown.setAttribute("disabled", "true");
    showtimesButton.setAttribute("disabled", "true");
  });

  function enableShowtimesButton() {
    if (dropdownFlags.cinemaSelected || dropdownFlags.movieSelected) {
      showtimesButton.removeAttribute("disabled");
    }
  }

  showtimesButton.addEventListener("click", function () {
    const selectedMovieTitle = movieDropdown.textContent;
    const selectedCinema = cinemaDropdown.textContent;
    const selectedTiming = timingDropdown.textContent;
    const selectedMovie = moviesData.find(movie => movie.title === selectedMovieTitle);
    const movieId = selectedMovie.movieId;
    const selectedCinemaId = cinemaMapping[selectedCinema];
  
    console.log("selectedMovie:", selectedMovieTitle);
    console.log("selectedMovieId:", movieId);
    console.log("selectedCinema:", selectedCinema);
    console.log("selectedCinemaId:", selectedCinemaId);
    console.log("selectedTiming:", selectedTiming);
  
    // Find the showtimeId by matching selectedTiming with showtimeInfoArray
    const selectedShowtime = showtimeInfoArray.find(showtime => {
      const showtimeString = `${showtime.showDate}, ${showtime.showTime}`;
      return showtimeString === selectedTiming;
    });
  
    if (selectedShowtime) {
      const showtimeId = selectedShowtime.showtimeId;
      console.log("selectedShowtimeId:", showtimeId);
    } else {
      console.log("No matching showtime found.");
    }

    if (dropdownFlags.cinemaSelected && !dropdownFlags.movieSelected && !dropdownFlags.timingSelected) {
      // Redirect to cinema page
      console.log("state: cinemaSelected && !movieSelected && !timingSelected");
    } else if (!dropdownFlags.cinemaSelected && dropdownFlags.movieSelected && !dropdownFlags.timingSelected) {
      // Redirect to movie details page with the selected movieId
      if (selectedMovie) {
        const movieId = selectedMovie.movieId;
        window.location.href = "/moviedetails?movieId=" + movieId;
      }
    } else if (dropdownFlags.cinemaSelected && dropdownFlags.movieSelected && !dropdownFlags.timingSelected) {
      // Redirect to movie details page with cinemaId
      console.log("state: cinemaSelected && movieSelected && !timingSelected");
    } else if (dropdownFlags.cinemaSelected && dropdownFlags.movieSelected && dropdownFlags.timingSelected) {
      // Redirect to booking page with the selected showtimeId
      if (selectedShowtime) {
        const showtimeId = selectedShowtime.showtimeId;
        const bookingURL = `/booking?showtimeId=${showtimeId}`;
        window.location.href = bookingURL;
      } else {
        console.log("No matching showtime found for booking.");
      }
      console.log("state: cinemaSelected && movieSelected && timingSelected");
    }
    // other scenarios involving the "Showtimes" button are not possible (data not loaded in)
  });

  timingDropdown.setAttribute("disabled", "true");

  addDropdownController(movieDropdown, movieDropdown.nextElementSibling, "movieSelected");
  addDropdownController(cinemaDropdown, cinemaDropdown.nextElementSibling, "cinemaSelected");
  addDropdownController(timingDropdown, timingDropdown.nextElementSibling, "timingSelected");
  
  updateTimingDropdown();
});