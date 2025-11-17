// Initialize AOS animation
AOS.init({
  duration: 1000,
  once: true
});

// Toggle mobile menu
document.querySelector('.menu-toggle').addEventListener('click', () => {
  document.querySelector('.navbar nav').classList.toggle('show');
});

// Accordion toggle
document.querySelectorAll('.accordion-title').forEach(title => {
  title.addEventListener('click', () => {
    const content = title.nextElementSibling;
    content.style.display = content.style.display === 'block' ? 'none' : 'block';
  });
});

// Accordion active state management
const accordionItems = document.querySelectorAll(".accordion-item");

accordionItems.forEach(item => {
  item.addEventListener("click", () => {
    accordionItems.forEach(el => {
      if (el !== item) el.classList.remove("active");
    });
    item.classList.toggle("active");
  });
});

// Counter animation on scroll
const counters = document.querySelectorAll('.counter');
let counterStarted = false;

const startCounters = () => {
  counters.forEach(counter => {
    counter.innerText = '0';
    const updateCounter = () => {
      const target = +counter.getAttribute('data-target');
      const count = +counter.innerText;
      const increment = target / 100;

      if (count < target) {
        counter.innerText = Math.ceil(count + increment);
        setTimeout(updateCounter, 20);
      } else {
        counter.innerText = target; 
      }
    };
    updateCounter();
  });
};

window.addEventListener('scroll', () => {
  const counterSection = document.querySelector('.counter-section');
  const sectionTop = counterSection.offsetTop;

  if (!counterStarted && window.scrollY + window.innerHeight >= sectionTop) {
    startCounters();
    counterStarted = true;
  }
});

// Back to top button
const btn = document.getElementById("backToTop");

// Show button after scrolling down 300px
window.onscroll = function () {
  if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
    btn.style.display = "block";
  } else {
    btn.style.display = "none";
  }
};

// Scroll to top on button click
btn.addEventListener("click", () => {
  window.scrollTo({
    top: 0,
    behavior: "smooth"
  });
});

// Sticky header on scroll
window.addEventListener("scroll", function () {
  const header = document.getElementById("mainHeader");
  if (window.scrollY > 100) {
    header.classList.add("fixed");
  } else {
    header.classList.remove("fixed");
  }
});


var typed = new Typed(".auto-type",{
      strings : ["OUR GREAT CLIENTS", "WHAT THEY SAY", "TESTIMONIALS"],
      typeSpeed : 60,
      backSpeed : 30,
      loop: true
    })

    
