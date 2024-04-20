


  document.addEventListener('DOMContentLoaded', function () {
    const glide = new Glide('.glide', {
      type: 'carousel',
      startAt: 0,
      perView: 3,
      focusAt: 'center',
      gap: 20,
      autoplay: 2000,
      breakpoints: {
        800: {
          perView: 1,
        },
        1200: {
          perView: 2,
        },
      },
    });
  
    glide.mount();
  
    const imageCards = document.querySelectorAll('.image-card');
  
    imageCards.forEach((card) => {
      card.addEventListener('click', () => {
        card.classList.toggle('opened');
      });
    });
  });

  