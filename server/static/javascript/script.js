// script.js
const card = document.querySelector('.card');
 
card.addEventListener('mouseover', function () {
  card.style.transform = 'scale(1.2)';
});
 
card.addEventListener('mouseout', function () {
  card.style.transform = 'scale(1)';
});


const swiper = new Swiper('.swiper', {
    // Optional parameters
    slidesPerView: 5,
    spaceBetween: 310,

    //direction: 'vertical',
    loop: true,
  
    // If we need pagination
    pagination: {
      el: '.swiper-pagination',
    },
  
    // Navigation arrows
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
  
    // And if we need scrollbar
    scrollbar: {
      el: '.swiper-scrollbar',
    },
  });