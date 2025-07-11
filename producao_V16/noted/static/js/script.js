document.addEventListener("DOMContentLoaded", () => {  
  /*console.log("Script loaded");
  
  // Debug: List all available menu elements
  console.log("Available menu elements:");
  document.querySelectorAll("[id^='menu-'], #mainMenu").forEach(menu => {
    console.log("- " + menu.id, menu.classList.contains("hidden") ? "(hidden)" : "(visible)");
  });*/
  
  // Elementos principais do DOM
  const menuToggle = document.getElementById("menuToggle");
  const closeMenu = document.getElementById("closeMenu");
  const navSidebar = document.getElementById("navMenuSidebar");

  const cartToggle = document.getElementById("cartToggle");
  const closeCart = document.getElementById("closeCart");
  const cartSidebar = document.getElementById("cartSidebar");

  // Mobile buttons
  const mobileMenuToggle = document.getElementById("mobileMenuToggle");
  const mobileCartToggle = document.getElementById("mobileCartToggle");
  const mobileAccountToggle = document.getElementById("mobileAccountToggle");

  // Overlay element
  const overlay = document.getElementById("overlay");
  
  // Back button
  const backButton = document.getElementById("backButton");

  // Utility functions for menu/cart state
  function openMenu() {
    document.body.classList.add("menu-open");
    navSidebar.classList.add("show");
    overlay.classList.add("show");
    // Close cart if open
    document.body.classList.remove("cart-open");
    cartSidebar.classList.remove("show");
    
    // Add active state to menu buttons
    if (menuToggle) menuToggle.classList.add("active");
    if (mobileMenuToggle) mobileMenuToggle.classList.add("active");
    // Remove active state from cart buttons
    if (cartToggle) cartToggle.classList.remove("active");
    if (mobileCartToggle) mobileCartToggle.classList.remove("active");
    
    // Hide all menus and show only the main menu
    document.querySelectorAll(".nav-menu-links").forEach(ul => {
      ul.style.display = "none";
    });
    
    const mainMenu = document.getElementById("mainMenu");
    if (mainMenu) {
      mainMenu.style.display = "block";
    }
    
    // Ensure back button is hidden when opening main menu
    if (backButton) {
      backButton.style.display = "none";
    }
  }

  function closeMenuSidebar() {
    document.body.classList.remove("menu-open");
    navSidebar.classList.remove("show");
    overlay.classList.remove("show");
    
    // Remove active state from menu buttons
    if (menuToggle) menuToggle.classList.remove("active");
    if (mobileMenuToggle) mobileMenuToggle.classList.remove("active");
    
    // Hide back button when closing menu
    if (backButton) {
      backButton.style.display = "none";
    }
  }

  function openCart() {
    document.body.classList.add("cart-open");
    cartSidebar.classList.add("show");
    overlay.classList.add("show");
    // Close menu if open
    document.body.classList.remove("menu-open");
    navSidebar.classList.remove("show");
    
    // Add active state to cart buttons
    if (cartToggle) cartToggle.classList.add("active");
    if (mobileCartToggle) mobileCartToggle.classList.add("active");
    // Remove active state from menu buttons
    if (menuToggle) menuToggle.classList.remove("active");
    if (mobileMenuToggle) mobileMenuToggle.classList.remove("active");
    
    loadCart();
  }

  // Make openCart globally accessible
  window.openCart = openCart;

  function closeCartSidebar() {
    document.body.classList.remove("cart-open");
    cartSidebar.classList.remove("show");
    overlay.classList.remove("show");
    
    // Remove active state from cart buttons
    if (cartToggle) cartToggle.classList.remove("active");
    if (mobileCartToggle) mobileCartToggle.classList.remove("active");
  }

  // Shows menu with simple, discrete fade-in animation
  function showMenu(id) {
    console.log("showMenu called with id:", id); // Debug log
    
    // Find current visible menu
    let currentMenu = null;
    document.querySelectorAll(".nav-menu-links").forEach(ul => {
      if (getComputedStyle(ul).display !== "none") {
        currentMenu = ul;
      }
    });
    
    const target = document.getElementById(id);
    if (!target) {
      console.log("Menu target not found:", id);
      return;
    }
    
    // If it's the same menu, do nothing
    if (currentMenu === target) {
      return;
    }
    
    // Hide all menus first
    document.querySelectorAll(".nav-menu-links").forEach(ul => {
      ul.style.display = "none";
      ul.style.opacity = "";
      ul.style.transform = "";
      ul.style.transition = "";
    });
    
    // Show target menu with discrete fade-in
    target.style.display = "block";
    target.style.opacity = "0";
    target.style.transition = "opacity 0.2s ease";
    
    // Animate to visible state
    requestAnimationFrame(() => {
      target.style.opacity = "1";
    });
    
    // Clean up after animation
    setTimeout(() => {
      target.style.transition = "";
    }, 200);
    
    // Show back button only if we're in a submenu
    if (id !== "mainMenu" && backButton) {
      backButton.style.display = "inline-block";
    } else if (backButton) {
      backButton.style.display = "none";
    }
    
    console.log("Menu shown:", id); // Debug log
  }



  // Desktop menu toggle - toggles open/close
  if (menuToggle) {
    menuToggle.addEventListener("click", () => {
      // If menu is already open, close it
      if (document.body.classList.contains("menu-open")) {
        closeMenuSidebar();
      } else {
        // If cart is open, close it first
        if (document.body.classList.contains("cart-open")) {
          closeCartSidebar();
          // Small delay before opening menu for better UX
          setTimeout(() => {
            openMenu();
          }, 150);
        } else {
          openMenu();
        }
      }
    });
  }

  // Close menu button
  if (closeMenu) {
    closeMenu.addEventListener("click", closeMenuSidebar);
  }
  
  // Back button
  if (backButton) {
    backButton.addEventListener("click", () => {
      // Find the current visible menu
      let currentMenu = null;
      document.querySelectorAll(".nav-menu-links").forEach(menu => {
        if (getComputedStyle(menu).display !== "none") {
          currentMenu = menu;
        }
      });

      if (currentMenu) {
        const menuId = currentMenu.id;
        
        // If we're in a category menu, go back to products menu
        if (menuId.startsWith("menu-category-")) {
          showMenu("menu-products");
        } else {
          // Otherwise go back to main menu
          showMenu("mainMenu");
        }
      }
    });
  }

  // Enhanced swipe functionality for menu navigation
  let touchStartX = 0;
  let touchEndX = 0;
  let touchStartY = 0;
  let touchEndY = 0;
  const minSwipeDistance = 50; // Minimum distance for a swipe to be recognized
  const maxVerticalDistance = 100; // Maximum vertical movement to still be considered horizontal swipe

  function handleSwipe() {
    const deltaX = touchEndX - touchStartX;
    const deltaY = Math.abs(touchEndY - touchStartY);
    
    // Check if it's a horizontal swipe (right direction) with minimal vertical movement
    if (deltaX > minSwipeDistance && deltaY < maxVerticalDistance) {
      // Only trigger back navigation if back button is visible and menu is open
      if (backButton && backButton.style.display !== "none" && navSidebar && navSidebar.classList.contains("show")) {
        // Add brief visual feedback that matches the sliding direction
        const currentMenu = document.querySelector(".nav-menu-links[style*='display: block'], .nav-menu-links:not([style*='display: none'])");
        if (currentMenu) {
          // Use a more subtle feedback animation
          currentMenu.style.transition = 'transform 0.15s cubic-bezier(0.4, 0, 0.2, 1)';
          currentMenu.style.transform = 'translateX(15px)';
          setTimeout(() => {
            currentMenu.style.transform = 'translateX(15px)';
            setTimeout(() => {
              currentMenu.style.transition = '';
            }, 0);
          }, 75);
        }
        
        // Add a small delay before triggering navigation for better UX
        setTimeout(() => {
          // Trigger the same logic as the back button click
          let currentMenuForLogic = null;
          document.querySelectorAll(".nav-menu-links").forEach(menu => {
            if (getComputedStyle(menu).display !== "none") {
              currentMenuForLogic = menu;
            }
          });

          if (currentMenuForLogic) {
            const menuId = currentMenuForLogic.id;
            
            // If we're in a category menu, go back to products menu
            if (menuId.startsWith("menu-category-")) {
              showMenu("menu-products");
            } else {
              // Otherwise go back to main menu
              showMenu("mainMenu");
            }
          }
        }, 150);
      }
    }
  }

  // Add touch event listeners to the menu sidebar
  if (navSidebar) {
    navSidebar.addEventListener("touchstart", (e) => {
      touchStartX = e.changedTouches[0].screenX;
      touchStartY = e.changedTouches[0].screenY;
    }, { passive: true });

    navSidebar.addEventListener("touchmove", (e) => {
      // Prevent default scroll behavior during swipe on menu
      if (Math.abs(e.changedTouches[0].screenX - touchStartX) > 10) {
        e.preventDefault();
      }
    }, { passive: false });

    navSidebar.addEventListener("touchend", (e) => {
      touchEndX = e.changedTouches[0].screenX;
      touchEndY = e.changedTouches[0].screenY;
      handleSwipe();
    }, { passive: true });
  }

  // Desktop cart toggle - toggles open/close
  if (cartToggle) {
    cartToggle.addEventListener("click", () => {
      // If cart is already open, close it
      if (document.body.classList.contains("cart-open")) {
        closeCartSidebar();
      } else {
        // If menu is open, close it first
        if (document.body.classList.contains("menu-open")) {
          closeMenuSidebar();
          // Small delay before opening cart for better UX
          setTimeout(() => {
            openCart();
          }, 150);
        } else {
          openCart();
        }
      }
    });
  }

  // Close cart button
  if (closeCart) {
    closeCart.addEventListener("click", closeCartSidebar);
  }

  // Mobile Menu Toggle - toggles open/close
  if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener("click", () => {
      // If menu is already open, close it
      if (document.body.classList.contains("menu-open")) {
        closeMenuSidebar();
      } else {
        // If cart is open, close it first
        if (document.body.classList.contains("cart-open")) {
          closeCartSidebar();
          // Small delay before opening menu for better UX
          setTimeout(() => {
            openMenu();
          }, 150);
        } else {
          openMenu();
        }
      }
    });
  }

  // Mobile Cart Toggle - toggles open/close
  if (mobileCartToggle) {
    mobileCartToggle.addEventListener("click", () => {
      // If cart is already open, close it
      if (document.body.classList.contains("cart-open")) {
        closeCartSidebar();
      } else {
        // If menu is open, close it first
        if (document.body.classList.contains("menu-open")) {
          closeMenuSidebar();
          // Small delay before opening cart for better UX
          setTimeout(() => {
            openCart();
          }, 150);
        } else {
          openCart();
        }
      }
    });
  }

  // Mobile Account Toggle
  if (mobileAccountToggle) {
    mobileAccountToggle.addEventListener("click", () => {
      fetch("/is_logged_in")
        .then(res => res.json())
        .then(data => {
          if (data.logged_in) {
            window.location.href = "/account";
          } else {
            window.location.href = "/login";
          }
        });
    });
  }

  // Overlay click to close menu/cart
  if (overlay) {
    overlay.addEventListener("click", () => {
      // Always close the menu sidebar
      closeMenuSidebar();
      
      // Only close the cart if in mobile view (screen width less than 768px)
      if (window.innerWidth < 768) {
        closeCartSidebar();
      }
    });
  }

  // Menu navigation with data-target - using event delegation for dynamic content
  document.addEventListener("click", (e) => {
    if (e.target.closest(".menu-link")) {
      e.preventDefault();
      const link = e.target.closest(".menu-link");
      const target = link.getAttribute("data-target");
      if (target) {
        console.log("Menu navigation clicked:", target); // Debug log
        console.log("Looking for element with id:", "menu-" + target); // Debug log
        
        // Debug: Log all menu-* elements with their display property
        console.log("Available menu elements with display property:");
        document.querySelectorAll("[id^='menu-'], #mainMenu").forEach(menu => {
          console.log("- " + menu.id + ": display = " + getComputedStyle(menu).display);
        });
        
        showMenu("menu-" + target);
        
        // Check display after showMenu
        console.log("Menu display after showMenu:");
        const targetMenu = document.getElementById("menu-" + target);
        if (targetMenu) {
          console.log("- " + targetMenu.id + ": display = " + getComputedStyle(targetMenu).display);
        }
      }
    }
  });

  // Auto-open cart on checkout page (desktop only)
  if (window.location.pathname === "/checkout") {
    if (window.innerWidth >= 768) {
      openCart();
      // Hide checkout button if necessary
      setTimeout(() => {
        const checkoutBtn = document.querySelector(".checkout-btn");
        if (checkoutBtn) checkoutBtn.style.display = "none";
      }, 200);
    }
  }

  // Initialize shipping cost
  const selectedShipping = document.querySelector('input[name="shipping_method"]:checked');
  const cost = selectedShipping ? parseFloat(selectedShipping.getAttribute("data-cost")) : 0;
  sessionStorage.setItem("shipping_cost", cost);

  // Optional: inform server about shipping cost
  if (selectedShipping) {
    fetch("/set_shipping", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ cost })
    });
  }

  // Cart content event delegation for remove buttons
  const cartContent = document.querySelector(".cart-content");
  if (cartContent) {
    cartContent.addEventListener("click", (e) => {
      const removeBtn = e.target.closest(".remove-item");
      if (removeBtn) {
        const wrapper = removeBtn.closest(".cart-item-wrapper");
        const productId = wrapper?.dataset.productId;

        if (productId) {
          fetch("/remove_from_cart", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ product_id: parseInt(productId) }),
          })
          .then(res => res.json())
          .then(result => {
            if (result.success) {
              loadCart(); // recarrega o carrinho
            }
          });
        }
      }
    });
  }
});

// Listener para shipping_method → atualiza sempre que muda
document.querySelectorAll('input[name="shipping_method"]').forEach(radio => {
  radio.addEventListener("change", () => {
    const selected = document.querySelector('input[name="shipping_method"]:checked');
    const shippingCost = selected ? parseFloat(selected.dataset.cost) : 0;
    console.log("Shipping selected:", selected.value, "→", shippingCost, "€");

    // Remove sessionStorage since we'll check directly from DOM
    // sessionStorage.setItem("shipping_cost", shippingCost);

    // Chamar para atualizar o total
    loadCart();
  });
});

function loadCart() {
  fetch("/cart_data")
  .then(response => response.json())
  .then(data => {
    const cartContent = document.querySelector(".cart-content");
    cartContent.innerHTML = "";

    if (!data.success || data.items.length === 0) {
      cartContent.innerHTML = "<p class='empty-message'>sadly, your cart is empty </p>";
      return;
    }

    // Renderizar os itens do carrinho
    data.items.forEach(item => {
      const itemElement = document.createElement("div");
      itemElement.className = "cart-item";

      itemElement.innerHTML = `
        <div class="cart-item-wrapper" data-product-id="${item.id}">
          <a href="/product/${item.id}">
            <img src="/static/img/products/${item.image}" alt="${item.name}" class="cart-thumb" />
          </a>
          <div class="cart-info">
            <p class="cart-title">
              <a href="/product/${item.id}" class="cart-link">${item.name}</a>
            </p>
            <p class="cart-variant">${item.color || ''}</p>
            <p class="cart-price">${(item.price * item.quantity).toFixed(2)}€</p>
          </div>
          <div class="cart-controls">
            <div class="qty-box">
              <button class="decrease-qty qty-btn" data-product-id="${item.id}">−</button>
              <span class="cart-qty">${item.quantity}</span>
              <button class="increase-qty qty-btn" data-product-id="${item.id}">+</button>
            </div>
            <button class="remove-item">
              <img src="/static/img/icons/close.png" alt="remove" />
            </button>
          </div>
        </div>
      `;
      cartContent.appendChild(itemElement);
    });

    // TOTAL e desconto
    const subtotal = data.items.reduce((sum, item) => {
      const price = parseFloat(item.price) || 0;
      const quantity = parseInt(item.quantity) || 0;
      return sum + (price * quantity);
    }, 0);

    let discountValue = 0;
    let totalAfterDiscount = subtotal;
    
    let isPercentage = false;
    let discountAmount = 0;

    if (data.discount) {
      discountAmount = data.discount.amount;
      isPercentage = data.discount.is_percentage;

      if (isPercentage) {
        discountValue = subtotal * (discountAmount / 100);
      } else {
        discountValue = discountAmount;
      }

      totalAfterDiscount = subtotal - discountValue;
    }

    // Check if we're on checkout page and if shipping is selected
    const isCheckoutPage = window.location.pathname === "/checkout";
    const selectedShipping = document.querySelector('input[name="shipping_method"]:checked');
    const shippingCost = selectedShipping ? parseFloat(selectedShipping.getAttribute("data-cost")) : 0;
    
    // Only include shipping cost if we're on checkout and shipping is selected
    const shouldShowShipping = isCheckoutPage && selectedShipping;
    const totalWithShipping = shouldShowShipping ? totalAfterDiscount + shippingCost : totalAfterDiscount;

    // Secção de código promocional + total
    let cartHTML = `
      <div class="discount-section">
        <input type="text" id="discount-code-input" placeholder="discount code">
        <button id="apply-discount-btn">apply</button>
        <p id="discount-message" class="discount-msg"></p>
      </div>`;
    
    // Only show discount line if a discount is applied
    if (data.discount) {
      cartHTML += `
        <p class="discount-line">
          <span class="discount-text">discount: -${discountValue.toFixed(2)}€</span>
          <span class="discount-details">(${isPercentage ? discountAmount + '%' : discountAmount.toFixed(2) + '€'})</span>
          <button class="remove-discount-btn" title="Remove discount">
            <img src="/static/img/icons/close.png" alt="remove discount" />
          </button>
        </p>`;
    }

    cartHTML += `
      <div class="cart-total">
        <p class="subtotal-line">subtotal: ${subtotal.toFixed(2)}€</p>`;
    
    // Only show shipping line if on checkout page and shipping is selected
    if (shouldShowShipping) {
      cartHTML += `<p class="shipping-line">shipping: ${shippingCost.toFixed(2)}€</p>`;
    }
    
    // Always display total, but only after all other values are shown
    cartHTML += `
        <p class="total-line"><strong>TOTAL: ${totalWithShipping.toFixed(2)}€</strong></p>
        <a href="/checkout" class="checkout-btn">checkout</a>
      </div>
    `;
    
    cartContent.innerHTML += cartHTML;

    // Botão de checkout → verificar login
    const checkoutBtn = document.querySelector(".checkout-btn");
    if (checkoutBtn) {
      checkoutBtn.addEventListener("click", (e) => {
        e.preventDefault();

        fetch("/is_logged_in")
          .then(res => res.json())
          .then(data => {
            if (data.logged_in) {
              window.location.href = "/checkout";
            } else {
              fetch("/set_next", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ next: "checkout" })
              }).then(() => {
                window.location.href = "/login";
              });
            }
          });
      });
    }

    // Aplicar desconto
    document.getElementById("apply-discount-btn").addEventListener("click", () => {
      const code = document.getElementById("discount-code-input").value.trim();

      fetch("/apply_discount", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code })
      })
      .then(res => res.json())
      .then(resp => {
        const msg = document.getElementById("discount-message");
        if (resp.success) {
          let displayAmount = resp.amount;
          if (resp.is_percentage) {
            displayAmount = `${displayAmount}%`;
          } else {
            displayAmount = `-${parseFloat(displayAmount || 0).toFixed(2)}€`;
          }
          //msg.textContent = `Discount applied: ${displayAmount}`;
          msg.className = "discount-msg success";

          setTimeout(() => {
            loadCart(); // garante que a sessão já tem os dados
          }, 100);
        }else {
          //msg.textContent = resp.error;
          msg.className = "discount-msg error";
        }
      });
    });

    // Remove discount functionality
    const removeDiscountBtn = document.querySelector(".remove-discount-btn");
    if (removeDiscountBtn) {
      removeDiscountBtn.addEventListener("click", () => {
        fetch("/remove_discount", {
          method: "POST",
          headers: { "Content-Type": "application/json" }
        })
        .then(res => res.json())
        .then(resp => {
          if (resp.success) {
            // Clear the discount input field
            const discountInput = document.getElementById("discount-code-input");
            if (discountInput) discountInput.value = "";
            
            // Clear any discount message
            const msg = document.getElementById("discount-message");
            if (msg) {
              msg.textContent = "";
              msg.className = "discount-msg";
            }
            
            // Reload cart to reflect changes
            setTimeout(() => {
              loadCart();
            }, 100);
          }
        })
        .catch(error => {
          console.error('Error removing discount:', error);
        });
      });
    }

    // If on checkout page, ensure the checkout button in the cart remains hidden
    if (window.location.pathname === "/checkout") {
      const btnToHide = cartContent.querySelector(".checkout-btn");
      if (btnToHide) {
        btnToHide.style.display = "none";
      }
    }

  });
}

// Lógica para atualizar a quantidade ao clicar nos botões "+" e "-"
document.querySelector(".cart-content").addEventListener("click", (e) => {
  const increase = e.target.closest(".increase-qty");
  const decrease = e.target.closest(".decrease-qty");

  if (increase || decrease) {
    const productId = (increase || decrease).dataset.productId;
    const delta = increase ? 1 : -1;

    fetch("/update_cart_quantity", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ product_id: parseInt(productId), delta: delta }),
    })
    .then(res => res.json())
    .then(result => {
      if (result.success) loadCart();
    });
  }
});

document.querySelectorAll(".add-to-cart").forEach(button => {
  button.addEventListener("click", () => {
    const productId = button.dataset.productId;

    fetch("/add_to_cart", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        product_id: parseInt(productId),
        quantity: 1,
      }),
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        loadCart(); // load content
        
        // Use the openCart function to ensure overlay is shown
        document.body.classList.add("cart-open");
        const cartSidebar = document.getElementById("cartSidebar");
        const overlay = document.getElementById("overlay");
        cartSidebar.classList.add("show");
        if (overlay) overlay.classList.add("show");

        // Close menu if it was open
        document.body.classList.remove("menu-open");
        const navSidebar = document.getElementById("navMenuSidebar");
        navSidebar.classList.remove("show");
      }
    })
    .catch(error => {
      console.error("Error:", error);
    });
  });
});

// --- PRODUCT DETAIL PAGE ADD TO CART BUTTON HANDLING ---
document.addEventListener('DOMContentLoaded', function() {
  // Wait a short time to ensure all scripts are loaded
  setTimeout(function() {
    // Check if productAddToCart is available
    if (typeof productAddToCart !== 'function') {
      console.error('error: productAddToCart function not found!');
      return;
    }
    // Set up main product add-to-cart button
    const addToCartBtn = document.querySelector('.add-to-cart-btn');
    if (addToCartBtn) {
      addToCartBtn.addEventListener('click', function() {
        const productId = this.dataset.productId;
        if (!productId) {
          console.error('Product ID missing from button');
          return;
        }
        const btn = this;
        const originalText = btn.textContent;
        btn.textContent = 'adding...';
        btn.disabled = true;
        productAddToCart(productId)
          .then(success => {
            if (success) {
              btn.textContent = 'added!';
              btn.style.backgroundColor = '#f8f9fa';
              btn.style.color = 'var(--color-black)';
              btn.disabled = false;
              if (typeof openCart === 'function') openCart(); // Open cart immediately after add
              setTimeout(() => {
                btn.textContent = originalText || 'add to cart';
                btn.style.backgroundColor = '#f8f9fa';
                btn.style.color = '#000';
              }, 1500);
            } else {
              showError();
            }
          })
          .catch(() => {
            showError();
          });
        function showError() {
          btn.textContent = 'error!';
          btn.style.backgroundColor = '#dc2626';
          btn.style.color = 'var(--color-white)';
          btn.disabled = false;
          setTimeout(() => {
            btn.textContent = originalText || 'add to cart';
            btn.style.backgroundColor = 'var(--color-black)';
            btn.style.color = 'var(--color-white)';
          }, 2000);
        }
      });
    }
    // Set up accessory add-to-cart buttons
    document.querySelectorAll('.add-accessory-btn').forEach(btn => {
      btn.addEventListener('click', function() {
        const accessoryId = this.dataset.accessoryId;
        if (!accessoryId) {
          console.error('Accessory ID missing from button');
          return;
        }
        const originalText = btn.textContent;
        btn.textContent = 'adding...';
        btn.disabled = true;
        productAddToCart(accessoryId)
          .then(success => {
            if (success) {
              btn.textContent = 'added!';
              btn.style.backgroundColor = 'var(--color-primary)';
              btn.style.color = 'var(--color-black)';
              btn.disabled = false;
              if (typeof openCart === 'function') openCart(); // Open cart immediately after add
              setTimeout(() => {
                btn.textContent = originalText || 'add to cart';
                btn.style.backgroundColor = 'var(--color-black)';
                btn.style.color = 'var(--color-white)';
              }, 1200);
            } else {
              showError();
            }
          })
          .catch(() => {
            showError();
          });
        function showError() {
          btn.textContent = 'error!';
          btn.style.backgroundColor = '#dc2626';
          btn.style.color = 'var(--color-white)';
          btn.disabled = false;
          setTimeout(() => {
            btn.textContent = originalText || 'add to cart';
            btn.style.backgroundColor = 'var(--color-black)';
            btn.style.color = 'var(--color-white)';
          }, 2000);
        }
      });
    });
  }, 100); // 100ms delay to ensure all scripts are loaded
});

function productAddToCart(productId, quantity = 1) {
  if (!productId) return false;
  
  return fetch("/add_to_cart", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      product_id: parseInt(productId),
      quantity: quantity
    }),
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      loadCart();
      return true;
    } else {
      return false;
    }
  })
  .catch(error => {
    console.error('Error adding product to cart:', error);
    return false;
  });
}

// Alternative approach - use the same calculation as in the cart sidebar
const cartTotalElement = document.querySelector(".cart-total strong");
if (cartTotalElement) {
  // Extract the total from the cart display (e.g., "TOTAL: 0.00€")
  const displayedTotal = parseFloat(cartTotalElement.textContent.match(/[\d.]+/)[0] || 0);
  data.total_confirmed = displayedTotal;
  
  console.log("Using displayed total:", displayedTotal);
  
  // Then do the balance check using this displayed total
}

function validateEmail(email) {
  const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return pattern.test(email);
}

// Registration form validation
const registerForm = document.getElementById("registerForm");
if (registerForm) {
  registerForm.addEventListener("submit", function(e) {
    const emailInput = document.getElementById("registerEmail");
    if (emailInput && !validateEmail(emailInput.value.trim())) {
      e.preventDefault();
      alert("please enter a valid email address.");
      emailInput.focus();
    }
  });
}

// Handle window resize events to adjust mobile/desktop behavior
window.addEventListener('resize', () => {
  // If switching from mobile to desktop while cart is open, ensure proper state
  if (window.innerWidth >= 768 && document.body.classList.contains('cart-open')) {
    // Ensure proper desktop cart view
    overlay.classList.add('show');
  }
});

// Initialize cart functionality and ensure script.js functions are available
document.addEventListener('DOMContentLoaded', function() {
  if (typeof productAddToCart !== 'function') {
    console.error('Warning: productAddToCart function not found in script.js');
  }
  // ...
});
