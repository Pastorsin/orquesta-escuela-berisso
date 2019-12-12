let globalUrl;
let currentWorkshopId;

$(document).ready(function(){
    $('#workshop-select option[value=""]').prop('selected',true);

    $('#workshop-select').on('change', function(){
        //Parsear URL con nuevo taller
        currentWorkshopId = $(this).val();
        let currentUrl = baseUrl;
        let index = currentUrl.lastIndexOf('/');
        let newUrl = currentUrl.substring(0,index+1);
        newUrl = newUrl.concat($(this).val()+'/');
        globalUrl = newUrl;

        console.log(globalUrl);
        //Mostrar sección de fechas previo render
        getNucleus(currentSchoolYearId,$(this).val());
    })

    $('body').on('change','.nucleus-select', function(){
        //Parsear URL con nuevo taller
        let currentUrl = globalUrl;
        let index = currentUrl.lastIndexOf('/');
        let newUrl = currentUrl.substring(0,index+1);
        newUrl = newUrl.concat($(this).val());
        globalUrl = newUrl;
        console.log(globalUrl);
        //Mostrar sección de fechas previo render
        getDates(currentSchoolYearId,currentWorkshopId,$(this).val());
    })
})

function getDates(schoolYearId, workshopId, nucleusId) {
    $.ajax({
        type: "GET",
        url: '/api/fechas/'+schoolYearId+'/'+workshopId+'/'+nucleusId,
        dataType: "json",
        success: function(data) {
            showDates(data);
        }
    });
}

function getNucleus(schoolYearId, workshopId) {
    $.ajax({
        type: "GET",
        url: '/api/nucleos/'+schoolYearId+'/'+workshopId,
        dataType: "json",
        success: function(data) {
            showNucleus(data);
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
            let dateCard = '<a class="date-card '+(date.fecha==currentDate ? 'date-today' : '')+' nostyle" href="'+globalUrl.concat('/'+date.fecha)+'">';
            dateCard += '<strong>'+date.dia+'</strong>';
            dateCard += date.fecha;
            dateCard += '</a>'
            $('#dates-container').append(dateCard);
        })
    }else{
        showEmptyDatesError();
    }
}

function showNucleus(nucleus) {
    //Vacio el container
    $('#dates-container').empty();
    $('#date-label').css('display','none');
    $('#nucleus-container').empty();
    if(nucleus.length!=0){
        hideEmptyNucleusError();
        let selectContent = '<select class="nucleus-select form-control">';
        //Opcion default
        selectContent += '<option value="" hidden selected="selected"></option>';
        nucleus.forEach(nucleu => {
            //Creo date card y le hago un append al container
            selectContent += '<option value="'+nucleu.id+'">'+nucleu.name+'</option>';
        })
        selectContent += '</select>'
        $('#nucleus-container').append(selectContent);
        //Seleccionar opcion default vacía
        $('.nucleus-select option[value=""]').prop('selected',true);
        //Mostrar segundo label
        $('#nucleus-label').css('display','inline-block');
    }else{
        showEmptyNucleusError();
    }
}

function showEmptyDatesError() {
    $('#date-label').css('display','none');
    $('#date-error').css('display','inline');
}

function showEmptyNucleusError() {
    $('#nucleus-label').css('display','none');
    $('#nucleus-error').css('display','inline');
}

function hideEmptyDatesError() {
    $('#date-label').css('display','inline');
    $('#date-error').css('display','none');
}

function hideEmptyNucleusError() {
    $('#nucleus-label').css('display','inline');
    $('#nucleus-error').css('display','none');
}