import "./index.sass"

import $ from "jquery"

$(window).scroll(function () {
    $(".navbar").toggleClass("__home_navbar", $(this).scrollTop() > 0);
});