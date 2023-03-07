class Header {
  constructor() {
    //switches
    this.slideDownBtn = false;
  }

  start() {
    this.animateElements();
    this.slideDown();
    this.logoSlider();
  }

  //mobile menu
  slideDown() {
    let menu = $(".nav-menu");
    $("#slide-down-btn").click(function () {
      if (!this.slideDownBtn) {
        menu.css("display", "block");

        $(this).find("i").removeClass("fa-caret-down");
        $(this).find("i").addClass("fa-caret-up");
        this.slideDownBtn = true;
      } else {
        menu.css("display", "none");

        $(this).find("i").removeClass("fa-caret-up");
        $(this).find("i").addClass("fa-caret-down");
        this.slideDownBtn = false;
      }
    });
  }

  logoSlider() {
    $(".customer-logos").slick({
      slidesToShow: 6,
      slidesToScroll: 1,
      autoplay: true,
      autoplaySpeed: 1500,
      arrows: false,
      dots: false,
      pauseOnHover: false,
      responsive: [
        {
          breakpoint: 768,
          settings: {
            slidesToShow: 4,
          },
        },
        {
          breakpoint: 520,
          settings: {
            slidesToShow: 3,
          },
        },
      ],
    });
  }

  animateElements(){
    $(function() {
      // Select all elements with "animate" class
      var $animatedElements = $('.animate');
      
      // Create IntersectionObserver instance
      var observer = new IntersectionObserver(function(entries) {
        // For each entry, check if it is intersecting and add/remove "animate" class accordingly
        entries.forEach(function(entry) {
          if (entry.isIntersecting) {
            $(entry.target).addClass('animated');
          } 
        });
      }, {
        // Optional options for the IntersectionObserver
        threshold: 0.5 // Trigger when element is 50% visible in viewport
      });
      
      // Observe each animated element
      $animatedElements.each(function() {
        observer.observe(this);
      });
    });
  }

}

const header = new Header();

$(document).ready(function () {
  header.start();
});