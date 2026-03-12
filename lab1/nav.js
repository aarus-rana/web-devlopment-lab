document.addEventListener("DOMContentLoaded", function () {
  var toggle = document.querySelector(".toggle");
  var links = document.querySelector(".links");

  if (!toggle || !links) return;

  toggle.addEventListener("click", function () {
    links.classList.toggle("show");
  });
});

