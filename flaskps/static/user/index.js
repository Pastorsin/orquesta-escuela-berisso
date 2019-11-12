$(document).ready(() => {
    const elementsPerPage = Number($("meta[name='elements']").attr("content"));
    const totalPages = $(".user-row").length
    const pager = new Pager(elementsPerPage);
    const search = new UserSearch(pager);

    $('.deactivate').on('click', function(){
        let surname=$(this).parents('td').siblings('.surname').text();
        let name=$(this).parents('td').siblings('.name').text();
        return confirm('¿Está seguro que desea deshabilitar el usuario correspondiente a '+surname+', '+name+'?');
    })

    $('.activate').on('click', function(){
        let surname=$(this).parents('td').siblings('.surname').text();
        let name=$(this).parents('td').siblings('.name').text();
        return confirm('¿Está seguro que desea habilitar el usuario correspondiente a '+surname+', '+name+'?');
    })
});