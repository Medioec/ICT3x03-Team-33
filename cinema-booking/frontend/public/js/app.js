
document.addEventListener("DOMContentLoaded", function () {
  // Get references to the dropdown buttons and their respective menus
  var movieDropdown = document.getElementById("movieDropdown");
  var cinemaDropdown = document.getElementById("cinemaDropdown");
  var timingDropdown = document.getElementById("timingDropdown");
  var showtimesButton = document.getElementById("showtimes");
  var resetButton = document.getElementById("reset");

  // Initialize flags for the dropdowns within an object
  var dropdownFlags = {
    movieSelected: false,
    cinemaSelected: false,
    timingSelected: false,
  };

  // Function to enable or disable the timing dropdown based on movie and cinema selections
  function enableTimingDropdown() {
    if (dropdownFlags.cinemaSelected && dropdownFlags.movieSelected) {
      timingDropdown.removeAttribute("disabled");
    } else {
      timingDropdown.textContent = "Select a Timeslot";
    } 
  }

  // Add event listeners to update the button text and set the corresponding flag
  function addDropdownController(dropdownButton, dropdownMenu, flag) {
    var dropdownItems = dropdownMenu.querySelectorAll(".dropdown-item");
    dropdownItems.forEach(function (item) {
      item.addEventListener("click", function () {
        dropdownButton.textContent = item.textContent;
        dropdownFlags[flag] = true; // Update the flag via the object
        enableShowtimesButton();
        enableTimingDropdown();
      });
    });
  }

  // Attach event listeners to the Bootstrap Select custom event "changed.bs.select"
  $(movieDropdown).on("changed.bs.select", function (e, clickedIndex, newValue, oldValue) {
    console.log("Movie dropdown changed: ", newValue, oldValue);
    dropdownFlags.movieSelected = true;
    enableShowtimesButton();
    enableTimingDropdown();
  });

  $(cinemaDropdown).on("changed.bs.select", function (e, clickedIndex, newValue, oldValue) {
    console.log("Cinema dropdown changed: ", newValue, oldValue);
    dropdownFlags.cinemaSelected = true;
    enableShowtimesButton();
    enableTimingDropdown();
  });

  // Add a click event listener to the "Reset" button
  resetButton.addEventListener("click", function () {
    // Reset the flags to false
    dropdownFlags.movieSelected = false;
    dropdownFlags.cinemaSelected = false;
    dropdownFlags.timingSelected = false;

    movieDropdown.textContent = "Select a Movie";
    cinemaDropdown.textContent = "Select a Cinema";
    timingDropdown.textContent = "Select a Timeslot";

    // Disable the timing dropdown
    timingDropdown.setAttribute("disabled", "true");

    // Disable the "Showtimes" button
    showtimesButton.setAttribute("disabled", "true");
  });

  // Enable the "Showtimes" button
  function enableShowtimesButton() {
    if (dropdownFlags.cinemaSelected || dropdownFlags.movieSelected) {
      showtimesButton.removeAttribute("disabled");
    }
  }

  // Check the dropdown combinations and determine the expected behavior
  showtimesButton.addEventListener("click", function () {
    if (dropdownFlags.cinemaSelected && !dropdownFlags.movieSelected && !dropdownFlags.timingSelected) {
      // Redirect to cinema page
      console.log("state: cinemaSelected && !movieSelected && !timingSelected");
    } else if (!dropdownFlags.cinemaSelected && dropdownFlags.movieSelected && !dropdownFlags.timingSelected) {
      // Redirect to movie details page
      console.log("state: !cinemaSelected && movieSelected && !timingSelected");
    } else if (dropdownFlags.cinemaSelected && dropdownFlags.movieSelected && !dropdownFlags.timingSelected) {
      // Redirect to movie details page with cinemaId
      console.log("state: cinemaSelected && movieSelected && !timingSelected");
    } else if (!dropdownFlags.cinemaSelected && !dropdownFlags.movieSelected && dropdownFlags.timingSelected) {
      // Button remains disabled
      console.log("state: !cinemaSelected && !movieSelected && timingSelected");
    } else if (dropdownFlags.cinemaSelected && !dropdownFlags.movieSelected && dropdownFlags.timingSelected) {
      // Button remains disabled
      console.log("state: cinemaSelected && !movieSelected && timingSelected");
    } else if (!dropdownFlags.cinemaSelected && dropdownFlags.movieSelected && dropdownFlags.timingSelected) {
      // Button remains disabled
      console.log("state: !cinemaSelected && movieSelected && timingSelected");
    } else if (dropdownFlags.cinemaSelected && dropdownFlags.movieSelected && dropdownFlags.timingSelected) {
      // Redirect to seat selection page
      console.log("state: cinemaSelected && movieSelected && timingSelected");
    }
  });

  // Disable the timing dropdown by default
  timingDropdown.setAttribute("disabled", "true");

  // Add controllers for each dropdown and set the corresponding flags
  addDropdownController(movieDropdown, movieDropdown.nextElementSibling, "movieSelected");
  addDropdownController(cinemaDropdown, cinemaDropdown.nextElementSibling, "cinemaSelected");
  addDropdownController(timingDropdown, timingDropdown.nextElementSibling, "timingSelected");
});
