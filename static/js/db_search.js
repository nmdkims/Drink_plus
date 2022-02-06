function getParameter(strParamName) {
    var arrResult = null;
    if (strParamName) {
        arrResult = location.search.match(new RegExp("[&?]" + strParamName + "=(.*?)(&|$)"));
        return arrResult && arrResult[1] ? arrResult[1] : null;
    }
}

var p_name = getParameter("q");
// alert('p_name은 : ' + p_name);
var parasearch_input = decodeURIComponent(p_name);
// alert('parasearch는 : ' + parasearch_input);

// $('input[name=q]').attr('value', 1);
// $('input[name=q]').attr('value', parasearch_input);


$(document).ready(function () {
    // if (parasearch_input == null) {
    //     $('input[name=q]').attr('value', '');
    //      alert('화면이 변화할때 입력 값이 없을때 : ' +  parasearch_input );
    // } else {
    //     $('input[name=q]').attr('value', parasearch_input);
    //      alert('화면이 변화할때 입력 값이 있을때  : ' +  parasearch_input );
    //      alert('화면이 변화할때 입력 값이 있을때  : ' + ('input[name=q]').attr('value', parasearch_input));
    // }
    db_search()
});

function db_search() {

    let input = parasearch_input
    $('#search-box').empty()
    $.ajax({
        type: "POST",
        url: "/api/search",
        data: {input_give: input},
        success: function (response) {
            console.log(response)
            let insta_searchs = response['insta_search']
            let count = insta_searchs.length

            // alert('p_name은 : ' + count);


            let first_temp = ` <div id="search-container">
                <div class="search-wrapper">
                    <div class="search-word" id="search-word_id">
                        <h1><b>#${input}</b></h1>
                    </div>
                    <div class="search-set">
                        <ul class="search-info">
                            <li class="search-post">
                                <a class="search-post" id="search-post_count" href="url" tabindex="0">
                                    게시물
                                    <span class="search-post">${count}</span>
                                </a>
                                </span>
                            </li>
                        </ul>
                    </div>

                </div>
            </div>
            <hr>

            <div id="photo-container">
            </div>
            `

            $('#main-container').append(first_temp)


            for (let i = 0; i < insta_searchs.length + 1; i++) {
                if (count - i >= 3) {
                    let img1 = insta_searchs[i]['img']
                    let img2 = insta_searchs[i + 1]['img']
                    let img3 = insta_searchs[i + 2]['img']
                    let temp_html = `
                    <div class="card">
                        <div class="photo-wrapper" id="photo-wrapper_id">     
                    
                            <div class="photoset">
                                <img src="${img1}">
                            </div>  
                             <div class="photoset">
                                <img src="${img2}">
                            </div>    
                             <div class="photoset">
                                <img src="${img3}">
                            </div>                                             
                                                                                                      
                         </div>
                    </div> 
                    `
                    i = i + 2
                    $('#photo-container').append(temp_html)

                } else if (count - i == 2) {

                    let img1 = insta_searchs[i]['img']
                    let img2 = insta_searchs[i + 1]['img']

                    let temp_html = `
                    <div class="photoset">
                        <img src="${img1}">
                    </div>
                    <div class="photoset">
                        <img src="${img2}">
                    </div>
                    `

                    i = i + 1
                    $('#photo-container').append(temp_html)
                } else if (count - i == 1) {
                    let img1 = insta_searchs[i]['img']
                    let temp_html = `
                    <div class="photoset">
                        <img src="${img1}">
                    </div>                     
                   `

                    i = i
                    $('#photo-container').append(temp_html)
                }
            }
        }
    })
}

