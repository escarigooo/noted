console.log('Checkout core script loaded');
function collectOrderData() {
  const sameAddress = document.getElementById('same_address')?.checked;

  return {
    shipping: {
      first_name: document.getElementById('first_name')?.value.trim(),
      last_name: document.getElementById('last_name')?.value.trim(),
      street_address: document.getElementById('street_address')?.value.trim(),
      city: document.getElementById('city')?.value.trim(),
      state: document.getElementById('state')?.value.trim(),
      zip_code: document.getElementById('zip_code')?.value.trim(),
      country: document.getElementById('country')?.value.trim(),
      phone: document.getElementById('phone')?.value.trim(),
      email: document.getElementById('email')?.value.trim()
    },
    billingSameAsShipping: sameAddress,
    billing: {
      street_address: document.getElementById('billing_street')?.value.trim(),
      city: document.getElementById('billing_city')?.value.trim(),
      state: document.getElementById('billing_state')?.value.trim(),
      zip_code: document.getElementById('billing_zip_code')?.value.trim(),
      country: document.getElementById('billing_country')?.value.trim()
    },
    shippingMethod: getSelectedValue('shipping_method'),
    paymentMethod: getSelectedValue('payment_method'),
    payment: {
      card_number: document.querySelector('input[name="card_number"]')?.value.trim(),
      expiry: document.querySelector('input[name="expiration"]')?.value.trim(),
      cvv: document.querySelector('input[name="security_code"]')?.value.trim(),
      name_on_card: document.querySelector('input[name="card_name"]')?.value.trim()
    }
  };
}
