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
                image: []
            },
            instrumentTypes: []
        },
        watch: {
            'instrument.name': function() {
                this.errors.name = [];
            },
            'instrument.type': function() {
                this.errors.name = [];
            },
            'instrument.code': function() {
                this.errors.name = [];
            },
            'instrument.image': function(newVal) {
                this.errors.image = [];
            }
        },
        mounted() {
            this.getInstrumentTypes();
        },
        methods: {
            getInstrumentTypes() {
                const types = [
                    {id: 1, name: 'Viento'},
                    {id: 2, name: 'Cuerda'},
                    {id: 3, name: 'Percusión'}
                ];
                this.instrumentTypes = types;
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
                if (!this.validateForm()) {
                    return false;
                }
                fetch('/api/instrumentos/', {
                    method: 'POST',
                    body: {
                        instrument: {
                            name: this.instrument.name,
                            category_id: this.instrument.type,
                            inventory_number: this.instrument.code
                        }
                    }
                })
                    .then(response => {
                        console.log(response);
                    })
                return false;
                //Hacer petición, agregar errores si es que aparecen, limpiar formulario y mostrar cartel
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
                }
            },
            validateInstrumentImage() {
                if (!this.instrument.image) {
                    this.errors.image.push('Por favor, agregue una imagen para el instrumento.');
                }
            },
            cleanErrors() {
                this.errors.name = [];
                this.errors.type = [];
                this.errors.code = [];
                this.errors.image = [];
            },
            hasErrors() {
                if (!this.errors.name.length || this.errors.type.length ||
                    this.errors.code.length || this.errors.image.length) {
                    return true;
                }
                return false;
            },
            setNewImage() {
                this.instrument.image = this.$refs.instrumentImage.files[0];
            }
        },

    })
}