function index_search() {
    let input_main = $('#input_search').val()
    window.location.href = '/search?q=' + input_main
}

function enterkey() {
    if (window.event.keyCode == 13) {
        let input_main = $('#input_search').val()
        window.location.href = '/search?q=' + input_main
    }
}