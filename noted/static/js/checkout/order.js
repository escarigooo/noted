console.log("Checkout order script loaded");
function sendOrder(data) {
  if (data.billingSameAsShipping) delete data.billing;

  fetch("/place_order", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  })
    .then(response => response.json())
    .then(result => {
      if (result.success) {
        showStatus("order placed successfully!", true);
        setTimeout(() => window.location.href = "/account", 1500);
      } else {
        showStatus("failed to place order: " + (result.message || "unknown error"), false);
      }
    })
    .catch(error => {
      console.error("Error submitting order:", error);
      showStatus("an error occurred while submitting your order.", false);
    });
}