import axios from "./axios";

$(document).ready(function () {
    const openModalDetails = $(".__open-modal-details");
    const modalDetails = $(".__modal-details");
    const modalTitle = $(".modal-card-title");
    const loadingDetails = $(".__loading-details > .lds-ellipsis");
    const openOpenFoodFactsLink = $(".modal-card-foot > a");
    const placeholderDetails = $(".__placeholder-details");
    const saveSubstitute = $(".__save-substitute");

    openModalDetails.click(function () {
        const productCode = $(this).attr("data-code");
        const productName = $(this).attr("data-name");

        modalTitle.text(productName);
        loadingDetails.css("display", "block");
        placeholderDetails.html(null);
        openOpenFoodFactsLink.attr("href", `https://fr.openfoodfacts.org/produit/${productCode}`);

        modalDetails.toggleClass("is-active");

        axios
            .get(`/details/${productCode}`)
            .then(function (response) {
                placeholderDetails.html(response.data)
            })
            .catch(function (error) {
                placeholderDetails.html(
                    '<div class="notification is-danger">' +
                    "Impossible de charger les données depuis le serveur." +
                    "</div>"
                )
            })
            .finally(function () {
                loadingDetails.css("display", "none")
            })
    });

    saveSubstitute.click(function () {
        const productCode = $(this).attr("data-product");
        const substituteCode = $(this).attr("data-substitute");

        $(this).toggleClass("is-loading");

        const formData = new FormData();
        formData.set("product_code", productCode);
        formData.set("substitute_code", substituteCode);

        const that = this;

        axios
            .post("", formData)
            .then(function (response) {
                $(that).replaceWith(response.data);
            })
            .catch(function (error) {
                console.log(error)
            })
            .finally(function () {
            })
    })
});