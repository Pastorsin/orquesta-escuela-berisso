class Filter {

    /* Abstract method*/
    satisfy(row, value) {
        throw new Error('Satisfy method is not implemented');
    }
}

class ActiveFilter extends Filter {

    constructor() {
        this.initSelectors()
    }

    initSelectors() {
        this.activeButton = $("#active-checkbox")
        this.deactiveButton = $("#inactive-checkbox")
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