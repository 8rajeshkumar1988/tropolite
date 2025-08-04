let buyNowCanvas = document.querySelector("canvas");
let buyNowCanvasContext = buyNowCanvas.getContext("2d");
let buyNowFrameCount = 180
let buyNowSeqImages = []
let buyNowSeq = {
    frame: 0,
  }

var loaded = 0;

for (let i = 1; i <= buyNowFrameCount; i++) {
  const img = new Image();
  img.src = `/static/front/assets/shop/s${i}.webp`;
  
  img.style.width = '100%'
  if(window.innerWidth < 600){
  }
  // img.src = `{% static 'front/assets/shop/s${i}.webp' %}`;
  // console.log(img.src);
  buyNowSeqImages.push(img);
  
}


let buyNowImg;
let buyNowCanvasRender;
const storeImg = new Image();
storeImg.src = `../static/front/assets/deals.webp`;
storeImg.onload = function () {
  buyNowImg = document.querySelector(".deals img");
  buyNowCanvas.width = buyNowImg.width;
  buyNowCanvas.height = buyNowImg.height;

  buyNowCanvasRender = () => {
    if (buyNowSeq.frame > buyNowFrameCount) return;
    const image = buyNowSeqImages[buyNowSeq.frame];
    buyNowCanvasContext.clearRect(
      0,
      0,
      buyNowCanvas.width,
      buyNowCanvas.height
    );
    const imgRatio = image.height / image.width;
    const h = buyNowImg.width * imgRatio;
    buyNowCanvasContext.imageSmoothingEnabled = false;
    buyNowCanvasContext.drawImage(
      image,
      0,
      (buyNowImg.height - h) / 2,
      buyNowImg.width,
      h
    );
  };

  gsap.to(buyNowSeq, {
    frame: buyNowFrameCount - 1,
    snap: "frame",
    onUpdate: buyNowCanvasRender,
    duration: 3,
    delay: 0.5,
    scrollTrigger: {
      trigger: ".deals",
      toggleActions: "play none none reverse",
    },
  });
};