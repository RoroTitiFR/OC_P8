import "./index.scss"

import $ from "jquery"

$(window).scroll(function () {
    $(".navbar").toggleClass("__home_dark_navbar", $(this).scrollTop() > 0);
});