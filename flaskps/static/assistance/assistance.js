let globalUrl;

$(document).ready(function(){
    $('#workshop-input option[value=""]').prop('selected',true);

    $('#workshop-input').on('change', function(){
        //Esconder mensaje de error
        $('#input-error').css('display','none');
        //Mostrar segundo label
        $('#date-label').css('display','inline-block');

        //Parsear URL con nuevo taller
        let currentUrl = baseUrl;
        let index = currentUrl.lastIndexOf('/');
        let newUrl = currentUrl.substring(0,index+1);
        newUrl = newUrl.concat($(this).val());
        globalUrl = newUrl;

        //Mostrar sección de fechas previo render
        getDates(currentSchoolYearId,$(this).val());
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

function getDates(schoolYearId, workshopId) {
    $.ajax({
        type: "GET",
        url: '/api/fechas/'+schoolYearId+'/'+workshopId,
        dataType: "json",
        success: function(data) {
            showDates(data);
        }
    });
}

function showDates(dates) {
    //Vacio el container
    $('#dates-container').empty();
    if(dates.length!=0){
        hideEmptyDatesError();
        dates.forEach(date => {
            //Creo date card y le hago un append al container
            let dateCard = '<a class="date-card nostyle" href="'+globalUrl.concat('/'+date.fecha)+'">';
            dateCard += '<strong>'+date.dia+'</strong>';
            dateCard += date.fecha;
            dateCard += '</a>'
            $('#dates-container').append(dateCard);
        })
    }else{
        showEmptyDatesError();
    }
}

function showEmptyDatesError() {
    $('#date-label').css('display','none');
    $('#date-error').css('display','inline');
}

function hideEmptyDatesError() {
    $('#date-label').css('display','inline');
    $('#date-error').css('display','none');
}