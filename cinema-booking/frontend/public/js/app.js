  document.addEventListener("DOMContentLoaded", function () {
    var movieDropdown = document.getElementById("movieDropdown");

    movieDropdown.addEventListener("click", function () {
      var dropdownMenu = movieDropdown.nextElementElement;
      if (dropdownMenu.style.display === "block") {
        dropdownMenu.style.display = "none";
      } else {
        dropdownMenu.style.display = "block";
      }
    });
  });