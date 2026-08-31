console.log("checkout.js loaded");

document.addEventListener("DOMContentLoaded", () => {
  const placeOrderBtn = document.getElementById("place-order-btn");

  if (!placeOrderBtn) {
    console.warn("Place Order button not found.");
    return;
  }

  placeOrderBtn.addEventListener("click", async () => {
    const data = collectOrderData();  // assume que esta função está definida

    const errors = validateCheckoutData(data); // assume que esta função está definida
    if (errors.length > 0) {
      showStatus(errors.join("\n"), false);
      return;
    }

    try {
      // Get cart data to calculate total ourselves
      const cartDataRes = await fetch("/cart_data");
      const cartData = await cartDataRes.json();
      
      if (!cartData.success) {
        showStatus("unable to retrieve cart data.", false);
        return;
      }
      
      // Calculate total using the SAME logic as in script.js
      const subtotal = cartData.items.reduce((sum, item) => {
        const price = parseFloat(item.price) || 0;
        const quantity = parseInt(item.quantity) || 0;
        return sum + (price * quantity);
      }, 0);
      
      let discountValue = 0;
      let totalAfterDiscount = subtotal;
      let discountDetails = null;
      
      if (cartData.discount) {
        const discountAmount = cartData.discount.amount;
        const isPercentage = cartData.discount.is_percentage;
        
        if (isPercentage) {
          discountValue = subtotal * (discountAmount / 100);
        } else {
          discountValue = discountAmount;
        }
        
        totalAfterDiscount = subtotal - discountValue;
        
        // Store discount details to send to server
        discountDetails = {
          code: cartData.discount.code || '',
          amount: discountAmount,
          is_percentage: isPercentage,
          value_applied: discountValue
        };
      }
      
      // Add shipping cost
      const shippingCost = parseFloat(sessionStorage.getItem("shipping_cost")) || 0;
      const totalWithShipping = totalAfterDiscount + shippingCost;
      
      // Use this total for validation and order
      const totalConfirmed = totalWithShipping;
      
      // Override the calculated total from API
      data.total_confirmed = totalConfirmed;
      data.subtotal = subtotal;
      data.discount_value = discountValue;
      data.shipping_cost = shippingCost;
      data.discount_details = discountDetails;
      data.client_calculated_total = true; // Retained for UI diagnostics only.
      
      
      // Check if payment method is noted_cash and validate balance
      if (data.paymentMethod === 'account') {
        const userBalance = parseFloat(document.querySelector('.user-balance')?.textContent.match(/[\d.]+/) || 0);
        
        console.log("User balance:", userBalance, "Total after discounts:", totalConfirmed);
        
        if (totalConfirmed > 0 && userBalance < totalConfirmed) {
          showStatus(`failed - insufficient noted cash balance. you have ${userBalance.toFixed(2)}€ but the order total is ${totalConfirmed.toFixed(2)}€.`, false);
          return;
        }
      }
      
      // Submit the server-validated order.
      // success - send order to backend
      const response = await fetch("/place-order", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
      });

      const result = await response.json();

      if (response.ok && result.success) {
        showStatus("success - order placed successfully!", true);
        setTimeout(() => {
          window.location.href = "/thank-you";  // ou "/account"
        }, 1500);
      } else {
        console.error("failed - order placement failed:", result.message);
        showStatus("failed - " + (result.message || "unknown error"), false);
      }

    } catch (err) {
      console.error("Order placement failed:", err);
      showStatus("unexpected error occurred: " + err.message, false);
    }
  });
});
