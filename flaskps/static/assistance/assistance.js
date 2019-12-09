$(document).ready(function(){
    $('#workshop-input').on('change',function(){
        let registerUrl = $('#register-url');
        let currentUrl = registerUrl.prop('href');
        let index = currentUrl.lastIndexOf('/');
        let newUrl = currentUrl[index]=$(this).val();
        registerUrl.prop('href',newUrl);
        console.log(registerUrl.prop('href'));
    })
})