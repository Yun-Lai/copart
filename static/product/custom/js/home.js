jQuery(function () {
    // global event function
    front_global_event_proc_funcs();
    // landing page event functions
    front_landing_event_proc_funcs();
});

/**
 * global event functions
 * */
function front_global_event_proc_funcs() {
    // Header Search Button
    jQuery("#f_global_search_btn").click(function () {
        let vin_lot = $(".f_search_ipt").val();
        if ('' === vin_lot)
            return;
        $.ajax({
            type: 'GET',
            url: '/ajax_get_lot/',
            data: {vin_or_lot: vin_lot},
            success: function (response) {
                if (response.result)
                    location.href = "/lot/" + response.lot;
                else {
                    // raise 404 page
                }
            }
        });
    });
}

/**
 * landing page event functions
 * */
function front_landing_event_proc_funcs() {
    // tabs event
    jQuery(".f_asearch_r_tabs").children("div").click(function () {
        jQuery(".f_asearch_r_tabs").children("div").removeClass("f_asearch_r_tab_clicked");
        jQuery(this).addClass("f_asearch_r_tab_clicked");
        jQuery(".f_asearch_r_cnts").children(".row").addClass("g_none_dis");
        jQuery(".f_asearch_tab" + jQuery(this).attr("torder")).removeClass("g_none_dis");
    });

    // event extend and pull in
    jQuery(".f_arrival_extend_img").click(function () {
        if (jQuery(this).attr("state") == "0") {
            jQuery(this).attr("state", "1").attr("src", "static/product/custom/imgs/top.png");
            jQuery(".f_land_hide_arrival").removeClass("g_none_dis");
        } else {
            jQuery(this).attr("state", "0").attr("src", "static/product/custom/imgs/down.png");
            jQuery(".f_land_hide_arrival").addClass("g_none_dis");
        }
    });

    // Vehicle Finder
    jQuery("#f_search_finder_btn").click(function () {
        let makes = $("#finder_makes").val();
        let models = $("#finder_models").val();
        let locations = $("#finder_location").val();

        let params = [];
        params.push('type=' + $("#finder_types").val());
        params.push('year=[' + $("#finder_from_year").val() + ',' + $("#finder_to_year").val() + ']');
        if ('0' !== makes)
            params.push('make=' + makes);
        if ('0' !== models)
            params.push('model=' + models);
        if ('0' !== locations)
            params.push('location=' + locations);

        params.push("status=['Sites', 'Already Sold', 'Featured Items', 'Make']");
        params.push("sort={'sort_by':'info__year', 'sort_type': 'desc'}");

        location.href = encodeURI("/lots_by_search/?" + params.join('&'));
    });

    function ajax_get_makes(finder_type) {
        $.ajax({
            type: 'GET',
            url: '/ajax_get_makes/',
            data: {finder_type: finder_type},
            success: function (response) {
                if (response.result) {
                    var str_makes = '<option value="0">All Makes</option>';
                    for (var i = 0; i < response.makes.length; i++) {
                        str_makes += '<option value="' + response.makes[i] + '">' + response.makes[i] + '</option>';
                    }
                    $("#finder_makes").html(str_makes);
                }
            }
        });
    }
    $("#finder_types").on('change', function() {
        let finder_type = $(this).val();
        ajax_get_makes(finder_type);
    });
    ajax_get_makes('V');

    function ajax_get_models(finder_type, finder_make) {
        if ("0" === finder_make) {
            $("#finder_models").html('<option value="0">All Models</option>');
            return;
        }
        $.ajax({
            type: 'GET',
            url: '/ajax_get_models/',
            data: {
                finder_type: finder_type,
                finder_make: finder_make
            },
            success: function (response) {
                if (response.result) {
                    var str_makes = '<option value="0">All Models</option>';
                    for (var i = 0; i < response.models.length; i++) {
                        str_makes += '<option value="' + response.models[i] + '">' + response.models[i] + '</option>';
                    }
                    $("#finder_models").html(str_makes);
                }
            }
        });
    }
    $("#finder_makes").on('change', function() {
        let finder_type = $("#finder_types").val();
        let finder_make = $(this).val();
        ajax_get_models(finder_type, finder_make);
    });
    $("#finder_models").html('<option value="0">All Models</option>');
}
