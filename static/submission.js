document.addEventListener("DOMContentLoaded", () => {
    const counties = [
          "Mombasa", "Kwale", "Kilifi", "Tana River", "Lamu", 
            "Taita-Taveta", "Garissa", "Wajir", "Mandera", 
            "Marsabit", "Isiolo", "Meru", "Tharaka-Nithi", 
            "Embu", "Kitui", "Machakos", "Makueni", "Nyandarua", 
            "Nyeri", "Kirinyaga", "Murang'a", "Kiambu", "Turkana", 
            "West Pokot", "Samburu", "Trans-Nzoia", "Uasin Gishu", 
            "Elgeyo-Marakwet", "Nandi", "Baringo", "Laikipia", 
            "Nakuru", "Narok", "Kajiado", "Kericho", "Bomet", 
            "Kakamega", "Vihiga", "Bungoma", "Busia", "Siaya", 
            "Kisumu", "Homa Bay", "Migori", "Kisii", "Nyamira", "Nairobi"
    ];

    const countySelect = document.getElementById('county');
    counties.forEach(county => {
        const option = document.createElement('option');
        option.value = county;
        option.textContent = county;
        countySelect.appendChild(option);
    });

    document.getElementById('hospital-registration-form').addEventListener('submit', async (e) => {
        e.preventDefault();

        const name = document.getElementById('hospital-name').value.trim();
        const county = document.getElementById('county').value;
        const email = document.getElementById('contact-email').value.trim();

        // Simple validation
        if (!name || !county || !email) {
            if (!name) document.getElementById('hospital-name-error').style.display = 'block';
            if (!county) document.getElementById('county-error').style.display = 'block';
            if (!email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
                document.getElementById('email-error').style.display = 'block';
            }
            return;
        }

        const data = {
            name,
            county,
            email
        };

        try {
            const response = await fetch('/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) throw new Error("Server error");

            document.getElementById('submission-feedback').innerHTML = `
                <div class="success-message">
                    Submission successful! We'll be in touch.
                </div>`;
            e.target.reset();
        } catch (error) {
            document.getElementById('submission-feedback').innerHTML = `
                <div class="error-message">Failed to submit. Try again later.</div>`;
        }
    });
});
