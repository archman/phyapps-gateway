$(function() {
    $(".btn-container-ctrl").click(function() {
        var op  = $(this).data("value");
        var url = $(this).data("url");
        var data = {'op': op};

        if ($(this).data('status') == 'enabled') {
            $.ajax({
                type: "PUT",
                url: url,
                data: JSON.stringify(data),
                contentType: "application/json; charset=utf-8",
                success: function() {
                    location.reload();
                },
                error: function() {
                    alert("Update failed");
                }
            });
        } else {
            alert("Button is disabled...Login to continue!");
        }
    });
});
