// JavaScript to update the dropdown button text
document.addEventListener('click', function (event) {
    const dropdownBtn = event.target.closest('.dropdown').querySelector('.btn');
    const dropdownItem = event.target.closest('.dropdown-item');
  
    if (dropdownBtn && dropdownItem) {
      dropdownBtn.textContent = dropdownItem.textContent;
    }
  });
  