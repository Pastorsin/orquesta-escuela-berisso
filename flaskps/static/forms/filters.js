class Filter {

    /* Hook method - Optional */
    initEvents(search) {
        /* Define the events that trigger the search */
    }

    /* Abstract method */
    satisfy(row, value) {
        throw new Error('Satisfy method is not implemented');
    }
}

class ActiveFilter extends Filter {

    constructor() {
        super()
        this.initSelectors()
    }

    initSelectors() {
        this.activeButton = $("#active-checkbox")
        this.deactiveButton = $("#inactive-checkbox")
        this.allButton = $("#all-checkbox")
    }

    initEvents(search) {
        this.activeButton.change(search.start.bind(search))
        this.deactiveButton.change(search.start.bind(search))
        this.allButton.change(search.start.bind(search))
    }

    satisfy(row, value) {
        if (this.thereButtonsChecked()) {
        	let columnIsActive = this.columnIsActive(row)
            return this.activeButtonChecked() ? columnIsActive : !columnIsActive
        } else {
            return true
        }
    }

    thereButtonsChecked() {
        return this.activeButtonChecked() || this.deactiveButtonChecked()
    }

    activeButtonChecked() {
        return this.activeButton.is(":checked")
    }

    deactiveButtonChecked() {
        return this.deactiveButton.is(":checked")
    }

    columnIsActive(row) {
        const selector = row.querySelector(".td-active")
        const isActive = Boolean(Number(selector.getAttribute("active")))
        return isActive
    }

}