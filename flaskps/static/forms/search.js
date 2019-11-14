/* Abstract Class */
class Search {

    constructor(pager) {
        this.pager = new Pager();
        this.initSelectors()
        this.initEvents()
        this.initFilters()
        this.start()
    }

    initSelectors() {
        this.searchInput = document.querySelector("#search")
        this.rowsSelector = document.querySelectorAll(".item-row")
        this.searchButton = document.querySelector("#search-button")
        this.resultText = document.querySelector("#result")
        this.activeButton = document.querySelector("#active-checkbox")
        this.deactiveButton = document.querySelector("#inactive-checkbox")
    }

    initEvents() {
        this.searchInput.addEventListener("keyup", this.start.bind(this))
        this.searchButton.addEventListener("clickup", this.start.bind(this))
        this.activeButton.addEventListener("change", this.start.bind(this))
        this.deactiveButton.addEventListener("change", this.start.bind(this))
    }

    initFilters() {
        this.filters = [new ActiveFilter()]
    }

    addFilter(aFilter) {
        this.filters.push(aFilter)
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