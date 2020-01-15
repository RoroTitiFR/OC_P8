import $ from "jquery"

$(window).on("scroll resize", function () {
    const navbar = $(".navbar");
    const navbarMenu = $(".navbar-menu");
    const navbarBurger = $(".navbar-burger");

    navbar.toggleClass("__home_dark_navbar shadow-xl", $(this).scrollTop() > 0);

    if (navbarBurger.hasClass("is-active")) {
        navbarBurger.toggleClass("is-active");
        navbarMenu.toggleClass("is-active");
    }
});

$(document).ready(function () {
    const navbar = $(".navbar");
    const navbarMenu = $(".navbar-menu");
    const navbarBurger = $(".navbar-burger");
    const notification = $(".notification");
    const notificationDelete = $(".notification .delete");

    // Check for click events on the navbar burger icon
    navbarBurger.click(function () {
        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        navbarBurger.toggleClass("is-active");
        navbarMenu.toggleClass("is-active");

        if ($(window).scrollTop() === 0) {
            navbar.toggleClass("__home_dark_navbar")
        }
    });

    notificationDelete.click(function () {
        $(this).parent().remove()
    })
});