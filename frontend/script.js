document.getElementById('bookingForm').addEventListener('submit', async function (e) {
  e.preventDefault();

  const formData = {
    name: this.name.value,
    email: this.email.value,
    service: this.service.value,
    date: this.date.value,
  };

  try {
    const response = await fetch('http://localhost:5000/book', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData),
    });

    const result = await response.json();
    document.getElementById('confirmation').innerText = result.message;
  } catch (error) {
    console.error('Error submitting booking:', error);
    document.getElementById('confirmation').innerText = 'Something went wrong. Please try again.';
  }
});