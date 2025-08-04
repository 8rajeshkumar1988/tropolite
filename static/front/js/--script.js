document.querySelectorAll(".access-menu>li").forEach((item) => {
    item.addEventListener("mouseenter", function (event) {
      open_menu_back(item, event);
    });
    item.addEventListener("click", function (event) {
      open_menu_back(item, event);
    });
    item.addEventListener("mouseleave", function () {
      if (item.children[1].classList.contains("gazab")) {
        item.children[1].classList.remove("gazab");
      }
      $(".back-nav").css("height", `${100}%`);
    });
  });
  
  var heiiii;
  let open_menu_back = (item, event) => {
    heiiii = item.children[1].clientHeight;
    if (window.innerWidth > 769) {
      if (item.children[1].children.length > 6) {
        heiiii = item.children[1].clientHeight;
        item.children[1].classList.add("gazab");
        if (event.type === "mouseenter") {
          $(".back-nav").css("height", `${heiiii - 160}px`);
        } else if (event.type === "click") {
          $(".back-nav").css("height", `${heiiii + 70}px`);
        }
      } else {
        $(".back-nav").css("height", `${heiiii + 60}px`);
      }
    }
  };
  
  $(".access-submenu > li").each(function () {
    var submenu = $(this).find("ul.acc-menu");
    var item_qw = $(this).find(".arrow-img-div");
    var item_img = $(this).find(".arrow-img-div > img");
    var item_a = $(this).find(".list-sub-menu");
    if (window.innerWidth > 1024) {
      $(this).on("mouseenter", function () {
        submenu.addClass("acc-show");
        if ($(".side-bar-pan").height() < $(".acc-menu.acc-show").height()) {
          $(".back-nav").css(
            "height",
            `${$(".acc-menu.acc-show").height() + 80}px`
          );
        } else {
          $(".back-nav").css("height", `${heiiii + 60}px`);
        }
      });
      $(this).on("mouseleave", function () {
        submenu.removeClass("acc-show");
      });
    }
    if (window.innerWidth < 1025) {
      $(item_qw).on("mousemove", function (e) {
        if ($(".arrow-img-div.addd").hasClass("addd")) {
          $(".arrow-img-div.addd").removeClass("addd");
        }
        item_qw.addClass("addd");
        if ($("ul.acc-menu").hasClass("acc-show")) {
          $("ul.acc-menu").removeClass("acc-show");
        }
        submenu.addClass("acc-show");
        item_img.addClass("rotate-like");
        if ($(".side-bar-pan ").height() < $(".acc-menu.acc-show").height()) {
          $(".back-nav").css(
            "height",
            `${$(".acc-menu.acc-show").height() + 80}px`
          );
          if (window.innerWidth < 769) {
            $(".back-nav").css("height", `${100}%`);
          }
        } else {
          if (window.innerWidth < 769) {
            $(".back-nav").css("height", `${100}%`);
          } else {
            $(".back-nav").css("height", `${heiiii + 60}px`);
          }
        }
      });
      $(item_qw).on("mouseleave", function () {
        item_img.removeClass("rotate-like");
      });
    }
  });
  
  $(".access-menu").on("mouseleave", function () {
    $(".back-nav").css("height", `100%`);
    if (window.innerWidth < 769) {
      $(".access-menu").removeClass("menu-open");
      $(".access-menu li").css("display", "none");
      $(".menu-bar").removeClass("fa-x");
      // $('.header').css('margin-top', '40px')
      $(".space").css("display", "none");
      $(".menu-bar").addClass("fa-bars");
      const heei = $(".menu-bar").height();
      $(".back-nav").css("height", `100%`);
      $(".header").removeClass("head-full-cover");
      $("body").css("overflow", "scroll");
      if (document.querySelector(".access-submenu.show-list")) {
        document
          .querySelector(".access-submenu.show-list")
          .classList.remove("show-list");
      }
    }
  });
  if (window.innerWidth < 769) {
    $(".menu-bar").click(function () {
      if ($(".access-menu").hasClass("menu-open")) {
        $(".access-menu").removeClass("menu-open");
        $(".access-menu li").css("display", "none");
        $(".menu-bar").removeClass("fa-x");
        $(".menu-bar").addClass("fa-bars");
        $(".space").css("display", "none");
        const heei = $(".menu-bar").height();
        $(".back-nav").css("height", `100%`);
        $(".header").removeClass("head-full-cover");
        $("body").css("overflow", "scroll");

        $('.show-list').removeClass('show-list')
        $('.acc-menu.acc-show').removeClass('acc-show')
        $('.arrow-img-div.addd').removeClass('addd')
      } else {
        $(".header").addClass("head-full-cover");
        $("body").css("overflow", "hidden");
        $(".access-menu").addClass("menu-open");
        $(".access-menu li").css("display", "block");
        $(".menu-bar").removeClass("fa-bars");
        $(".menu-bar").addClass("fa-x");
        $(".space").css("display", "block");
        const heei = $(".access-menu").height();
        $(".back-nav").css("height", `100%`);
      }
    });
  }
  
  document.querySelectorAll(".access-menu>li").forEach((item) => {
    item.children[0].addEventListener("click", function (e) {
      if (item.children[1].classList.contains("show-list")) {
        item.children[1].classList.remove("show-list");
        const heei = $(".access-menu").height();
        $(".back-nav").css("height", `100%`);
      } else if (item.children[1].classList.contains("double-col")) {
        item.children[1].classList.remove("double-col");
        const heei = $(".access-menu").height();
        $(".back-nav").css("height", `100%`);
      } else {
        if (document.querySelector(".access-submenu.show-list")) {
          document
            .querySelector(".access-submenu.show-list")
            .classList.remove("show-list");
          const heei = $(".access-menu").height();
          $(".back-nav").css("height", `100%`);
        } else if (document.querySelector(".access-submenu.double-col")) {
          document
            .querySelector(".access-submenu.double-col")
            .classList.remove("double-col");
          const heei = $(".access-menu").height();
          $(".back-nav").css("height", `100%`);
        }
  
        if (item.children[1].children.length > 5) {
          item.children[1].classList.add("double-col");
        } else {
          item.children[1].classList.add("show-list");
        }
        const heei = $(".access-menu").height();
        $(".back-nav").css("height", `100%`);
      }
    });
  });
  
  $(document).on("scroll", function () {
    if ($(window).scrollTop() > 500) {
      $(".to-top").css("display", "flex");
    } else {
      $(".to-top").css("display", "none");
    }
  });
  $(".to-top").on("click", function () {
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
    $(".header").css("top", "0");
  });
  document.querySelectorAll(".points").forEach((item) => {
    item.addEventListener("mousemove", function () {
      item.children[2].classList.add("hotspot-on");
    });
    item.addEventListener("mouseleave", function () {
      item.children[2].classList.remove("hotspot-on");
    });
  });
  
  //  animation script   // //
  if (window.innerWidth > 768) {
    const tl_head = gsap.timeline({
      scrollTrigger: {
        trigger: ".main-cara",
        start: "top bottom",
        end: "bottom top",
        // markers: true
      },
    });
    tl_head.to(".main-cara", {
      y: 0,
      duration: 0.5,
      opacity: 1,
    });
    tl_head.from(".create-text>h5 span", {
      delay: 1,
      duration: 0.3,
      position: "relative",
      top: "100px",
      ease: "power4.out",
      delay: -0.5,
      opacity: 0,
      // skewY: 7,
      stagger: {
        amount: 0.5,
      },
    });
  
    const tl_sec_cara = gsap.timeline({
      scrollTrigger: {
        trigger: ".sec-main-cara",
        start: "top 100%",
        toggleActions: "play none none reverse",
        // markers:true
      },
    });
  
    tl_sec_cara.from("#carouselExampleIndicators", {
      y: 300,
      opacity: 0,
      // skewY: 7,
      duration: 0.5,
    });
    tl_sec_cara.from(".sec-cara>h5 span", {
      delay: 1,
      duration: 0.3,
      position: "relative",
      top: "100px",
      ease: "power4.out",
      delay: -0.5,
      opacity: 0,
      // skewY: 7,
      stagger: {
        amount: 0.5,
      },
    });
  
    tl_sec_cara.fromTo(
      ".append-img",
      {
        transform: " translate(0, 150px)",
        opacity: 0,
        // skewY: 10,
      },
      {
        transform: " translate(0, 0px)",
        opacity: 1,
        duration: 0.8,
        // skewY: 0,
      }
    );
  } else {
    gsap.set(".main-cara", { y: 0, opacity: 1 });
  
    gsap.set(".master-piece img", {
      transform: "translateY(0px) skewY(0deg)",
      opacity: 1,
    });
  }

  const tl_book = gsap.timeline({
    scrollTrigger: {
      trigger: "section.book",
      start: "top 90%",
      end: "botom 200px",
      // scrub: 2,
      toggleActions: "play none none reverse",
      // markers: true,
      // pin: true
    },
  });
  // tl_book.timeScale(3)
  tl_book.from("section.book", {
    delay: -0.5,
    y: 500,
    // skewY: 20,
    opacity: 0,
    duration: 1,
    ease: "power4.out",
  });
  tl_book.from(".chef-head>span", {
    delay: -1,
    duration: 0.5,
    position: "relative",
    top: "100px",
    ease: "power4.out",
    opacity: 0,
    // skewY: 20,
    stagger: {
      amount: 0.2,
    },
  });
  tl_book.from(".book-galary>div", {
    y: 300,
    delay: -1,
    // skewY: 20,
    opacity: 0,
    duration: 1,
    ease: "power4.out",
    stagger: 0.3,
  });

 
  const tl_tropo = gsap.timeline({
    scrollTrigger: {
      trigger: ".gourmet",
      start: "top 115%",
      toggleActions: "play none none reverse",
    },
  });
  tl_tropo.from(".gourmet", {
    delay: 0,
    duration: 0.5,
    ease: "power4.out",
    y: 400,
    // skewY: 8,
    opacity: 0,
  });


  if ($(".social")) {
    const tl_social = gsap.timeline({
      scrollTrigger: {
        trigger: ".social",
        start: "top bottom",
        toggleActions: "play none none reverse",
      },
    });
    // tl_social.timeScale(1.7);
    tl_social.from(".social", {
      delay: 0,
      y: 300,
      duration: 1,
      // skewY: 10,
      opacity: 0,
    });
  }
  const tl_truck = gsap.timeline({
    scrollTrigger: {
      trigger: ".deals",
      start: "top 100%",
      toggleActions: "play none none none",
    },
  });
  tl_truck.from(".deals", {
    delay: 0,
    y: 300,
    duration: 0.5,
    // skewY: 10,
    opacity: 0,
  });

  if (window.innerWidth > 768) {
    const tl_footer = gsap.timeline({
      scrollTrigger: {
        trigger: ".footer",
        start: "top 100%",
        toggleActions: "play none none reverse",
      },
    });
    // tl_footer.timeScale(1)
    tl_footer.from(".footer", {
      delay: -0.5,
      duration: 1,
      opacity: 0,
    });
    tl_footer.from(".footer-content>div:nth-child(1) .logo", {
      delay: -0.49,
      duration: 0.5,
      opacity: 0,
    });
    tl_footer.from(".davar", {
      delay: -0.49,
      duration: 0.5,
      opacity: 0,
    });
    tl_footer.from(".footer-content>div:nth-child(2) a", {
      delay: -1.5,
      duration: 1,
      ease: "power4.out",
      opacity: 0,
      stagger: {
        amount: 0.5,
      },
    });
    tl_footer.from(".footer-content>div:nth-child(3) a", {
      delay: -1.3,
      duration: 1,
      ease: "power4.out",
      opacity: 0,
      stagger: {
        amount: 0.5,
      },
    });
    tl_footer.from(".footer-content>div:nth-child(4) a", {
      duration: 1.4,
      delay: -1,
      ease: "power4.out",
      opacity: 0,
      stagger: {
        amount: 0.5,
      },
    });
    tl_footer.from(".footer-content>div:nth-child(5) a", {
      duration: 1.4,
      delay: -1.5,
      ease: "power4.out",
      opacity: 0,
      stagger: {
        amount: 0.5,
      },
    });
  }
  let mm = gsap.matchMedia();
  mm.add("(min-width : 769px)", () => {
    const tl = gsap.timeline({
      scrollTrigger: {
        trigger: ".reach",
        start: "top bottom",
        toggleActions: "play none none reverse",
      },
    });
  
    // tl.timeScale(1.5);
    tl.from(".reach>div", {
      y: 300,
      // skewY: 20,
      opacity: 0,
      duration: 0.5,
      ease: "power4.out",
      stagger: 0.2,
    });
  
    // tl.from(".first-reach>div h1", {
    //   overflow: "hidden",
    //   duration: 1.3,
    //   position: "relative",
    //   top: "100px",
    //   ease: "power4.out",
    //   delay: -0.1,
    //   opacity: 0,
    //   stagger: {
    //     amount: 1,
    //   },
    // });
    tl.from(".first-reach>div p", {
      delay: -1.5,
      ease: "power4.out",
      opacity: 0,
      duration: 0.5,
      stagger: 0.1,
    });
  
    tl.from(".sec-reach>h3 h3", {
      delay: -1.5,
      ease: "power4.out",
      opacity: 0,
      duration: 0.5,
      stagger: 0.1,
    });
    tl.from(".sec-reach>h1 span, .sec-reach>.h1 span", {
      delay: -1.3,
      duration: 0.5,
      position: "relative",
      top: "100px",
      ease: "power4.out",
      // delay: 1,
      opacity: 0,
      // skewY: 20,
      stagger: {
        amount: 0.5,
      },
    });
    // tl.from(".linee p", {
    //   delay: -1.3,
    //   duration: 1,
    //   ease: "power4.out",
    //   opacity: 0,
    //   stagger: {
    //     amount: 2,
    //   },
    // });
  });
  mm.add("(max-width: 768px)", () => {
    const tl = gsap.timeline({
      scrollTrigger: {
        trigger: ".reach",
        start: "top bottom",
        toggleActions: "play none none reverse",
      },
    });
  
    tl.from(".sec-reach", {
      y: 200,
      delay: -1,
      opacity: 0,
      duration: 0.3,
      ease: "power4.out",
      stagger: 0.2,
    });
  
    tl.from(".first-reach", {
      y: 200,
      delay: -1,
      opacity: 0,
      duration: 0.5,
      ease: "power4.out",
      stagger: 0.2,
    });
  });
  
  /////////////// / // / bakery gradient
  if ($(".bakery")) {
    // const tl_bakery = gsap.timeline({
    //   scrollTrigger: {
    //     trigger: ".bakery",
    //     start: "top bottom",
    //     toggleActions: "play none none reverse",
    //   },
    // });
    // tl_bakery.from(".bakery", {
    //   delay: 0.3,
    //   opacity: 0,
    //   y: 300,
    //   // skewY: 20,
    //   duration: 0.5,
    // });
    // tl_bakery.from(".bakery>h1 span", {
    //   delay: -0.3,
    //   duration: 0.5,
    //   position: "relative",
    //   top: "100px",
    //   ease: "power4.out",
    //   opacity: 0,
    //   // skewY: 20,
    //   stagger: {
    //     amount: 0.5,
    //   },
    // // });
    // tl_bakery.from(".bakery>div video", {
    //   delay: -0.3,
    //   opacity: 0,
    //   y: 300,
    //   duration: 0.5,
    //   // skewY: 7,
    // });
    // tl_bakery.from(".bakery>div>h3 span", {
    //   delay: -0.3,
    //   duration: 0.5,
    //   position: "relative",
    //   top: "50px",
    //   ease: "power4.out",
    //   opacity: 0,
    //   // skewY: 20,
    //   // scrub: 10,
    //   stagger: {
    //     amount: 1,
    //   },
    // });
    // tl_bakery.from(".bakery>div p span", {
    //   delay: -1,
    //   duration: 1,
    //   ease: "power4.out",
    //   opacity: 0,
    //   // scrub: 10,
    //   stagger: {
    //     amount: 1,
    //   },
    // });
  }
  if ($(".application")) {
  }
  
  const tl_food = gsap.timeline({
    scrollTrigger: {
      trigger: ".food",
      start: "top bottom",
      toggleActions: "play none none reverse",
    },
  });
  tl_food.from(".food>div:first-child", {
    y: 300,
    opacity: 0,
    // skewY: 7,
    duration: 0.8,
  });
  tl_food.from(".food>div:last-child p span", {
    delay: -0.5,
    opacity: 0,
    duration: 0.9,
    stagger: {
      amount: 2,
    },
  });
  
  document.querySelectorAll("img").forEach((item) => {
    gsap.from(item, {
      scrollTrigger: {
        trigger: item,
        start: "top 100%",
        end: "top 100%",
        toggleActions: "play none none reverse",
      },
      scale: 1.1,
      duration: 1,
      ease: "easeOutQuart",
      duration: 1,
    });
  });
  
  
  var touchStartX;
  var threshold = 50; 
  
  $(".gal-dis").on("touchstart", function (event) {
    touchStartX = event.touches[0].clientX;
  });
  
  $(".gal-dis").on("touchend", function (event) {
    var touchEndX = event.changedTouches[0].clientX;
    var deltaX = touchEndX - touchStartX;
  
    if (Math.abs(deltaX) > threshold) {
      if (deltaX > 0) {
       leftCalled()
      } else {
        // Swiped left, get next element's src value
        rightCalled()
      }
    }
  });
  var leftCalled = ()=>{
    var prevElem = $(".gal-opt .active").prev();
    $(".gal-opt .active").removeClass("active");
    if (!prevElem.length) {
      prevElem = $(".gal-opt").children().last();
      $(".gal-opt").children().last().addClass("active");
      prevElem.addClass("active");
    } else {
      prevElem.addClass("active");
    }

    if (`${prevElem.attr("src")}` === "undefined") {
      $(".gal-dis").children().hide();
      $(".gal-dis .embed_video").show();
    } else {
      $(".gal-dis").children().hide();
      $(".gal-dis img").show();
      $(".gal-dis img").attr("src", `${prevElem.attr("src")}`);
    }
  }
  var rightCalled = ()=>{
    var nextElem = $(".gal-opt .active").next();
    $(".gal-opt .active").removeClass("active");
    if (!nextElem.length) {
      nextElem = $(".gal-opt").children().first();
      $(".gal-opt").children().first().addClass("active");
      nextElem.addClass("active");
    } else {
      nextElem.addClass("active");
    }

    if (`${nextElem.attr("src")}` === "undefined") {
      $(".gal-dis").children().hide();
      $(".gal-dis .embed_video").show();
    } else {
      $(".gal-dis").children().hide();
      $(".gal-dis img").show();
      $(".gal-dis img").attr("src", `${nextElem.attr("src")}`);
    }
  }

  function updateGalleryDisplay(item, title_imgg, thiss) {
    $(".gal-opt img, .gal-opt video, .gal-opt .embed_video").removeClass(
      "active"
    );
    if (item.prop("tagName").toLowerCase() === "div") {
      $(".gal-dis").children().hide();
      $(".gal-dis .embed_video").show();
    } else if (item.prop("tagName").toLowerCase() === "img") {
      $(".gal-dis").children().hide();
      $(".gal-dis img").show();
      $(".gal-dis img").show().attr("src", item.attr("src"));
    } else if (item.prop("tagName").toLowerCase() === "video") {
      $(".gal-dis").children().hide();
      $(".gal-dis video").show();
      $(".gal-dis video").show().attr("src", item.attr("src"));
    }
    if (title_imgg === "None" || title_imgg === "") {
      $(".title-img").text("");
    } else {
      $(".title-img").show().text(title_imgg);
    }
    item.addClass("active");
  }
  
  $(".gal-opt img, .gal-opt video, .gal-opt .embed_video").on(
    "click",
    function () {
      var item = $(this);
      var thiss = this;
      var title_img;
      
      item = $(this);
      title_img = this.title;
     
      updateGalleryDisplay(item, title_img, thiss);
    }
    );
    
    if (window.innerWidth > 768) {
      $(document).keydown(handleKeyDown);
    }
  function handleKeyDown(e) {
    if (e.key === "ArrowLeft" || e.key === "ArrowRight") {
      if (e.key === "ArrowLeft") {
        leftCalled() 
      } else {    
        rightCalled()
      }
    }
  }
  

  
  // slider
  
  var myElement = $(".containerSlider_pro-2");
  myElement.on("wheel", function (event) {
    const delta =
      event.originalEvent.deltaY ||
      event.originalEvent.detail ||
      event.originalEvent.wheelDelta;
    const currentScrollLeft = myElement.scrollLeft();
    const isScrollingDown = delta > 0;
    const isScrollingUp = delta < 0;
    myElement.scrollLeft(currentScrollLeft + delta);
    const isScrolledToRight =
      currentScrollLeft + myElement.innerWidth() >= myElement[0].scrollWidth;
    const isScrolledToLeft = currentScrollLeft === 0;
    const measure_wid = myElement[0].scrollWidth - 20;
    const end_wid = myElement.scrollLeft() + myElement.innerWidth();
    if (myElement.scrollLeft() !== 0 && end_wid < measure_wid) {
      event.preventDefault();
    }
  });
  if (window.innerWidth < 450) {
    // myElement.scrollLeft(100);
  }
  
  //  pro_2card animation
  
  $(".pro-2").each(function () {
    const item_main = $(this);
    const triggerPoint = item_main.find(".pro_2Card");
    // const item = item_main.find('.pro-2 .pro_2Card')
    gsap.from(triggerPoint, {
      scrollTrigger: {
        trigger: item_main,
        toggleActions: "play none none reverse",
      },
      y: 400,
      delay: -1.5,
      opacity: 0,
      stagger: { amount: 0.3 },
      duration: 1,
      ease: "power4.inOut",
    });
  });
  
  
  function validateInputText(input) {
    var input = document.getElementById(input).value;
    var letters = /^[a-zA-Z]*$/;
    var inputField = document.getElementById(input);
  
    if (!input.match(letters)) {
        inputField.value = input.replace(/[^a-zA-Z]/g, '');
    }
  }
  
  
  

  $(document).ready(function () {
    $(".alphaonly").on("input",function(){
      var value =$(this).val();
      var letters = /^[a-zA-Z\s]*$/;
      if (!value.match(letters)) {
          $(this).val(value.replace(/[^a-zA-Z\s]/g, ''));
      }
    });   


    $(".numbers").on("input",function(){
      var value =$(this).val();
      var numbers = /^[0-9]*$/;
      if (!value.match(numbers)) {
          $(this).val(value.replace(/[^0-9]/g, ''));
      }
    });  

    $(".zipcode").on("change",function(){
           
      var zip_code =$(this).val();
      
      
      var settings = {
         "url": "https://api.postalpincode.in/pincode/"+zip_code,
         "method": "GET",
         "timeout": 0,
       };
       
       $.ajax(settings).done(function (response) {
         response=response[0];
         var Status=response.Status;
         if(Status=="Success"){
             var PostOffice=response.PostOffice;
             var state_name=PostOffice[0].State;
             $(".id_state").val(state_name);
             if(state_name){
                 $('.id_state').prop('readonly', true);
             }
             
         }
         
       });
     }); 
   


    if ($(".check-hei")) {
      $(".check-hei").each(function () {
        const item_hei = $(this);
        const givecheck = item_hei.find(".give-check");
        const check_para = item_hei.find(".check-para");
        const check_h4 = item_hei.find(".check-h4").height();
        const check_cta = item_hei.find(".check-cta").height();
        const check_main = item_hei.height();
        const para_hei = check_main - (check_h4 + check_cta + 20);
        var fontHeight = getFontHeight(".give-check");
        var numOfLine = parseInt(para_hei / fontHeight);
        numOfLine = numOfLine - 1;
        check_para.css("height", `${numOfLine * fontHeight}px`);
        givecheck.css("-webkit-line-clamp", `${numOfLine}`);
      });
    }
  });
  
  function getFontHeight(selector) {
    var tempElement = $("<span>").text("M");
    var paragraph = $(selector);
    tempElement.css({
      fontSize: paragraph.css("fontSize"),
      lineHeight: paragraph.css("lineHeight"),
      visibility: "hidden",
      position: "absolute",
    });
    $("body").append(tempElement);
    var fontHeight = tempElement.height();
    tempElement.remove();
    return fontHeight;
  }
  
  $(document).ready(function () {
    var currentUrl = window.location.href;
    var containsAboutUs = currentUrl.includes("about-us");
    containsAboutUs
      ? $(".sec-reach .cta").css("display", "none")
      : $(".sec-reach .cta").css("display", "block");
  });
  
  $(document).ready(function () {
    $("#share_btn").on("click", function () {
      if ($("#share_btn").hasClass("opened")) {
        removeElements();
        $("#share_btn").removeClass("opened");
      } else {
        $("#share_btn").addClass("opened");
        showSharePopup();
      }
    });
  });
  
  function showSharePopup() {
    // Get the current webpage URL
    var currentUrl = window.location.href;
  
    // Construct sharing URLs for different platforms
    var whatsappUrl = "https://wa.me/?text=" + encodeURIComponent(currentUrl);
    var instagramUrl =
      "https://www.instagram.com/share?url=" + encodeURIComponent(currentUrl);
    var telegramUrl =
      "https://t.me/share/url?url=" + encodeURIComponent(currentUrl);
    var facebookUrl =
      "https://www.facebook.com/sharer/sharer.php?u=" +
      encodeURIComponent(currentUrl);
    var messengerUrl =
      "fb-messenger://share/?link=" + encodeURIComponent(currentUrl);
    1;
  
    var myArray = [
      `<i style='color: #E2B57C;' class="share-item fa-brands fa-whatsapp" onclick="shareLink('${whatsappUrl}')"></i>`,
      `<i style='color: #E2B57C;' class="share-item fa-brands fa-instagram" onclick="shareLink('${instagramUrl}')"></i>`,
      `<i style='color: #E2B57C;' class="share-item fa-brands fa-telegram" onclick="shareLink('${telegramUrl}')"></i>`,
      `<i style='color: #E2B57C;' class="share-item fa-brands fa-facebook"  onclick="shareLink('${facebookUrl}')"> </i>`,
      `<i style='color: #E2B57C;' onclick="shareLink('${messengerUrl}')" class="share-item fa-brands fa-facebook-messenger"></i>`,
      `<i style='color: #E2B57C;' class="share-item fa-regular fa-copy" onclick="copied('${currentUrl}')"></i>`,
    ];
    for (var i = 0; i < myArray.length; i++) {}
    for (var i = 0; i < myArray.length; i++) {
      (function (index) {
        setTimeout(function () {
          $("#share").append(myArray[index] + "");
        }, 50 * i);
      })(i);
    }
  }
  
  function shareLink(url) {
    removeElements();
    window.open(url, "yash");
  }
  
  function copied(text) {
    var tempInput = $("<input name='copied' id='copied_d' />");
    $("body").append(tempInput);
    tempInput.val(text);
    tempInput.select();
    document.execCommand("copy");
    tempInput.remove();
    removeElements();
  }
  
  function removeElements() {
    var elementsToRemove = $("#share_btn").nextAll("i");
    elementsToRemove.each(function (index) {
      var element = $(this);
      setTimeout(function () {
        element.remove();
      }, 50 * (index + 1));
    });
  }
  
  $("body").click(function () {
    if ($("#share_btn").hasClass("opened")) {
      removeElements();
    }
  });
  
  const players = [];
  
  const videoElements = $('iframe[src*="player.vimeo.com"]');
  videoElements.each(function () {
    const player = new Vimeo.Player(this);
  
    players.push(player);
  });
  
  function pauseAllVimeoVideos() {
    players.forEach((player) => {
      player.pause().catch((error) => {
        console.error("Error pausing Vimeo video:", error);
      });
    });
  }
  
  function muteAllVimeoVideos() {
    players.forEach((player) => {
      player.setVolume(0).catch((error) => {
        console.error("Error muting Vimeo video:", error);
      });
    });
  }
  function playAllVimeoVideos() {
    players.forEach((player) => {
      player.play().catch((error) => {
        console.error("Error pausing Vimeo video:", error);
      });
    });
  }
  
  $(document).on("visibilitychange", () => {
    if (document.visibilityState !== "visible") {
      // pauseAllVimeoVideos();
      muteAllVimeoVideos();
    }
  });
  
  function handleVisibilityChange(entries, observer) {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        // playMusic();
      } else {
        pauseMusic();
      }
    });
  }
  
  const options = {
    root: null,
    rootMargin: "0px",
    threshold: 0.5,
  };
  
  const intersectionObserver = new IntersectionObserver(
    handleVisibilityChange,
    options
  );
  
  const carouselElement = document.getElementById("carouselExampleDark");
  
  if (carouselElement) {
    intersectionObserver.observe(carouselElement);
  }
  
  function pauseMusic() {
    muteAllVimeoVideos();
  }
  
  // $("body").on("wheel", function (event) {
  //   if (event.originalEvent.deltaY > 0) {
  //     $(".header").css("top", "-90px");
  //   } else if (event.originalEvent.deltaY < 0) {
  //     $(".header").css("top", "0px");
  //   }
  // });
  
  // var touchStartY;
  // document.addEventListener("touchstart", function (event) {
  //   touchStartY = event.touches[0].clientY;
  // });
  
  // document.addEventListener("touchmove", function (event) {
  //   event.preventDefault();
  //   var touchEndY = event.touches[0].clientY;
  //   var deltaY = touchEndY - touchStartY;
  
  //   if (deltaY > 0) {
  //     $(".header").css("top", "0px");
  //   } else {
  //     $(".header").css("top", "-90px");
  //   }
  // });
  
  
  
  // const isiOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
  const isiOS = /iPad|iPhone|iPod/.test(navigator.platform) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  const isAndroid = navigator.userAgent.toLowerCase().includes("android");
  const isWindows = navigator.platform.toLowerCase().includes("win");
  const isMac = navigator.platform.toLowerCase().includes("mac");
  var navbar = document.querySelector(".header");
  if (isiOS) {
  //  $('.happy-taste').html('ios')
    // $("section.header").addClass("for_ios");
  
    let prevScrollPos = window.scrollY || window.pageYOffset;
    const navbar = document.querySelector(".header");
  
    window.onscroll = function () {
      const currentScrollPos = window.scrollY || window.pageYOffset;
      
      if (prevScrollPos > currentScrollPos) {
        navbar.style.top = "0px";
      } else {
        if (prevScrollPos > 150 & currentScrollPos > 150) {
          navbar.style.top = "-90px";
        }
      }
  
      prevScrollPos = currentScrollPos;
    };
  } else if(isAndroid){
    // $('.happy-taste').html('andriod')
    let prevScrollPos = window.scrollY || window.pageYOffset;
    const navbar = document.querySelector(".header");
  
    window.onscroll = function () {
      const currentScrollPos = window.scrollY || window.pageYOffset;
      if (prevScrollPos > currentScrollPos) {
        navbar.style.top = "0px";
      } else {
        navbar.style.top = "-90px";
      }
  
      prevScrollPos = currentScrollPos;
    };
  }  else if(isMac){
    // $('.happy-taste').html(navigator.userAgent.toLowerCase())
    let prevScrollPos = window.scrollY || window.pageYOffset;
    const navbar = document.querySelector(".header");
  
    window.onscroll = function () {
      const currentScrollPos = window.scrollY || window.pageYOffset;
  
      if (prevScrollPos > currentScrollPos) {
        navbar.style.top = "0px";
      } else {
        navbar.style.top = "-90px";
      }
  
      prevScrollPos = currentScrollPos;
    };
  }
  else if(isWindows){
    // $('.happy-taste').html('window')
    let prevScrollPos = window.scrollY || window.pageYOffset;
    const navbar = document.querySelector(".header");
  
    window.onscroll = function () {
      const currentScrollPos = window.scrollY || window.pageYOffset;
  
      if (prevScrollPos > currentScrollPos) {
        navbar.style.top = "0px";
      } else {
        navbar.style.top = "-90px";
      }
  
      prevScrollPos = currentScrollPos;
    };
  }  else{
    // $('.happy-taste').html('not detected')
    let prevScrollPos = window.scrollY || window.pageYOffset;
    const navbar = document.querySelector(".header");
  
    window.onscroll = function () {
      const currentScrollPos = window.scrollY || window.pageYOffset;
  
      if (prevScrollPos > currentScrollPos) {
        navbar.style.top = "0px";
      } else {
        navbar.style.top = "-90px";
      }
  
      prevScrollPos = currentScrollPos;
    };
  }






  


  