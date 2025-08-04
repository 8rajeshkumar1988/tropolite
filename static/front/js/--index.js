var tl1 = gsap.timeline();
// let tl = gsap.timeline()
gsap.to('.classs', {
    scrollTrigger: {
        trigger: '.classs',
        start: 'top 120%' ,        
    },
    transform: "translateX(0px)",
    scale: 1,
    opacity: 1,
    duration: 1
})
gsap.to('.sec-reach p',{
    scrollTrigger: {
        trigger: '.sec-reach p',
        start: 'top 80%' ,
        end:' top top',        
    },
    delay: 0.5,
    opacity: 1,
    duration:1
})
gsap.to('.first-reach h1',{
    scrollTrigger: {
        trigger: '.first-reach h1',
        start: 'top 120%',
        // scrub: true
    },
    transform: "translateY(0px)",
    scale: 1,
    opacity: 1,
    duration: 1
})

gsap.to('.first-reach p',{
    scrollTrigger: {
        trigger: '.first-reach p',
        start: 'top 80%' ,
        end:' top top',        
    },
    delay: 1,
    opacity: 1,
    duration:1
})
gsap.to('.chef-head', {
    scrollTrigger: {
        trigger: '.chef-head',
        start: 'top 100%' ,        
    },
    transform: "translateX(0px)",
    opacity: 1,
    duration: 1
})

gsap.to('.gal-1', {
    scrollTrigger: {
        trigger: '.gal-1',
        start: 'top 110%' ,
    },
    transform: 'skew(0deg, 0deg)',
    duration: 0.5
})
gsap.to('.gal-2', {
    scrollTrigger: {
        trigger: '.gal-2',
        start: 'top 110%' ,
    },
    transform: 'skew(0deg, 0deg)',
    duration: 1
})

gsap.to('.gal-3', {
    scrollTrigger: {
        trigger: '.gal-3',
        start: 'top 110%' ,
    },
    transform: 'skew(0deg, 0deg)',
    duration: 1.5
})
gsap.to('.gal-4', {
    scrollTrigger: {
        trigger: '.gal-4',
        start: 'top 110%' ,
    },
    transform: 'skew(0deg, 0deg)' ,
    duration: 0.5
})
gsap.to('.gal-5', {
    scrollTrigger: {
        trigger: '.gal-5',
        start: 'top 110%' ,
    },
    transform: 'skew(0deg, 0deg)',
    duration: 1.5    
})

gsap.to('.master-div h1', {
    scrollTrigger: {
        trigger: '.master-div h1', 
        start: 'top 90%' ,
    },
    transform : 'translateX(0px)',
    opacity: 1,
    duration : 1
})

gsap.to('.gourmet .gourmet-item h1', {
    scrollTrigger:{
        trigger: '.gourmet .gourmet-item h1',
        start : 'top 105%'
    },
    transform : 'translateY(0px)',
    opacity: 1,
    duration : 0.5
})
gsap.to('.gourmet .gourmet-item h4', {
    scrollTrigger:{
        trigger: '.gourmet .gourmet-item h4',
        start : 'top 95%'
    },
    transform : 'translateY(0px)',
    opacity: 1,
    duration : 1,
    delay: 1
})
gsap.to('.master-div>div', {
    scrollTrigger: {
        trigger: '.master-div>div',
        start: 'top 90%'
    },
    opacity: 1,
    duration: 1,
    delay: 0.5
})
gsap.to('.gourmet .gourmet-item img', {
    scrollTrigger: {
        trigger: '.gourmet .gourmet-item img',
        start: 'top 100%'
    },
    scale: 1,
    duration: 0.5,    
})

gsap.to('.social-posts div:first-child, .social h1', {
    scrollTrigger: {
        trigger: '.social-posts div:first-child, .social h1',
        start: 'top 90%',              
    },
    transform: 'translateX(0) skew(0deg, 0deg)',
    opacity: 1,
    duration: 0.5,
})
gsap.to('.social-posts div:nth-child(2)', {
    scrollTrigger: {
        trigger: '.social-posts div:nth-child(2)',
        start: 'top 90%',              
    },
    transform: 'translateX(0) skew(0deg, 0deg)',
    delay: 0.5,
    duration: 0.5,
})
gsap.to('.social-posts div:nth-child(3)', {
    scrollTrigger: {
        trigger: '.social-posts div:nth-child(3)',
        start: 'top 90%',              
    },
    transform: 'translateX(0) skew(0deg, 0deg)',
    delay: 0.5,
    duration: 1,
})
gsap.to('.deals h1', {
    scrollTrigger: {
        trigger: '.deals h1',
        start: 'top 90%',              
    },
    transform: 'translateX(0)',
    duration: 1,
})
gsap.to('.footer-content', {
    scrollTrigger: {
        trigger: '.footer-content',
        start: 'top 110%',              
    },
    transform: 'translate(0px, 0px)',
    duration: 0.5,
    opacity: 1
})




// const image = document.getElementById("bend-image");

// Add a mousemove event listener to the image container
document.querySelectorAll('.book-galary div').forEach(item=>{
    item.addEventListener("mousemove", (event) => {
        const { clientX, clientY } = event;
    
        // Calculate the angle based on the cursor position
        const xOffset = clientX / window.innerWidth - 1;
        const yOffset = clientY / window.innerHeight - 1;
        const angle = 20; // You can adjust this value to control the bending effect.
    
        // Apply the bending effect using GSAP
        gsap.to(item, {
            duration: 0.5,
            rotationX: angle * yOffset,
            rotationY: angle * xOffset,
            ease: "power2.out", // You can change the ease type as needed.
        });
    });
})

// // Reset the image on mouseleave
document.querySelectorAll('.book-galary div').forEach(item=>{
    item.addEventListener("mouseleave", () => {
        gsap.to(item, {
            duration: 0.5  ,
            rotationX: 0,
            rotationY: 0,
            ease: "power2.out",
        });
    });
})


// const tl = gsap.timeline({
//     scrollTrigger: {
//         trigger: box,
//         start: 'top center',
//         end: 'bottom center',
//         toggleActions: 'play pause reverse pause', // Actions to take on trigger
//     }
// });

// tl.to(box, {
//     x: 300,
//     rotation: 360,
//     scale: 1.5,
//     duration: 1,
// });
// var vara = new Vara(
//   "#baccha",
//   "https://rawcdn.githack.com/akzhy/Vara/ed6ab92fdf196596266ae76867c415fa659eb348/fonts/Satisfy/SatisfySL.json",
//   [
//     {
//       text: "Gourmet Excellence",
//       y: 150,
//       fromCurrentPosition: { y: false },
//       duration: 3000
//     }
//   ],
//   {
//     strokeWidth: 1,
//     color: "red",
//     fontSize: '70px',
//     textAlign: "center",
//     fontFamily: 'castlegar'
                                                                                                                                                           
//   }
// );
// vara.ready(function() {
//   var erase = false;
//   vara.animationEnd(function(i, o) {
//     if (i == "no_erase") erase = false;
//     if (erase) {
//       o.container.style.transition = "opacity 1s 1s";
//       o.container.style.opacity = 0;
//     }
//   });
//   // vara.get("github").container.style.cursor = "pointer";
//   // vara.get("github").container.onclick = function() {
//   //   document.querySelector("#link").click();
//   // };
// });

    
$('.access-menu').on('mousemove', function(){
    const heiii = $('.access-submenu').height()
    console.log(heiii);
    $('.back-nav').css("height", `${heiii + 60}px`)
    if(window.innerWidth < 769){
        $('.back-nav').css("height", `100%`)
    }
})
$('.access-menu').on('mouseleave', function(){
    $('.back-nav').css("height", `100%`)
})

$('.menu-bar').on('click', function(){
    $('.access-menu').addClass('menu-open')
    $(".access-menu li").css('display', 'block')
})
$('.access-menu').on('mouseleave', function(){
    if(innerWidth  < 770){
        $('.access-menu').removeClass('menu-open')
        $(".access-menu li").css('display', 'none')
    }
})

$('.access-menu').on('click', function() {
    console.log('cliclajdfj');
});





//?? A1
const scrollSwipeHandler = (e) => {
    if ((canUpScroll && e.wheelDeltaY > 100) || (canScroll && e.wheelDeltaY > 50 && currentSectionIndex - 1 >= 0)) {
        // wheel up
        // console.log("up");
        currentSectionIndex--;
        goTo("L");
        canScroll = false;
        if (canUpScroll) {
            gsap.set([document.body, 'html'], {
                overflow: "hidden",
                height: '100%'
            });
            canUpScroll = false;
        }
        setTimeout(() => {
            canScroll = true;
        }, 1000);
    } else if (
        canScroll &&
        e.wheelDeltaY < -50 &&
        currentSectionIndex + 1 < sections.length
    ) {
        // wheel down
        // console.log("down");
        currentSectionIndex++;
        goTo("R");
        canScroll = false;
        setTimeout(() => {
            canScroll = true;
        }, 1000);
    }
    else if (canScroll && currentSectionIndex == 3 && e.wheelDeltaY < -50) {
        // currentSectionIndex = 4
        canScroll = false;
        canUpScroll = false;
        gsap.set([document.body, 'html'], {
            overflow: "unset",
            height: 'auto'
        });
        initScrollTopTimeline()
    }
}


// gsap.to("body", {
//     scrollTrigger: {
//         trigger: "#containerSlider", // The trigger element
//         start: "center center", // When the center of the trigger element reaches the center of the viewport
//         end: "center center", // When the center of the trigger element leaves the center of the viewport
//         toggleActions: "play none none none" // Animation actions on enter/leave
//     },
//     onUpdate: function () {
//         document.querySelector('body').style.overflow = "hidden"
//         // document.addEventListener("wheel", scrollSwipeHandler);
//     }
// });




// document.querySelectorAll('.pro_2Card').forEach((element)=>{
//     element.style.transform = "translateX(-350px)"
// })


