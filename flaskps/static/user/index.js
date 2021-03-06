$(document).ready(() => {
    const filters = [new ActiveFilter()]
    const search = new UserSearch(filters);

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