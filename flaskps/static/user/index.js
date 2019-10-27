$(document).ready(() => {
    const elementsPerPage = Number($("meta[name='elements']").attr("content"));
    const totalPages = $(".user-row").length
    const pager = new Pager(elementsPerPage);
    const search = new Search(pager);
});