// Optional photo viewer for the gallery. Without it, each tile links to the full image.
(function () {
  var viewer = document.querySelector(".photo-viewer");
  if (!viewer || typeof viewer.showModal !== "function") return;
  var img = viewer.querySelector("img");

  document.querySelectorAll(".gallery a").forEach(function (link) {
    link.addEventListener("click", function (event) {
      event.preventDefault();
      var thumb = link.querySelector("img");
      img.src = link.href;
      img.alt = thumb ? thumb.alt : "";
      viewer.showModal();
    });
  });

  // A click on the backdrop (outside the photo) closes the viewer.
  viewer.addEventListener("click", function (event) {
    if (event.target === viewer) viewer.close();
  });

  viewer.addEventListener("close", function () {
    img.removeAttribute("src");
  });
})();
