jQuery(function () {
    // global event function
    front_global_event_proc_funcs();
    // detail page event proc functions
    front_detail_event_proc_funcs();
});

/**
 * global event functions
 * */
function front_global_event_proc_funcs() {
    // Header Search Button
    jQuery("#f_global_search_btn").click(function () {
        var vin_lot = $(".f_search_ipt").val();
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
 * detail page event proc functions
 * */
function front_detail_event_proc_funcs() {
    jQuery(".p_a_gallery_sub_img").click(function () {
        jQuery(".f_l_detail_photo").attr("src", jQuery(this).attr("src"));
        jQuery(".f_detail_main_img_a").attr("href", jQuery(this).attr("src"));
    });

    // gallery arrow margintop setting
    var ih = parseInt(jQuery(".p_a_gallery_sub_img").height());
    var mt = ( ih - 30 ) / 2 - 30;
    jQuery(".f_detail_arrow_a").css("margin-top", mt);

    jQuery(window).resize(function () {
        var ih = parseInt(jQuery(".p_a_gallery_sub_img").height());
        var mt = ( ih - 30 ) / 2 - 30;
        jQuery(".f_detail_arrow_a").css("margin-top", mt);
    });

    // event extend and pull in
    jQuery(".f_arrival_extend_img").click(function () {
        if (jQuery(this).attr("state") == "0") {
            jQuery(this).attr("state", "1").attr("src", "/static/product/custom/imgs/top.png");
            jQuery(".f_land_hide_arrival").removeClass("g_none_dis");
        } else {
            jQuery(this).attr("state", "0").attr("src", "/static/product/custom/imgs/down.png");
            jQuery(".f_land_hide_arrival").addClass("g_none_dis");
        }
    });

    $("#detail_find_more").on('click', function () {
        location.href = "/lots_by_search/" + $("#lot_type").html() + "/2008/2019/" + $("#lot_make").html() + "/_/_/";
    });
}