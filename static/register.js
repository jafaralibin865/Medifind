document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("registerForm");

  form.addEventListener("submit", async function (e) {
    e.preventDefault(); // prevent form from refreshing

    const formData = new FormData(form);
    const data = new URLSearchParams(formData);

    try {
      const response = await fetch("/register", {
        method: "POST",
        headers: {
          "Accept": "text/html", // Expect HTML response
          "Content-Type": "application/x-www-form-urlencoded"
        },
        body: data
      });

      if (response.redirected) {
        // Follow the redirection to login or error page
        window.location.href = response.url;
      } else {
        const text = await response.text();
        console.log("Registration response:", text);
      }
    } catch (error) {
      console.error("Error submitting registration:", error);
    }
  });
});
