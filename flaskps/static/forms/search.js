/* Abstract Class */
class Search {

    constructor(pager) {
        this.pager = pager
        this.initSelectors()
        this.initEvents()
        this.start()
    }

    initSelectors() {
        this.searchInput = document.querySelector("#search")
        this.rowsSelector = document.querySelectorAll(".user-row")
        this.searchButton = document.querySelector("#search-button")
        this.resultText = document.querySelector("#result")
    }

    initEvents() {
        this.searchInput.addEventListener("keyup", this.start.bind(this))
        this.searchButton.addEventListener("clickup", this.start.bind(this))
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

    /* Abstract Method */
    satisfy(row, value) {
        throw new Error('Satisfy abstract method is not implemented');
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