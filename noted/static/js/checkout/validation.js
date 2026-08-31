// validation.js

console.log("checkout validation.js loaded");

function isEmpty(value) {
  return !value || value.trim() === "";
}

function validateEmail(email) {
  // More comprehensive email validation
  // Checks for valid format with TLD, and disallows unusual characters
  const pattern = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$/;
  return pattern.test(email) && email.length <= 254 && email.indexOf('@') > 0;
}

function validatePhone(phone) {
  // More robust phone validation (international format)
  // Allows for country code, spaces, dashes, and parentheses
  const pattern = /^\+?[0-9\s()\-]{6,20}$/;
  return pattern.test(phone) && phone.replace(/[\s()\-]/g, '').length >= 6;
}

function validateName(name, fieldName) {
  const errors = [];
  if (isEmpty(name)) {
    errors.push(`${fieldName} is required.`);
  } else {
    if (name.length < 2) errors.push(`${fieldName} must be at least 2 characters.`);
    if (name.length > 50) errors.push(`${fieldName} must be less than 50 characters.`);
    if (!/^[a-zA-ZÀ-ÿ\s\-'\.]+$/.test(name)) errors.push(`${fieldName} contains invalid characters.`);
  }
  return errors;
}

function validateStreetAddress(address, fieldName) {
  const errors = [];
  if (isEmpty(address)) {
    errors.push(`${fieldName} is required.`);
  } else {
    if (address.length < 5) errors.push(`Please enter a complete ${fieldName.toLowerCase()}.`);
    if (address.length > 100) errors.push(`${fieldName} must be less than 100 characters.`);
    // Allow letters, numbers, spaces, common punctuation for addresses
    if (!/^[a-zA-Z0-9À-ÿ\s\-\.,#\/]+$/.test(address)) errors.push(`${fieldName} contains invalid characters.`);
  }
  return errors;
}

function validateCity(city, fieldName) {
  const errors = [];
  if (isEmpty(city)) {
    errors.push(`${fieldName} is required.`);
  } else {
    if (city.length < 2) errors.push(`Please enter a valid ${fieldName.toLowerCase()}.`);
    if (city.length > 50) errors.push(`${fieldName} must be less than 50 characters.`);
    // Allow letters, spaces, hyphens, apostrophes for city names
    if (!/^[a-zA-ZÀ-ÿ\s\-'\.]+$/.test(city)) errors.push(`${fieldName} contains invalid characters.`);
  }
  return errors;
}

function validateState(state, fieldName) {
  const errors = [];
  if (isEmpty(state)) {
    errors.push(`${fieldName} is required.`);
  } else {
    if (state.length < 2) errors.push(`Please enter a valid ${fieldName.toLowerCase()}.`);
    if (state.length > 50) errors.push(`${fieldName} must be less than 50 characters.`);
    // Allow letters, spaces, hyphens for state/province names
    if (!/^[a-zA-ZÀ-ÿ\s\-'\.]+$/.test(state)) errors.push(`${fieldName} contains invalid characters.`);
  }
  return errors;
}

function validateZipCode(zipCode, fieldName, country = null) {
  const errors = [];
  if (isEmpty(zipCode)) {
    errors.push(`${fieldName} is required.`);
  } else {
    // Country-specific zip/postal code validation
    const zipPatterns = {
      'US': /^\d{5}(-\d{4})?$/, // US ZIP codes: 12345 or 12345-6789
      'CA': /^[A-Za-z]\d[A-Za-z][\s\-]?\d[A-Za-z]\d$/, // Canadian postal codes: A1A 1A1
      'UK': /^[A-Za-z]{1,2}\d[A-Za-z\d]?\s?\d[A-Za-z]{2}$/, // UK postcodes
      'DE': /^\d{5}$/, // German postal codes: 12345
      'FR': /^\d{5}$/, // French postal codes: 12345
      'IT': /^\d{5}$/, // Italian postal codes: 12345
      'ES': /^\d{5}$/, // Spanish postal codes: 12345
      'AU': /^\d{4}$/, // Australian postcodes: 1234
      'NL': /^\d{4}\s?[A-Za-z]{2}$/, // Dutch postal codes: 1234 AB
      'BR': /^\d{5}-?\d{3}$/, // Brazilian CEP: 12345-678
      'IN': /^\d{6}$/, // Indian PIN codes: 123456
      'JP': /^\d{3}-?\d{4}$/, // Japanese postal codes: 123-4567
    };

    if (country && zipPatterns[country]) {
      if (!zipPatterns[country].test(zipCode)) {
        errors.push(`Please enter a valid ${fieldName.toLowerCase()} for ${country}.`);
      }
    } else {
      // Generic validation for unknown countries
      if (zipCode.length < 3 || zipCode.length > 12) {
        errors.push(`${fieldName} must be between 3 and 12 characters.`);
      }
      if (!/^[a-zA-Z0-9\s\-]+$/.test(zipCode)) {
        errors.push(`${fieldName} contains invalid characters.`);
      }
    }
  }
  return errors;
}

function validateCountry(country, fieldName) {
  const errors = [];
  if (isEmpty(country)) {
    errors.push(`${fieldName} is required.`);
  } else {
    // List of valid country codes or names (you can expand this)
    const validCountries = [
      'US', 'CA', 'UK', 'GB', 'DE', 'FR', 'IT', 'ES', 'AU', 'NL', 'BR', 'IN', 'JP',
      'United States', 'Canada', 'United Kingdom', 'Germany', 'France', 'Italy', 
      'Spain', 'Australia', 'Netherlands', 'Brazil', 'India', 'Japan'
    ];
    
    if (country.length < 2) errors.push(`Please select a valid ${fieldName.toLowerCase()}.`);
    // Note: In a real application, you'd validate against a comprehensive country list
  }
  return errors;
}

function validateAddressSet(addressData, prefix) {
  const errors = [];
  
  // Validate names
  errors.push(...validateName(addressData.first_name, `${prefix} first name`));
  errors.push(...validateName(addressData.last_name, `${prefix} last name`));
  
  // Validate address components
  errors.push(...validateStreetAddress(addressData.street_address, `${prefix} street address`));
  errors.push(...validateCity(addressData.city, `${prefix} city`));
  errors.push(...validateState(addressData.state, `${prefix} state/province`));
  errors.push(...validateZipCode(addressData.zip_code, `${prefix} zip/postal code`, addressData.country));
  errors.push(...validateCountry(addressData.country, `${prefix} country`));
  
  // Validate contact information (only for shipping)
  if (prefix === 'Shipping') {
    if (isEmpty(addressData.phone)) {
      errors.push("Phone number is required.");
    } else if (!validatePhone(addressData.phone)) {
      errors.push("Please enter a valid phone number with country code (e.g., +1234567890).");
    }
    
    if (isEmpty(addressData.email)) {
      errors.push("Email address is required.");
    } else if (!validateEmail(addressData.email)) {
      errors.push("Please enter a valid email address.");
    }
  }
  
  return errors;
}

function validateCardNumber(card) {
  // Use Luhn algorithm for credit card validation
  if (!/^\d{13,19}$/.test(card)) return false;
  
  // Luhn algorithm implementation
  let sum = 0;
  let shouldDouble = false;
  
  // Loop through values starting from the rightmost digit
  for (let i = card.length - 1; i >= 0; i--) {
    let digit = parseInt(card.charAt(i));
    
    if (shouldDouble) {
      digit *= 2;
      if (digit > 9) digit -= 9;
    }
    
    sum += digit;
    shouldDouble = !shouldDouble;
  }
  
  return (sum % 10) === 0;
}

function validateExpiration(exp) {
  // Validate MM/YY format and check if the date is not expired
  const pattern = /^(0[1-9]|1[0-2])\/\d{2}$/;
  if (!pattern.test(exp)) return false;
  
  // Get current date and expiry date
  const [month, year] = exp.split('/').map(num => parseInt(num, 10));
  const currentDate = new Date();
  const currentYear = currentDate.getFullYear() % 100; // Get last 2 digits
  const currentMonth = currentDate.getMonth() + 1; // JS months are 0-indexed
  
  // Check if expiry date is in the future
  if (year < currentYear || (year === currentYear && month < currentMonth)) {
    return false;
  }
  
  return true;
}

function validateCVV(cvv) {
  // CVV is 3 digits for most cards, 4 for American Express
  return /^\d{3,4}$/.test(cvv);
}

function validateCheckoutData(data) {
  const errors = [];

  // Validate shipping address
  errors.push(...validateAddressSet(data.shipping, 'Shipping'));

  // Validate billing address (if different from shipping)
  if (!data.billingSameAsShipping) {
    errors.push(...validateAddressSet(data.billing, 'Billing'));
  }

  // Shipping method validation
  if (isEmpty(data.shippingMethod)) {
    errors.push("Please select a shipping method.");
  }

  // Payment method validation
  if (isEmpty(data.paymentMethod)) {
    errors.push("Please select a payment method.");
  }

  // Payment fields validation (if method is card)
  if (data.paymentMethod === "card") {
    const p = data.payment;
    
    if (isEmpty(p.card_number)) {
      errors.push("Card number is required.");
    } else if (!validateCardNumber(p.card_number)) {
      errors.push("Please enter a valid card number.");
    }
    
    if (isEmpty(p.expiry)) {
      errors.push("Expiration date is required.");
    } else if (!validateExpiration(p.expiry)) {
      errors.push("Please enter a valid expiration date (MM/YY) that hasn't expired.");
    }
    
    if (isEmpty(p.cvv)) {
      errors.push("CVV is required.");
    } else if (!validateCVV(p.cvv)) {
      errors.push("Please enter a valid CVV (3-4 digits).");
    }
    
    if (isEmpty(p.name_on_card)) {
      errors.push("Cardholder name is required.");
    } else {
      // Validate cardholder name
      if (p.name_on_card.length < 2) errors.push("Cardholder name must be at least 2 characters.");
      if (p.name_on_card.length > 50) errors.push("Cardholder name must be less than 50 characters.");
      if (!/^[a-zA-ZÀ-ÿ\s\-'\.]+$/.test(p.name_on_card)) errors.push("Cardholder name contains invalid characters.");
    }
  }

  // PayPal validation (if applicable)
  if (data.paymentMethod === "paypal") {
    // PayPal validation would go here if needed
    // For now, just ensure the method is selected
  }

  // Additional validation for order consistency
  if (data.items && data.items.length === 0) {
    errors.push("Your cart is empty. Please add items before checkout.");
  }

  return errors;
}

// Real-time validation helpers
function validateFieldRealTime(fieldElement, validationFunction, ...args) {
  const value = fieldElement.value.trim();
  const fieldName = fieldElement.getAttribute('data-field-name') || fieldElement.name || 'Field';
  
  let errors = [];
  if (validationFunction === validateName) {
    errors = validateName(value, fieldName);
  } else if (validationFunction === validateStreetAddress) {
    errors = validateStreetAddress(value, fieldName);
  } else if (validationFunction === validateCity) {
    errors = validateCity(value, fieldName);
  } else if (validationFunction === validateState) {
    errors = validateState(value, fieldName);
  } else if (validationFunction === validateZipCode) {
    errors = validateZipCode(value, fieldName, ...args);
  } else if (validationFunction === validateCountry) {
    errors = validateCountry(value, fieldName);
  } else if (validationFunction === validateEmail) {
    errors = validateEmail(value) ? [] : ['Please enter a valid email address.'];
  } else if (validationFunction === validatePhone) {
    errors = validatePhone(value) ? [] : ['Please enter a valid phone number.'];
  }
  
  // Remove existing error styling and messages
  fieldElement.classList.remove('error', 'valid');
  const existingError = fieldElement.parentNode.querySelector('.error-message');
  if (existingError) {
    existingError.remove();
  }
  
  if (errors.length > 0) {
    fieldElement.classList.add('error');
    
    // Add error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = errors[0]; // Show first error
    fieldElement.parentNode.insertBefore(errorDiv, fieldElement.nextSibling);
    
    return false;
  } else if (value) {
    fieldElement.classList.add('valid');
    return true;
  }
  
  return true; // Empty fields are considered valid for real-time validation
}

function setupRealTimeValidation() {
  // Setup real-time validation for shipping address
  const shippingFields = {
    'input[name="shipping_first_name"]': (el) => validateFieldRealTime(el, validateName),
    'input[name="shipping_last_name"]': (el) => validateFieldRealTime(el, validateName),
    'input[name="shipping_street_address"]': (el) => validateFieldRealTime(el, validateStreetAddress),
    'input[name="shipping_city"]': (el) => validateFieldRealTime(el, validateCity),
    'input[name="shipping_state"]': (el) => validateFieldRealTime(el, validateState),
    'input[name="shipping_zip_code"]': (el) => {
      const countryField = document.querySelector('select[name="shipping_country"]');
      const country = countryField ? countryField.value : null;
      return validateFieldRealTime(el, validateZipCode, country);
    },
    'select[name="shipping_country"]': (el) => validateFieldRealTime(el, validateCountry),
    'input[name="shipping_phone"]': (el) => validateFieldRealTime(el, validatePhone),
    'input[name="shipping_email"]': (el) => validateFieldRealTime(el, validateEmail),
  };
  
  // Setup real-time validation for billing address
  const billingFields = {
    'input[name="billing_first_name"]': (el) => validateFieldRealTime(el, validateName),
    'input[name="billing_last_name"]': (el) => validateFieldRealTime(el, validateName),
    'input[name="billing_street_address"]': (el) => validateFieldRealTime(el, validateStreetAddress),
    'input[name="billing_city"]': (el) => validateFieldRealTime(el, validateCity),
    'input[name="billing_state"]': (el) => validateFieldRealTime(el, validateState),
    'input[name="billing_zip_code"]': (el) => {
      const countryField = document.querySelector('select[name="billing_country"]');
      const country = countryField ? countryField.value : null;
      return validateFieldRealTime(el, validateZipCode, country);
    },
    'select[name="billing_country"]': (el) => validateFieldRealTime(el, validateCountry),
  };
  
  // Apply event listeners for shipping fields
  Object.entries(shippingFields).forEach(([selector, validator]) => {
    const field = document.querySelector(selector);
    if (field) {
      field.setAttribute('data-field-name', selector.replace(/.*\[name="([^"]+)"\].*/, '$1').replace(/_/g, ' '));
      field.addEventListener('blur', () => validator(field));
      field.addEventListener('input', debounce(() => validator(field), 500));
    }
  });
  
  // Apply event listeners for billing fields
  Object.entries(billingFields).forEach(([selector, validator]) => {
    const field = document.querySelector(selector);
    if (field) {
      field.setAttribute('data-field-name', selector.replace(/.*\[name="([^"]+)"\].*/, '$1').replace(/_/g, ' '));
      field.addEventListener('blur', () => validator(field));
      field.addEventListener('input', debounce(() => validator(field), 500));
    }
  });
}

// Debounce function for real-time validation
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// Enhanced validation with summary display
function showValidationSummary(errors, containerId = 'validation-summary') {
  let summaryContainer = document.getElementById(containerId);
  
  if (!summaryContainer) {
    // Create validation summary container if it doesn't exist
    summaryContainer = document.createElement('div');
    summaryContainer.id = containerId;
    summaryContainer.className = 'validation-summary';
    
    // Insert at the top of the form
    const form = document.querySelector('form');
    if (form) {
      form.insertBefore(summaryContainer, form.firstChild);
    }
  }
  
  if (errors.length > 0) {
    summaryContainer.innerHTML = `
      <h4>Please correct the following errors:</h4>
      <ul>
        ${errors.map(error => `<li>${error}</li>`).join('')}
      </ul>
    `;
    summaryContainer.classList.add('show');
    
    // Scroll to summary
    summaryContainer.scrollIntoView({ behavior: 'smooth', block: 'center' });
  } else {
    summaryContainer.classList.remove('show');
  }
}

function hideValidationSummary(containerId = 'validation-summary') {
  const summaryContainer = document.getElementById(containerId);
  if (summaryContainer) {
    summaryContainer.classList.remove('show');
  }
}

// Enhanced validateCheckoutData with better error categorization
function validateCheckoutDataWithSummary(data) {
  const errors = validateCheckoutData(data);
  
  if (errors.length > 0) {
    showValidationSummary(errors);
    return { isValid: false, errors };
  } else {
    hideValidationSummary();
    return { isValid: true, errors: [] };
  }
}

// Progressive validation - validate each section as user progresses
function validateSection(sectionName, data) {
  const errors = [];
  
  switch (sectionName) {
    case 'shipping':
      errors.push(...validateAddressSet(data.shipping, 'Shipping'));
      break;
      
    case 'billing':
      if (!data.billingSameAsShipping) {
        errors.push(...validateAddressSet(data.billing, 'Billing'));
      }
      break;
      
    case 'shipping-method':
      if (isEmpty(data.shippingMethod)) {
        errors.push("Please select a shipping method.");
      }
      break;
      
    case 'payment':
      if (isEmpty(data.paymentMethod)) {
        errors.push("Please select a payment method.");
      }
      
      if (data.paymentMethod === "card") {
        const p = data.payment;
        
        if (isEmpty(p.card_number)) {
          errors.push("Card number is required.");
        } else if (!validateCardNumber(p.card_number)) {
          errors.push("Please enter a valid card number.");
        }
        
        if (isEmpty(p.expiry)) {
          errors.push("Expiration date is required.");
        } else if (!validateExpiration(p.expiry)) {
          errors.push("Please enter a valid expiration date (MM/YY) that hasn't expired.");
        }
        
        if (isEmpty(p.cvv)) {
          errors.push("CVV is required.");
        } else if (!validateCVV(p.cvv)) {
          errors.push("Please enter a valid CVV (3-4 digits).");
        }
        
        if (isEmpty(p.name_on_card)) {
          errors.push("Cardholder name is required.");
        } else {
          if (p.name_on_card.length < 2) errors.push("Cardholder name must be at least 2 characters.");
          if (p.name_on_card.length > 50) errors.push("Cardholder name must be less than 50 characters.");
          if (!/^[a-zA-ZÀ-ÿ\s\-'\.]+$/.test(p.name_on_card)) errors.push("Cardholder name contains invalid characters.");
        }
      }
      break;
  }
  
  return errors;
}

// Helper function to enable/disable continue buttons based on validation
function updateContinueButton(sectionName, isValid) {
  const continueBtn = document.querySelector(`#${sectionName}-continue, .btn-continue[data-section="${sectionName}"]`);
  if (continueBtn) {
    continueBtn.disabled = !isValid;
    continueBtn.classList.toggle('disabled', !isValid);
  }
}

// Initialize real-time validation when DOM is loaded
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', setupRealTimeValidation);
} else {
  setupRealTimeValidation();
}
