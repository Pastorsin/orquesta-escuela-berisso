$(document).ready(function(){
    $('#workshop-input option[value=""]').prop('selected',true);

    $('#workshop-input').on('change', function(){
        //Esconder mensaje de error
        $('#input-error').css('display','none');

        //Parsear URL con nuevo taller
        let registerUrl = $('#register-url');
        let currentUrl = registerUrl.prop('href');
        let index = currentUrl.lastIndexOf('/');
        let newUrl = currentUrl.substring(0,index+1);
        newUrl = newUrl.concat($(this).val());
        $('#register-url').prop('href',newUrl);
    })

    $('#register-url').on('click', function(e){
        //Si no se seleccionó ningún valor, muestro mensaje de error
        if($('#workshop-input').val()==''){
            e.preventDefault();
            $('#workshop-input').focus();
            $('#input-error').css('display','inline-block');
            return false;
        }
        return true;
    })
})