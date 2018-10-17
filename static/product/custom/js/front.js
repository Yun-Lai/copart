jQuery(function () {
    // global event function
    front_global_event_proc_funcs();
    // landing page event functions
    front_landing_event_proc_funcs();
    // list page event proc functions
    front_list_event_proc_funcs();
    // detail page event proc functions
    front_detail_event_proc_funcs();
});

/**
 * global event functions
 * */
function front_global_event_proc_funcs() {
    // Layout.init();
    // Layout.initOWL();
    // Layout.initImageZoom();
    // Layout.initTouchspin();
    // Layout.initTwitter();
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


    // Vehicle Finder
    jQuery("#f_search_finder_btn").click(function () {
        var types = $("#finder_types").val();
        var from_year = $("#finder_from_year").val();
        var to_year = $("#finder_to_year").val();
        var makes = $("#finder_makes").val();
        var models = $("#finder_models").val();
        var locations = $("#finder_location").val();

        if ('0' === makes)
            makes = '_';
        if ('0' === models)
            models = '_';
        if ('0' === locations)
            locations = '_';
        location.href = "/lots_by_search/" + types + "/" + from_year + "/" + to_year + "/" + makes + "/" + models + "/" + locations + "/";
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
        var finder_type = $(this).val();
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
        var finder_type = $("#finder_types").val();
        var finder_make = $(this).val();
        ajax_get_models(finder_type, finder_make);
    });
    $("#finder_models").html('<option value="0">All Models</option>');

    $("#detail_find_more").on('click', function () {
        location.href = "/lots_by_search/" + $("#lot_type").html() + "/2008/2019/" + $("#lot_make").html() + "/_/_/";
    });

    $(".f_f_r_t_scnt_slt").on('change', function() {
        var url = window.location.href;
        if (url.endsWith('/'))
            window.location.href = url + "?page=1&entry=" + $(this).val();
        else
            window.location.href = url.split('&')[0] + '&entry=' + $(this).val();
    });
}

/**
 * list page event proc functions
 * */
function front_list_event_proc_funcs() {
    // data table load
    if (jQuery("#f_list_page_mark").val() == "1") {
        jQuery('#c_seach_tb').DataTable({
            "lengthMenu": [[100], [100]],
            pagerPosition: 'both'
        });

    }

    // left filter function
    jQuery(".f_l_f_tlt").click(function () {
        if (jQuery(this).children("i").is(".fa-minus-square")) {
            jQuery(this).children("i").removeClass("fa-minus-square");
            jQuery(this).children("i").addClass("fa-plus-square");
            jQuery(this).next(".f_l_f_cnt").addClass("g_none_dis");
        } else {
            jQuery(this).children("i").removeClass("fa-plus-square");
            jQuery(this).children("i").addClass("fa-minus-square");
            jQuery(this).next(".f_l_f_cnt").removeClass("g_none_dis");
        }
    });

    // remove filtered filter item
    jQuery(".f_l_f_a_item").children("i").click(function () {
        jQuery(this).parent(".f_l_f_a_item").remove();
    });

    // expand left filter list
    jQuery(".f_list_left_filter_min_i").click(function () {
        if (jQuery(".f_list_filter_cnt").is(":visible")) {
            jQuery(".f_list_filter_cnt").hide();
        } else if (jQuery(".f_list_filter_cnt").is(":hidden")) {
            jQuery(".f_list_filter_cnt").show();
        }
        $(".f_asearch_tlt_dv").toggleClass("open");
    });

    jQuery(".f_list_goto_top_dv").click(function () {
        location.href = "#f_lr_main_dv";
    });

    // set search result div width
    // if ( screen.width <= 992 ) {
    // jQuery(".f_list_filter_cnt").hide();
    // var tw = jQuery(".f_asearch_tdv").width();
    // jQuery(".f_list_search_result_cnt_dv").width(tw);
    // } else {
    // jQuery(".f_list_filter_cnt").show();
    // var tw = jQuery(".f_asearch_tdv").width();
    // var fw = jQuery(".f_list_filter_dv").width();
    // jQuery(".f_list_search_result_cnt_dv").width(tw-fw-20);
    // }

    jQuery(window).resize(function () {
        if (screen.width <= 992) {
            // jQuery(".f_list_filter_cnt").hide();
            var tw = jQuery(".f_asearch_tdv").width();
            jQuery(".f_list_search_result_cnt_dv").width(tw);
        } else {
            // jQuery(".f_list_filter_cnt").show();
            var tw = jQuery(".f_asearch_tdv").width();
            var fw = jQuery(".f_list_filter_dv").width();
            // jQuery(".f_list_search_result_cnt_dv").width(tw-fw-20);
        }
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

}