class UserSearch extends Search {

    satisfyText(row, value) {
        let selector = row.querySelector(".username")
        let username = selector.textContent.toLowerCase()
        return username.includes(value)
    }
}