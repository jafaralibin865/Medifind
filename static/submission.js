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

    const form = document.getElementById('hospital-registration-form');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(form);

        const name = formData.get('hospital-name')?.trim();
        const county = formData.get('county');
        const email = formData.get('contact-email')?.trim();

        // Simple validation
        if (!name || !county || !email || !email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
            if (!name) document.getElementById('hospital-name-error').style.display = 'block';
            if (!county) document.getElementById('county-error').style.display = 'block';
            if (!email || !email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
                document.getElementById('email-error').style.display = 'block';
            }
            return;
        }

        try {
            const response = await fetch('/register', {
                method: 'POST',
                body: formData
            });

            if (!response.redirected && !response.ok) {
                throw new Error("Submission failed");
            }

            // If redirect occurs, go to success page
            if (response.redirected) {
                window.location.href = response.url;
            }
        } catch (error) {
            document.getElementById('submission-feedback').innerHTML = `
                <div class="error-message">❌ Submission failed. Try again later.</div>`;
        }
    });
});
