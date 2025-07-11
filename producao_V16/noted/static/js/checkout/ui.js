
document.addEventListener("DOMContentLoaded", function () {
  // ============================
  // ELEMENTOS & VARIÁVEIS
  // ============================
  const phoneInput = document.getElementById("phone");
  const flagIcon = document.getElementById("flagIcon");

  const sameAddressCheckbox = document.getElementById("same_address");
  const billingFields = document.getElementById("billingAddressFields");

  const sections = document.querySelectorAll('.section-block');
  const continueButtons = document.querySelectorAll('.section-block .btn');
  const shippingRadios = document.querySelectorAll('input[name="shipping_method"]');
  const paymentSection = document.getElementById('paymentSection');

  const countryFlags = {
    "+351": "pt", "+34": "es", "+33": "fr", "+44": "gb",
    "+49": "de", "+39": "it", "+1": "us", "+55": "br"
  };

  // ============================
  // BANDEIRA DO TELEFONE
  // ============================
  if (phoneInput && flagIcon) {
    const updateFlagIcon = () => {
      const value = phoneInput.value.trim();
      let found = false;
      for (const prefix in countryFlags) {
        if (value.startsWith(prefix)) {
          const code = countryFlags[prefix];
          flagIcon.src = `https://flagcdn.com/32x24/${code}.png`;
          flagIcon.style.display = 'inline-block';
          found = true;
          break;
        }
      }
      if (!found) flagIcon.style.display = 'none';
    };
    phoneInput.addEventListener("input", updateFlagIcon);
    updateFlagIcon();
  }

  // ============================
  // CHECKBOX "MESMO ENDEREÇO"
  // ============================
  if (sameAddressCheckbox && billingFields) {
    const toggleBillingFields = () => {
      if (sameAddressCheckbox.checked) {
        billingFields.style.display = 'none';
        billingFields.querySelectorAll('input').forEach(input => {
          input.removeAttribute('required');
          input.value = '';
        });
      } else {
        billingFields.style.display = 'block';
        billingFields.querySelectorAll('input').forEach(input => {
          input.setAttribute('required', 'required');
        });
      }
    };
    sameAddressCheckbox.addEventListener('change', toggleBillingFields);
    toggleBillingFields();
  }

  // ============================
  // NAVEGAR ENTRE SECÇÕES
  // ============================
  if (sections.length > 0 && continueButtons.length > 0) {
    sections.forEach((section, index) => {
      const content = section.querySelectorAll('input, label, .form-group, .accordion-payment, .checkbox, .btn');
      content.forEach(el => {
        if (el.tagName !== 'H2') el.style.display = 'none';
      });
      if (index === 0) {
        section.querySelectorAll('input, label, .form-group, .accordion-payment, .checkbox, .btn').forEach(el => {
          el.style.display = '';
        });
      }
    });

    continueButtons.forEach((btn, index) => {
      btn.addEventListener('click', () => {
        const section = sections[index];
        const inputs = section.querySelectorAll('input[required]');
        let valid = true;

        inputs.forEach(input => {
          if (!input.checkValidity()) {
            input.reportValidity();
            valid = false;
          }
        });

        if (!valid) return;

        // Resumo
        inputs.forEach(input => {
        const formGroup = input.closest('.form-group');
        if (formGroup) {
          const label = formGroup.querySelector('label');
          const summary = document.createElement('div');
          summary.className = 'checkout-summary';
          summary.textContent = `${label ? label.textContent : input.name}: ${input.value}`;
          formGroup.appendChild(summary);

          if (label) label.classList.add('label-hide');
          input.classList.add('input-hide');
          setTimeout(() => {
            if (label) label.style.display = 'none';
            input.style.display = 'none';
          }, 300);
        }
      });


        btn.style.display = 'none';
        const header = section.querySelector('.section-header .edit-button');
        if (header) header.style.display = 'inline-block';

        const nextSection = sections[index + 1];
        if (nextSection) {
          const nextElements = nextSection.querySelectorAll('input, label, .form-group, .accordion-payment, .checkbox, .btn');
          nextElements.forEach(el => {
            el.style.display = '';
          });
        }
      });
    });

    // Editar secção
    sections.forEach(section => {
      const editBtn = section.querySelector('.edit-button');
      if (!editBtn) return;

      editBtn.addEventListener('click', () => {
        const summaries = section.querySelectorAll('.checkout-summary');
        summaries.forEach(s => s.remove());
        const labels = section.querySelectorAll('label');
        const inputs = section.querySelectorAll('input');
        const btn = section.querySelector('.btn');

        labels.forEach(label => {
          label.style.display = '';
          label.classList.remove('label-hide');
        });
        inputs.forEach(input => {
          input.style.display = '';
          input.classList.remove('input-hide');
        });
        btn.style.display = '';
        editBtn.style.display = 'none';
      });
    });
  }

  // ============================
  // MOSTRAR SECÇÃO PAGAMENTO
  // ============================
  if (shippingRadios.length > 0 && paymentSection) {
    shippingRadios.forEach(radio => {
      radio.addEventListener('change', () => {
        const paymentElements = paymentSection.querySelectorAll('input, label, .form-group, .accordion-payment, .checkbox, .btn');
        paymentElements.forEach(el => {
          el.style.display = '';
        });
      });
    });
  }

});


console.log("Checkout UI script loaded");

function getSelectedValue(name) {
  const selected = document.querySelector(`input[name='${name}']:checked`);
  return selected ? selected.value : "";
}

function showStatus(message, success = true) {
  const statusEl = document.getElementById("order-status");
  if (statusEl) {
    statusEl.textContent = message;
    statusEl.className = `order-status-msg ${success ? 'success' : 'error'}`;
    statusEl.style.display = "block";
    statusEl.scrollIntoView({ behavior: "smooth" });
  }
}

function toggleSection(sectionId, show) {
  const section = document.getElementById(sectionId);
  if (section) {
    section.style.display = show ? "block" : "none";
  }
}

function fillSummary(sectionId, data) {
  const summary = document.getElementById(`${sectionId}-summary`);
  if (summary && data) {
    summary.innerHTML = Object.entries(data).map(([key, value]) =>
      `<p><strong>${key}:</strong> ${value}</p>`
    ).join("");
  }
}

function updateProgressSteps() {
  const steps = document.querySelectorAll(".checkout-step");
  steps.forEach(step => {
    const completed = step.querySelector(".step-complete");
    if (completed) {
      step.classList.add("completed");
    }
  });
}

function enableNextSection(currentId, nextId) {
  const currentSection = document.getElementById(currentId);
  const nextSection = document.getElementById(nextId);
  if (currentSection && nextSection) {
    currentSection.style.display = "none";
    nextSection.style.display = "block";
    nextSection.scrollIntoView({ behavior: "smooth" });
    updateProgressSteps();
  }
}

function handleStepTransitions() {
  document.querySelectorAll(".btn-continue").forEach(btn => {
    btn.addEventListener("click", () => {
      const currentStep = btn.closest(".checkout-section");
      const nextStep = currentStep?.nextElementSibling;
      if (currentStep && nextStep) {
        const data = collectOrderData();
        fillSummary(currentStep.id, data[currentStep.dataset.type]);
        toggleSection(currentStep.id, false);
        toggleSection(nextStep.id, true);
      }
    });
  });
}

document.addEventListener("DOMContentLoaded", handleStepTransitions);