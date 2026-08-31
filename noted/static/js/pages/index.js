// Enhanced attractive image animation
document.addEventListener('DOMContentLoaded', function() {
  const img = document.querySelector('.hero-image-block img');
  if (!img) return;
  
  // Add floating animation class after page loads with entrance effect
  setTimeout(() => {
    img.style.transform = 'translateY(0px) scale(1)';
    img.style.opacity = '1';
    img.classList.add('floating');
  }, 300);
  
  // Enhanced scroll effect with more dynamic movement
  function handleScroll() {
    const rect = img.getBoundingClientRect();
    const windowHeight = window.innerHeight;
    const isVisible = rect.top < windowHeight && rect.bottom > 0;
    
    if (isVisible) {
      const scrollProgress = Math.max(0, Math.min(1, (windowHeight - rect.top) / windowHeight));
      const parallaxOffset = (scrollProgress - 0.5) * 20;
      const rotateAmount = (scrollProgress - 0.5) * 3;
      const scaleAmount = 0.98 + (scrollProgress * 0.04);
      
      img.style.transform = `translateY(${parallaxOffset}px) rotate(${rotateAmount}deg) scale(${scaleAmount})`;
      img.style.opacity = 0.8 + (scrollProgress * 0.2);
    }
  }
  
  // Smooth scroll listener with RAF
  let ticking = false;
  window.addEventListener('scroll', () => {
    if (!ticking) {
      requestAnimationFrame(() => {
        handleScroll();
        ticking = false;
      });
      ticking = true;
    }
  });
  
  // Add mouse move parallax effect
  const heroSection = document.querySelector('.hero-section');
  if (heroSection) {
    heroSection.addEventListener('mousemove', (e) => {
      const rect = heroSection.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width;
      const y = (e.clientY - rect.top) / rect.height;
      
      const moveX = (x - 0.5) * 15;
      const moveY = (y - 0.5) * 15;
      
      img.style.transform += ` translate(${moveX}px, ${moveY}px)`;
    });
    
    heroSection.addEventListener('mouseleave', () => {
      img.style.transform = img.style.transform.replace(/translate\([^)]*\)/g, '');
    });
  }
  
  // Initial call
  handleScroll();
  
  // Adding counter animation for stats
  const userCountElement = document.querySelector('.hero-stats .stat:first-child h2');
  if (userCountElement) {
    const finalCount = parseInt(userCountElement.textContent, 10);
    if (!isNaN(finalCount)) {
      // Start from zero
      userCountElement.textContent = '0';
      
      // Animate to the final number
      let currentCount = 0;
      const duration = 2000; // ms
      const interval = 50; // ms
      const steps = duration / interval;
      const increment = finalCount / steps;
      
      const counter = setInterval(() => {
        currentCount += increment;
        if (currentCount >= finalCount) {
          userCountElement.textContent = finalCount;
          clearInterval(counter);
        } else {
          userCountElement.textContent = Math.floor(currentCount);
        }
      }, interval);
    }
  }

});