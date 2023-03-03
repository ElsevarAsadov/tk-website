class Header {
  constructor() {
    //switches
    this.slideDownBtn = false;
  }

  start() {
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

  logoSlider(){
    $('.customer-logos').slick({
      slidesToShow: 6,
      slidesToScroll: 1,
      autoplay: true,
      autoplaySpeed: 1500,
      arrows: false,
      dots: false,
      pauseOnHover: false,
      responsive: [{
          breakpoint: 768,
          settings: {
              slidesToShow: 4
          }
      }, {
          breakpoint: 520,
          settings: {
              slidesToShow: 3
          }
      }]
  });
  }
}


const header = new Header();

$(document).ready(function () {
  header.start();
});
