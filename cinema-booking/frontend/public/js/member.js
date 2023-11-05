async function getAllCinemas() {
  try {
      const response = await fetch('/getAllCinemas', {
          method: 'GET',
          headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json'
          }
      });

      if (!response.ok) {
          console.error('Response not OK. Status:', response.status);
          throw new Error('Failed to get all cinemas');
      }

      return response.json();
  } catch (error) {
      console.error('Error in getAllCinemas:', error);
      throw error;
  }
}

document.addEventListener("DOMContentLoaded", function () {


  document.querySelector("#location").addEventListener("click", geoFindMe);

  let cinemaData;

  getAllCinemas()
  .then(data => {
    cinemaData = data;
  })
  .catch(error => {
    console.error('Error fetching cinema data:', error);
  });


  function geoFindMe() {
    const status = document.querySelector("#status");

    function success(position) {
      const userLat = position.coords.latitude;
      const userLng = position.coords.longitude;

      status.textContent = "";

      // After obtaining the user's location, find the nearest cinema
      const userLocation = { lat: userLat, lng: userLng };
      const nearestCinema = findNearestCinema(userLocation, cinemaLocations, cinemaData);
      if (nearestCinema) {
        // Pass over cinemaId in the URL
        const cinemaName = nearestCinema.cinemaName;
        const cinemaId = nearestCinema.cinemaId;
        status.textContent = `The nearest cinema is ${cinemaName}, ${cinemaId}.`;
        // Redirect to the nearest cinema page
        window.location.href = "/cinemas?cinemaId=" + cinemaId;
      } else {
        status.textContent = "No cinemas found.";
      }
    }

    function error() {
      status.textContent = "Unable to retrieve your location";
    }

    if (!navigator.geolocation) {
      status.textContent = "Geolocation is not supported by your browser";
    } else {
      status.textContent = "Locating…";
      navigator.geolocation.getCurrentPosition(success, error);
    }
  }

  function calculateDistance(lat1, lng1, lat2, lng2) {
    const radian = Math.PI / 180;
    const dLat = (lat2 - lat1) * radian;
    const dLng = (lng2 - lng1) * radian;
    const a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(lat1 * radian) * Math.cos(lat2 * radian) * Math.sin(dLng / 2) * Math.sin(dLng / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    const earthRadius = 6371; // Earth's radius in kilometers
    return earthRadius * c;
  }

  function findNearestCinema(userLocation, cinemaLocations, cinemaData) {
    let nearestCinema = null;
    let minDistance = Infinity;

    for (const cinema of cinemaLocations) {
      const cinemaDataItem = cinemaData.find((item) => item.cinemaName === cinema.name);
      if (cinemaDataItem) {
        const distance = calculateDistance(userLocation.lat, userLocation.lng, cinema.lat, cinema.lng);

        if (distance < minDistance) {
          minDistance = distance;
          nearestCinema = cinemaDataItem;
        }
      }
    }

    return nearestCinema;
  }

  const cinemaLocations = [
    {
      name: 'Golden Village Tampines',
      lat: 1.3523764053191365,
      lng: 103.94441794172593
    },
    {
      name: 'Shaw JCube',
      lat: 1.3336011469216356,
      lng: 103.73986263786222
    },
    {
      name: 'Cathay AMK Hub',
      lat: 1.3698768913380295,
      lng: 103.8481612801913
    },
    {
      name: 'GV Suntec City',
      lat: 1.2961700770717264,
      lng: 103.85796816854551
    },
    {
      name: 'The Projector',
      lat: 1.3021293157453337,
      lng: 103.86405791087472
    }
  ];
});
