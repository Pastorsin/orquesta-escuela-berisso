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
        this.activeCheckbox = document.querySelector("#active-checkbox")
        this.inactiveCheckbox = document.querySelector("#inactive-checkbox")
        this.resultText = document.querySelector("#result")
    }

    initEvents() {
        this.searchInput.addEventListener("keyup", this.start.bind(this))
        this.searchButton.addEventListener("clickup", this.start.bind(this))
        this.activeCheckbox.addEventListener("change", this.start.bind(this))
        this.inactiveCheckbox.addEventListener("change", this.start.bind(this))
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
        return this.includesUsername(row, value) && this.satisfyFilter(row, value)
    }

    includesUsername(row, value) {
        let selector = row.querySelector(".username")
        let username = selector.textContent.toLowerCase()
        return username.includes(value)
    }

    satisfyFilter(row, value) {
        let filteringActiveUsers = $("#active-checkbox").is(":checked")
        let filteringInactiveUsers = $("#inactive-checkbox").is(":checked")
        if (!(filteringActiveUsers || filteringInactiveUsers)) {
            return true
        } else if(filteringActiveUsers){
            let selector = row.querySelector(".user-active")
            let userActive = selector.getAttribute("active")
            return Boolean(Number(userActive))
        } else if(filteringInactiveUsers){
            let selector = row.querySelector(".user-active")
            let userActive = selector.getAttribute("active")
            return !Boolean(Number(userActive))
        }
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