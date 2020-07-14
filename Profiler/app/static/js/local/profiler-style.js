/**
 * Created by amendrashrestha on 2020-07-14.
 */
$(document).ready(function () {
    // this will get the full URL at the address bar
    var url = window.location.href;

    // passes on every "a" tag
    $(".main-sidebar  a").each(function () {
        // checks if its the same on the address bar
        if (url == (this.href)) {
            $(this).closest("li").addClass("active");
            //for making parent of submenu active
            $(this).closest("li").parent().parent().addClass("active");
        }
    });

    $('#btn-profiler').click(function (e) {
        var dict_user_inputs = {};
        var text_input;

        text_input = document.getElementsByName("txt-user-input")[0].value;
        dict_user_inputs['text'] = text_input

        var form_data = new FormData();
        form_data.append("file", document.getElementById('file-selector').files[0]);

        form_data.append("user-choices", JSON.stringify(dict_user_inputs))

        $.ajax({
            type: 'POST',
            url: 'analysis',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function (response) {
                window.location.href = "topic";
            }
        });
    });

});