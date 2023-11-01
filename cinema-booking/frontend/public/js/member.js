document.querySelector("#location").addEventListener("click", geoFindMe);

function geoFindMe() {
  const status = document.querySelector("#status");

  function success(position) {
    const userLat = position.coords.latitude;
    const userLong = position.coords.longitude;

    status.textContent = "";

    // After obtaining the user's location, find the nearest cinema
    const userLocation = { lat: userLat, lng: userLong };
    const nearestCinema = findNearestCinema(userLocation, cinemaLocations);
    if (nearestCinema) {
      // pass over cinemaId in the url
      const cinemaName = nearestCinema.name;
      // check for cinemaName's cinemaId in the cinemaMapping
      const cinemaId = cinemaMapping[cinemaName];
      status.textContent = `The nearest cinema is ${nearestCinema.name}, ${cinemaId}.`;
      // Redirect to the nearest cinema page
      // window.location.href = "/cinemas?cinemaId=" + cinemaId;
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

function findNearestCinema(userLocation, cinemaLocations) {
  let nearestCinema = null;
  let minDistance = Infinity;

  for (const cinema of cinemaLocations) {
    const distance = calculateDistance(userLocation.lat, userLocation.lng, cinema.lat, cinema.lng);

    if (distance < minDistance) {
      minDistance = distance;
      nearestCinema = cinema;
    }
  }

  return nearestCinema;
}

  // Define the cinemaMapping
  const cinemaMapping = {
    'Golden Village Tampines': 1,
    'Shaw JCube': 2,
    'Cathay AMK Hub': 3,
    'GV Suntec City': 4,
    'The Projector': 5,
};

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
