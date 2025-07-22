document.addEventListener('DOMContentLoaded', function () {
  const buttons = document.querySelectorAll('.update-btn');

  buttons.forEach(button => {
    button.addEventListener('click', function () {
      const hospitalId = this.getAttribute('data-id');
      loadUpdateForm(hospitalId);
    });
  });
});

function loadUpdateForm(hospitalId) {
  fetch(`/update_hospital_partial/${hospitalId}`)
    .then(response => response.text())
    .then(html => {
      document.getElementById("main-content").innerHTML = html;
    })
    .catch(error => {
      console.error('Error loading form:', error);
      alert("Failed to load update form.");
    });
}
