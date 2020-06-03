$(document).ready(() => {
	const filters = []
    const search = null;
});

window.onload = function () {
    const app = new Vue({
        el: '#app',
        delimiters: ['[[',']]'],
        data: {
            instruments: [],
            instrumentStateFilter: 'all',
            instrumentNameFilter: '',
            currentPage: 1,
            elementsPerPage: document.getElementById('pagination').dataset.pagination,
        },
        mounted() {
            this.getInstruments();
        },
        computed: {
            pagedInstruments() {
                return this.getFilteredInstruments().slice(
                    (this.currentPage - 1) * this.elementsPerPage,
                    this.currentPage * this.elementsPerPage
                );
            },
            maxPages() {
                return Math.ceil(this.getFilteredInstruments().length / this.elementsPerPage);
            }
        },
        watch: {
            //No se que conviene, devolverlos a la primer página o fijarse si se puede quedar en la página actual
            //Tal vez al modificar los instrumentos si quedarse, pero al modificar el filtro volver
            instrumentStateFilter(value) {
                this.currentPage = 1;
            },
            instrumentNameFilter(value) {
                this.currentPage = 1;
            },
            instruments() {
                this.currentPage = this.maxPages >= this.currentPage ? this.currentPage : 1;
                //this.currentPage = 1;
            }
        },
        methods: {
            getInstruments() {
                fetch('/api/instrumentos')
                    .then(response => {
                        return response.json();
                    })
                    .then(response => {
                        this.instruments = response;
                        console.log(this.instruments);
                    })
            },
            getFilteredInstruments() {
                return this.instruments.filter(instrument => {
                    return instrument.name.includes(this.instrumentNameFilter.trim()) &&
                        (this.instrumentStateFilter != 'all' ? instrument.is_active == this.instrumentStateFilter : true);
                })
            },
            switchInstrumentStatus(instrumentId) {
                fetch('/api/instrumentos/' + instrumentId + '/estado', {
                    method: 'PATCH'
                })
                    .then(() => {
                        this.getInstruments();
                    })
            },
            clearInstrumentNameFilter() {
                this.instrumentNameFilter = '';
            },
            goToPage(pageNumber) {
                this.currentPage = pageNumber;
            },
            goToNextPage() {
                this.currentPage++;
            },
            goToPreviousPage() {
                this.currentPage--;
            }
        },
    })
}