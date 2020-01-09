import "../scss/bulma.scss"
import "../scss/tailwind.scss"
import "../scss/animate.scss"

import $ from "jquery"

$(window).scroll(function () {
    const navbar = $(".navbar");
    navbar.toggleClass("__home_dark_navbar shadow-xl", $(this).scrollTop() > 0);
});

$(document).ready(function () {
    const navbar = $(".navbar");
    const navbarMenu = $(".navbar-menu");
    const navbarBurger = $(".navbar-burger");

    // Check for click events on the navbar burger icon
    navbarBurger.click(function () {
        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        navbarBurger.toggleClass("is-active");
        navbarMenu.toggleClass("is-active");

        if ($(window).scrollTop() === 0) {
            navbar.toggleClass("__home_dark_navbar")
        }
    });
});