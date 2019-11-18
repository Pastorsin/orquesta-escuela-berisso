/* Abstract Class */
class Search {

    constructor(filters) {
        this.pager = new Pager();
        this.filters = filters
        this.initSelectors()
        this.initEvents()
        this.start()
    }

    initSelectors() {
        this.searchInput = document.querySelector("#search")
        this.rowsSelector = document.querySelectorAll(".item-row")
        this.searchButton = document.querySelector("#search-button")
        this.resultText = document.querySelector("#result")
    }

    initEvents() {
        this.searchInput.addEventListener("keyup", this.start.bind(this))
        this.searchButton.addEventListener("clickup", this.start.bind(this))
        this.filters.forEach((filter) => filter.initEvents(this))
    }

    start() {
        this.hideRows()
        let rows = this.search()
        this.showResult(rows)
        this.showRows(rows)
    }

    hideRows() {
        this.pager.clear()
        this.rowsSelector.forEach((row) => row.style.display = 'none')
    }

    search() {
        let value = this.searchInput.value.trim().toLowerCase()
        let rows = Array.from(this.rowsSelector)
        return rows.filter((row) => this.satisfy(row, value))
    }

    satisfy(row, value) {
        return this.satisfyText(row, value) && this.satisfyFilters(row, value)
    }

    /* Abstract Method */
    satisfyText(row, value) {
        throw new Error('SatisfyText method is not implemented');
    }

    satisfyFilters(row, value) {
        return this.filters.every((filter) => filter.satisfy(row, value))
    }

    showRows(rows) {
        rows.forEach((row) => row.style.display = '');
        this.pager.paginate(rows);
    }

    showResult(rows) {
        let text = rows.length + " " + "resultados."
        this.resultText.textContent = text
    }
}