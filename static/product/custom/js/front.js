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

    // go to list page
    jQuery("#f_global_search_btn, #f_search_finder_btn").click(function () {
        var from_year = $('#finder_from_year').val();
        var to_year = $('#finder_to_year').val();
        location.href = "/lots/?from_year=" + from_year + "&to_year=" + to_year;
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

    // set search result div width
    /*
    if ( screen.width <= 550 ) {
        jQuery(".f_l_sr_dv").addClass("f_100_wth");
    } else {
        jQuery(".f_l_sr_dv").removeClass("f_100_wth");
    }

    jQuery(window).resize(function(){
        if ( screen.width <= 550 ) {
            jQuery(".f_l_sr_dv").addClass("f_100_wth");
        } else {
            jQuery(".f_l_sr_dv").removeClass("f_100_wth");
        }
    });
    */
}

/**
 * list page event proc functions
 * */
function front_list_event_proc_funcs() {
    // data table load
    if (jQuery("#f_list_page_mark").val() == "1") {
        jQuery('#c_seach_tb').DataTable({
            "lengthMenu": [[10, 25, 50, 100], [10, 25, 50, 100]],
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