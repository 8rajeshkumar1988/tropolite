document.addEventListener("DOMContentLoaded", function () {
    const popupLinks = document.querySelectorAll(".popup-link");

    popupLinks.forEach((link) => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            const imageUrl = this.getAttribute("data-image-url");
            window.open(imageUrl, "Image Popup", "width=600,height=400");
        });
    });
});
