$(onLoad)

function onLoad() {
    $('.ui.search')
        .search({
            apiSettings: {
                url: '/search/{query}/'
            },
            type: 'category',
            searchFields: [
                'title',
                'url'
            ]
        })
}



