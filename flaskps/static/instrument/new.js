window.onload = function() {
    const app = new Vue({
        el: '#app',
        delimiters: ['[[',']]'],
        data: {
            instrument: {
                name: '',
                type: '',
                code: '',
                image: null
            },
            errors: {
                name: [],
                type: [],
                code: [],
                image: [],
                general: []
            },
            successMessages: [],
            instrumentTypes: [],
            allowedImageExtensions: [
                'image/jpeg',
                'image/jpg',
                'image/png',
                'image/bpm',
            ],
            sendingForm: false
        },
        watch: {
            'instrument.name': function() {
                this.errors.name = [];
            },
            'instrument.type': function() {
                this.errors.type = [];
            },
            'instrument.code': function() {
                this.errors.code = [];
            },
            'instrument.image': function() {
                this.errors.image = [];
            }
        },
        mounted() {
            this.getInstrumentTypes();
        },
        methods: {
            getInstrumentTypes() {
                fetch('/api/instrumentos/tipos')
                    .then(response => {
                        return response.json();
                    })
                    .then(response => {
                        this.instrumentTypes = response;
                    })
            },
            validateForm() {
                this.cleanErrors();
                this.validateInstrumentName();
                this.validateInstrumentType();
                this.validateInstrumentCode();
                this.validateInstrumentImage();
                return this.hasErrors();
            },
            submitNewInstrument() {
                if (this.validateForm()) {
                    return false;
                }
                this.sendingForm = true;
                fetch('/api/instrumentos/', {
                    method: 'POST',
                    body: new FormData(this.$refs.form)
                })
                    .then(response => {
                        return response.json();
                    })
                    .then(json => {
                        if (!json.success) {
                            this.clearGeneralErrors();
                            this.errors.general = json.messages;
                        } else {
                            this.clearForm();
                            this.successMessages = json.messages;
                        }
                        this.sendingForm = false;
                    })
                return false;
            },
            validateInstrumentName() {
                if (!this.instrument.name) {
                    this.errors.name.push('Por favor, especifique un nombre para el instrumento.');
                }
            },
            validateInstrumentType() {
                if (!this.instrument.type) {
                    this.errors.type.push('Por favor, especifique un tipo para el instrumento.');
                }
            },
            validateInstrumentCode() {
                if (!this.instrument.code) {
                    this.errors.code.push('Por favor, especifique un código para el instrumento.');
                } else if (!parseInt(this.instrument.code)) {
                    this.errors.code.push('Por favor, especifique un código numérico.');
                }
            },
            validateInstrumentImage() {
                if (!this.instrument.image) {
                    this.errors.image.push('Por favor, agregue una imagen para el instrumento.');
                } else if (!this.allowedImageExtensions.includes(this.instrument.image.type)) {
                    this.errors.image.push('Por favor, agregue una imagen con extensión válida.');
                }
            },
            cleanErrors() {
                this.errors.name = [];
                this.errors.type = [];
                this.errors.code = [];
                this.errors.image = [];
                this.clearGeneralErrors();
            },
            hasErrors() {
                if (this.errors.name.length || this.errors.type.length || this.errors.code.length || this.errors.image.length) {
                    return true;
                }
                return false;
            },
            setNewImage() {
                this.instrument.image = this.$refs.instrumentImage.files[0];
            },
            clearForm() {
                this.instrument = {};
                this.$refs.instrumentImage.value = '';
                this.$refs.instrumentImageLabel.innerText = 'Elegir archivo';
            },
            clearGeneralErrors() {
                this.errors.general = [];
                this.successMessages = [];
            },
        },

    })
}