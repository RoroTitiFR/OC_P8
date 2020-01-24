$(document).ready(function () {
    const openModalConfirm = $(".__open-modal-confirm");
    const modalConfirm = $(".__modal-confirm");
    const confirmDelete = $(".__confirm-delete");
    const cancelDelete = $(".__cancel-delete");

    openModalConfirm.click(function () {
        const id = $(this).attr("data-id");
        $("input[name=product_substitute_id]").attr("value", id);

        modalConfirm.toggleClass("is-active")
    });

    confirmDelete.click(function () {
        confirmDelete.toggleClass("is-loading")
    });

    cancelDelete.click(function () {
        modalConfirm.toggleClass("is-active")
    })
});