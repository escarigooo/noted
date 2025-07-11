document.addEventListener('DOMContentLoaded', function() {
  console.log("Product details script loaded");
  
  // Debug mode
  const DEBUG = true;
  
  function log(message) {
    if (DEBUG) console.log(`[Product Gallery] ${message}`);
  }
  
  log("Initializing product gallery...");
  
  // Get elements
  const mainImage = document.getElementById('main-product-image');
  const thumbnails = document.querySelectorAll('.thumbnail-container');
  const prevButton = document.getElementById('prevImage');
  const nextButton = document.getElementById('nextImage');
  
  if (!mainImage) {
    log("Error: Main image element not found!");
    return;
  }
  
  log(`Found ${thumbnails.length} thumbnails`);
  
  // Hide navigation if we don't have enough images
  if (thumbnails.length <= 1) {
    log("Not enough images for navigation, hiding controls");
    if (prevButton) prevButton.style.display = 'none';
    if (nextButton) nextButton.style.display = 'none';
    return;
  }
  
  // Track current active thumbnail index
  let currentIndex = 0;
  
  // Set up thumbnail click events
  thumbnails.forEach((thumbnail, index) => {
    log(`Setting up thumbnail ${index}`);
    thumbnail.addEventListener('click', function() {
      log(`Thumbnail ${index} clicked`);
      changeImage(index);
    });
  });
  
  // Set up navigation buttons
  if (prevButton) {
    log("Setting up prev button");
    prevButton.addEventListener('click', function(e) {
      e.preventDefault();
      log("Previous button clicked");
      const newIndex = (currentIndex - 1 + thumbnails.length) % thumbnails.length;
      changeImage(newIndex);
    });
  } else {
    log("Warning: Previous button not found");
  }
  
  if (nextButton) {
    log("Setting up next button");
    nextButton.addEventListener('click', function(e) {
      e.preventDefault();
      log("Next button clicked");
      const newIndex = (currentIndex + 1) % thumbnails.length;
      changeImage(newIndex);
    });
  } else {
    log("Warning: Next button not found");
  }
  
  // Function to change the active image
  function changeImage(index) {
    log(`Changing to image at index ${index}`);
    
    // Make sure index is valid
    if (index < 0 || index >= thumbnails.length) {
      log(`ERROR: Invalid index ${index}`);
      return;
    }
    
    // Update current index
    currentIndex = index;
    
    // Get image source from data attribute
    const newSrc = thumbnails[index].getAttribute('data-src');
    log(`New image source: ${newSrc}`);
    
    // Update main image
    if (mainImage && newSrc) {
      mainImage.src = newSrc;
      log(`Updated main image src to: ${newSrc}`);
    } else {
      log("ERROR: Couldn't update main image");
      log("mainImage:", mainImage);
      log("newSrc:", newSrc);
    }
    
    // Update active thumbnail
    thumbnails.forEach(thumb => thumb.classList.remove('active'));
    thumbnails[index].classList.add('active');
    log(`Updated active class to thumbnail ${index}`);
  }
  
  // Keyboard navigation
  document.addEventListener('keydown', function(e) {
    if (e.key === 'ArrowLeft' && prevButton) {
      prevButton.click();
    } else if (e.key === 'ArrowRight' && nextButton) {
      nextButton.click();
    }
  });
  
  // Inicializar outros elementos da página
  initColorCircles();
  initMaterialButtons();
  
  // Initialize color circles
  function initColorCircles() {
    const colorCircles = document.querySelectorAll('.color-circle[data-color-hex]');
    const colorNameElement = document.querySelector('.color-name');
    
    colorCircles.forEach(circle => {
      // Set color circle backgrounds
      const colorHex = circle.dataset.colorHex;
      if (colorHex) {
        circle.style.backgroundColor = colorHex;
      }
      
      // Add click handler
      circle.addEventListener('click', function() {
        colorCircles.forEach(c => c.classList.remove('active'));
        circle.classList.add('active');
        
        if (colorNameElement) {
          colorNameElement.textContent = circle.dataset.color || 'Default';
        }
      });
    });
  }
  
  // Initialize material buttons
  function initMaterialButtons() {
    const materialBtns = document.querySelectorAll('.material-btn');
    const priceIndicator = document.querySelector('.price-indicator');
    const descInput = document.querySelector('.material-desc-input');
    
    materialBtns.forEach(btn => {
      btn.addEventListener('click', function() {
        materialBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        
        if (priceIndicator) {
          const price = btn.dataset.price || '';
          priceIndicator.textContent = `${price}€`;
        }
        
        if (descInput) {
          descInput.value = btn.textContent.trim();
        }
      });
    });
  }
  
  // Inicializar outros elementos da página
  initColorCircles();
  initMaterialButtons();
  
  // Initialize color circles
  function initColorCircles() {
    const colorCircles = document.querySelectorAll('.color-circle[data-color-hex]');
    const colorNameElement = document.querySelector('.color-name');
    
    colorCircles.forEach(circle => {
      // Set color circle backgrounds
      const colorHex = circle.dataset.colorHex;
      if (colorHex) {
        circle.style.backgroundColor = colorHex;
      }
      
      // Add click handler
      circle.addEventListener('click', function() {
        colorCircles.forEach(c => c.classList.remove('active'));
        circle.classList.add('active');
        
        if (colorNameElement) {
          colorNameElement.textContent = circle.dataset.color || 'Default';
        }
      });
    });
  }
  
  // Initialize material buttons
  function initMaterialButtons() {
    const materialBtns = document.querySelectorAll('.material-btn');
    const priceIndicator = document.querySelector('.price-indicator');
    const descInput = document.querySelector('.material-desc-input');
    
    materialBtns.forEach(btn => {
      btn.addEventListener('click', function() {
        materialBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        
        if (priceIndicator) {
          const price = btn.dataset.price || '';
          priceIndicator.textContent = `${price}€`;
        }
        
        if (descInput) {
          descInput.value = btn.textContent.trim();
        }
      });
    });
  }
  
  // Inicializar outros elementos da página
  initColorCircles();
  initMaterialButtons();
  
  // Initialize color circles
  function initColorCircles() {
    const colorCircles = document.querySelectorAll('.color-circle[data-color-hex]');
    const colorNameElement = document.querySelector('.color-name');
    
    colorCircles.forEach(circle => {
      // Set color circle backgrounds
      const colorHex = circle.dataset.colorHex;
      if (colorHex) {
        circle.style.backgroundColor = colorHex;
      }
      
      // Add click handler
      circle.addEventListener('click', function() {
        colorCircles.forEach(c => c.classList.remove('active'));
        circle.classList.add('active');
        
        if (colorNameElement) {
          colorNameElement.textContent = circle.dataset.color || 'Default';
        }
      });
    });
  }
  
  // Initialize material buttons
  function initMaterialButtons() {
    const materialBtns = document.querySelectorAll('.material-btn');
    const priceIndicator = document.querySelector('.price-indicator');
    const descInput = document.querySelector('.material-desc-input');
    
    materialBtns.forEach(btn => {
      btn.addEventListener('click', function() {
        materialBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        
        if (priceIndicator) {
          const price = btn.dataset.price || '';
          priceIndicator.textContent = `${price}€`;
        }
        
        if (descInput) {
          descInput.value = btn.textContent.trim();
        }
      });
    });
  }
  
  // Inicializar outros elementos da página
  initColorCircles();
  initMaterialButtons();
  
  // Initialize color circles
  function initColorCircles() {
    const colorCircles = document.querySelectorAll('.color-circle[data-color-hex]');
    const colorNameElement = document.querySelector('.color-name');
    
    colorCircles.forEach(circle => {
      // Set color circle backgrounds
      const colorHex = circle.dataset.colorHex;
      if (colorHex) {
        circle.style.backgroundColor = colorHex;
      }
      
      // Add click handler
      circle.addEventListener('click', function() {
        colorCircles.forEach(c => c.classList.remove('active'));
        circle.classList.add('active');
        
        if (colorNameElement) {
          colorNameElement.textContent = circle.dataset.color || 'Default';
        }
      });
    });
  }
  
  // Initialize material buttons
  function initMaterialButtons() {
    const materialBtns = document.querySelectorAll('.material-btn');
    const priceIndicator = document.querySelector('.price-indicator');
    const descInput = document.querySelector('.material-desc-input');
    
    materialBtns.forEach(btn => {
      btn.addEventListener('click', function() {
        materialBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        
        if (priceIndicator) {
          const price = btn.dataset.price || '';
          priceIndicator.textContent = `${price}€`;
        }
        
        if (descInput) {
          descInput.value = btn.textContent.trim();
        }
      });
    });
  }
  
  // Inicializar outros elementos da página
  initColorCircles();
  initMaterialButtons();
  
  // Initialize color circles
  function initColorCircles() {
    const colorCircles = document.querySelectorAll('.color-circle[data-color-hex]');
    const colorNameElement = document.querySelector('.color-name');
    
    colorCircles.forEach(circle => {
      // Set color circle backgrounds
      const colorHex = circle.dataset.colorHex;
      if (colorHex) {
        circle.style.backgroundColor = colorHex;
      }
      
      // Add click handler
      circle.addEventListener('click', function() {
        colorCircles.forEach(c => c.classList.remove('active'));
        circle.classList.add('active');
        
        if (colorNameElement) {
          colorNameElement.textContent = circle.dataset.color || 'Default';
        }
      });
    });
  }
  
  // Initialize material buttons
  function initMaterialButtons() {
    const materialBtns = document.querySelectorAll('.material-btn');
    const priceIndicator = document.querySelector('.price-indicator');
    const descInput = document.querySelector('.material-desc-input');
    
    materialBtns.forEach(btn => {
      btn.addEventListener('click', function() {
        materialBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        
        if (priceIndicator) {
          const price = btn.dataset.price || '';
          priceIndicator.textContent = `${price}€`;
        }
        
        if (descInput) {
          descInput.value = btn.textContent.trim();
        }
      });
    });
  }
  
  // Inicializar navegação para produtos relacionados
  initRelatedProductsNavigation();
  
  // Function to initialize related products navigation
  function initRelatedProductsNavigation() {
    const prevRelatedBtn = document.getElementById('prevRelated');
    const nextRelatedBtn = document.getElementById('nextRelated');
    const relatedWrapper = document.getElementById('relatedProductsWrapper');
    
    if (!relatedWrapper) {
      log("No related products wrapper found");
      return;
    }
    
    log("Initializing related products navigation");
    
    // Check if we have any related products
    const relatedProducts = relatedWrapper.querySelectorAll('.related-product');
    if (relatedProducts.length === 0) {
      log("No related products found");
      if (prevRelatedBtn) prevRelatedBtn.style.display = 'none';
      if (nextRelatedBtn) nextRelatedBtn.style.display = 'none';
      return;
    }
    
    log(`Found ${relatedProducts.length} related products`);
    
    // Set up navigation buttons
    if (prevRelatedBtn) {
      prevRelatedBtn.addEventListener('click', function() {
        log("Scrolling related products left");
        relatedWrapper.scrollBy({ left: -250, behavior: 'smooth' });
      });
    }
    
    if (nextRelatedBtn) {
      nextRelatedBtn.addEventListener('click', function() {
        log("Scrolling related products right");
        relatedWrapper.scrollBy({ left: 250, behavior: 'smooth' });
      });
    }
  }
});
