class MultipleStepForm {

    constructor() {
        this.initEvents()
        this.navigateTo(0);
        this.initSections();
    }

    initEvents() {
        $('form').submit(this.submitForm.bind(this));
        $('.buttons .previous').click(this.previous.bind(this));
        $('.buttons .next').click(this.next.bind(this));
    }

    submitForm(event) {
        event.preventDefault();

        $('form').parsley().whenValidate({
            group: 'block-' + this.curIndex()
        }).done(this.ajax.bind(this));
    }

    ajax() {
        $.ajax({
            type: "POST",
            url: $('form').attr('action').trim(),
            data: JSON.stringify(this.formData()),
            contentType: "application/json",
            dataType: "json",
            success: this.successAjax
        });
    }

    successAjax(data) {
        let success = data[0]['success']
        let messagesHTML = data[1]['messages']

        if (success) {
            window.location.href = "/estudiantes"
        } else {
            $('.messages').empty().append(messagesHTML)
        }
    }

    formData() {
        let data = {}

        data['student'] = this.serializeStudent()
        data['responsable'] = {}
        data['responsable']['created'] = this.serializeResponsablesCreated()
        data['responsable']['checked'] = this.serializeResponsablesChecked()
        return data
    }

    serializeStudent() {
        let student = $(".student :input")
        return this.serialize(student)

    }

    serializeResponsablesCreated() {
        let responsables = Array.from($(".form-section.responsable"))
        return responsables.map((responsable) =>
            this.serialize($(responsable).find(':input'))
        )
    }

    serializeResponsablesChecked() {
        let responsablesChecked = Array.from($(".responsable-checkbox:checkbox:checked"))
        return responsablesChecked.map(
            (responsable) => $(responsable).val()
        )
    }

    serialize(selector) {
        let result = {}
        let json = selector.serializeArray()
        json.forEach((item) => result[item.name] = item.value)
        return result
    }

    navigateTo(index) {
        this.refreshCurrentClass(index)
        this.showButtons(index)
        this.addNewResponsable(index)
    }

    refreshCurrentClass(index) {
        $('.form-section')
            .removeClass('current')
            .eq(index)
            .addClass('current');
    }

    showButtons(index) {
        $('.buttons .previous').toggle(index > 0);
        $('.buttons [type=submit]').toggle(this.atTheEnd(index));
    }

    atTheEnd(index) {
        return index == this.lastIndex();
    }

    addNewResponsable(index) {
        if (this.atTheEnd(index)) {
            $('.buttons .next').text('Agregar otro tutor')
        } else {
            $('.buttons .next').text('Siguiente >')
        }
    }

    curIndex() {
        return $('.form-section').index($('.form-section').filter('.current'));
    }

    lastIndex() {
        return $('.form-section').length - 1
    }

    createResponsableSection() {
        let responsableHTML = $('.responsable:first').clone()
        this.convertSection(responsableHTML)
        this.clearInputs(responsableHTML)
        return responsableHTML
    }

    convertSection(responsableHTML) {
        responsableHTML.removeClass('d-none');
        responsableHTML.addClass('form-section');
    }

    clearInputs(responsable) {
        let nextIndex = this.curIndex() + 1
        let inputs = responsable.find(':input')
        inputs.val('')
        inputs.removeClass('parsley-success')
        inputs.attr('data-parsley-group', 'block-' + nextIndex);
    }

    previous() {
        this.navigateTo(this.curIndex() - 1);
    }

    next() {
        $('form').parsley().whenValidate({
            group: 'block-' + this.curIndex()
        }).done(() => {
            if (this.curIndex() == this.lastIndex()) {
                let responsableSection = this.createResponsableSection()
                responsableSection.insertBefore($(".buttons"));
            }
            this.navigateTo(this.curIndex() + 1);
        });
    }

    initSections() {
        // Prepare sections by setting the `data-parsley-group` attribute to 'block-0', 'block-1', etc.
        $('.form-section').each(function(index, section) {
            $(section).find(':input').attr('data-parsley-group', 'block-' + index);
        });
    }

}

$(document).ready(() => {
    const form = new MultipleStepForm();
});