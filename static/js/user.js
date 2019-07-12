$(function() {
    // delete user
    $(".btn-del-user").click(function() {
        var uname = $(this).data('uname');
        if(confirm("Are you sure to delete '" + uname + "'?")) {
            $.ajax({
                type: "DELETE",
                url: $(this).data('url'),
                success: function() {
                    alert("User Deleted");
                    location.reload();
                },
                error: function() {
                    alert("Delete Failed");
                }
            });
        };
    });

    // edit user
    $(".btn-edit-user").click(function() {
        var uname = $(this).data('uname');
        var cname = $(this).data('cname');
        var desc  = $(this).data('desc');
        var curl  = $(this).data('curl');
        var url   = $(this).data('url');
        $(".modal-body #username").val(uname);
        $(".modal-body #container_name").val(cname);
        $(".modal-body #description").val(desc);
        $(".modal-body #notebook_url").val(curl);
        $(".modal-body #user_url").val(url);
    });

    // submit update user
    $(".submit-update-user").click(function() {
        var uname = $(".modal-body #username").val();
        // var cname   = $(".modal-body #container_name").val();
        var pass  = $(".modal-body #password").val();
        var desc  = $(".modal-body #description").val();
        // var curl  = $(".modal-body #notebook_url").val();
        var url   = $(".modal-body #user_url").val();
        var data  = {'name': uname, 'password': pass, 'description': desc};

        $.ajax({
            type: "PUT",
            url: url,
            data: JSON.stringify(data),
            contentType: "application/json; charset=utf-8",
            success: function() {
                alert("User Updated");
                location.reload();
            },
            error: function() {
                alert("Update Failed");
            }
        });
    });

    // submit create user
    $(".submit-create-user").click(function() {
        var username = $(".modal-body #new_username").val();
        var password = $(".modal-body #new_password").val();
        var cid   = $(".modal-body #new_container_id").val();
        var desc  = $(".modal-body #new_description").val();
        var url   = $(".open-create-user").data('url');
        var data  = {'username': username, 'password': password,
                     'description': desc,
                     'container_id': cid};

        //console.log(data);
        //console.log(url);

        $.ajax({
            type: "POST",
            url: url,
            data: JSON.stringify(data),
            contentType: "application/json; charset=utf-8",
            success: function() {
                alert("User Created");
                location.reload();
            },
            error: function() {
                alert("Create Failed");
            }
        });
    });

    // edit service (container)
    $(".btn-edit-container").click(function() {
        var curl  = $(this).data('curl');
        var cid   = $(this).data('cid');
        var cname = $(this).data('cname');
        var uname = $(this).data('uname');

        //console.log("curl:", curl);
        //console.log("cid:", cid);
        //console.log("cname:", cname);
        //console.log("uname:", uname);

        $(".modal-body #uname").val(uname);
        $(".modal-body #cid").val(cid);
        $(".modal-body #cname").val(cname);
        $(".modal-body #notebook_url").val(curl);
    });

//    $('.selectpicker').on('changed.bs.select', function (e) {
//            var selected = e.target.value;
//            console.log(selected);
//    });

    // create new service
    $(".btn-start-service").click(function(e) {
        e.preventDefault();
        var uname  = $("#uname").val();
        var cimage = $("#clist").val();
        var csect  = $("#csect").val();
        var url    = $(this).data('url');
        var data   = {'image': cimage, 'mach': csect, 'uname': uname,};

        if (cimage == 'notebook')
        {
            data['mach'] = '';
        }
        console.log("---Starting Service---")
        console.log("uname:", uname);
        console.log("cimage:", cimage);
        console.log("section:", csect);
        console.log("url:", url);
        console.log(JSON.stringify(data));

        $.ajax({
            type: "POST",
            url: url,
            data: JSON.stringify(data),
            contentType: "application/json; charset=utf-8",
            success: function(data) {
                //console.log(data);
                $(".modal-body #cid").val(data['id']);
                $(".modal-body #cname").val(data['name']);

                // update user via submit btn.
                // add reset container button, along as start.

                $(".modal-body #notebook_url").val(data['nb_url']);
                alert("New service created");
            },
            error: function() {
                alert("Failed to create new service!");
            }
        });
    });

    // submit update container (update user configuration)
    $(".submit-update-container").click(function() {
        var url  = $(".btn-edit-container").data('url');
        var curl = $(".modal-body #notebook_url").val();
        var cname  = $(".modal-body #cname").val();
        var data = {'container_name': cname}

        console.log("--- Update container status ---")
        console.log(JSON.stringify(data));
        console.log(url)

        $.ajax({
            type: "PUT",
            url: url,
            data: JSON.stringify(data),
            contentType: "application/json; charset=utf-8",
            success: function() {
                alert("User's service updated");
                location.reload();
            },
            error: function() {
                alert("Failed to update user's service, START and UPDATE again.");
            }
        });
    });

});
