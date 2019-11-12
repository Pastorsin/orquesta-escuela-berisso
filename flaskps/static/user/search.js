class UserSearch extends Search {

    initEvents() {
        super.initEvents()
        this.activeCheckbox.addEventListener("change", this.start.bind(this))
        this.inactiveCheckbox.addEventListener("change", this.start.bind(this))
    }

    initSelectors() {
        super.initSelectors()
        this.activeCheckbox = document.querySelector("#active-checkbox")
        this.inactiveCheckbox = document.querySelector("#inactive-checkbox")
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
        } else if (filteringActiveUsers) {
            let selector = row.querySelector(".user-active")
            let userActive = selector.getAttribute("active")
            return Boolean(Number(userActive))
        } else if (filteringInactiveUsers) {
            let selector = row.querySelector(".user-active")
            let userActive = selector.getAttribute("active")
            return !Boolean(Number(userActive))
        }
    }
}