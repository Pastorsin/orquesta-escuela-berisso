class Pager {

    constructor(elementsPerPage) {
        this.elementsPerPage = elementsPerPage
    }

    paginate(rows) {
        let pages = this.distributePages(rows);
        let totalPages = pages.length;
        this.build(pages);
        this.render(totalPages);
    }

    distributePages(anArray) {
        let results = [];
        let chunk_size = this.elementsPerPage;

        while (anArray.length) {
            results.push(anArray.splice(0, chunk_size));
        }

        return results;
    }

    build(pages) {
        pages.forEach((rows, index) => {
            let pageContainer = document.createElement("tbody");
            pageContainer.classList.add("page");
            pageContainer.id = "page" + (index + 1)
            rows.forEach((row) => pageContainer.append(row))            
            $("table").append(pageContainer);
        })
    }

    render(pages) {
        $('#pagination-demo').twbsPagination('destroy');
        $('#pagination-demo').twbsPagination({
            totalPages: pages,
            // the current page that show on start
            startPage: 1,

            // maximum visible pages
            visiblePages: 5,

            initiateStartPageClick: true,

            // template for pagination links
            href: false,

            // variable name in href template for page number
            hrefVariable: '{{number}}',

            // Text labels
            first: '',
            prev: '<',
            next: '>',
            last: '',

            // carousel-style pagination
            loop: false,

            // callback function
            onPageClick: function(event, page) {
                $('.page-active').removeClass('page-active');
                $('#page' + page).addClass('page-active');
            },

        });
    }

    clear() {
        $('tbody > *').unwrap()
    }
}