jQuery(function () {
    $(window).load(function() {
		$(".se-pre-con").fadeOut("slow");
	});

    // global event function
    front_global_event_proc_funcs();
    // list page event proc functions
    front_list_event_proc_funcs();
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

    // page entry changed
    $(".f_f_r_t_scnt_slt").on('change', function() {
        let current_url = decodeURI(location.href);
        if (current_url.endsWith('/')) {
            location.href = encodeURI(current_url + "?page=1&entry=" + $(this).val());
        }
        else {
            let exists = false;
            let params = decodeURI(location.search).slice(1).split('&');
            for (let i = 0; i < params.length; i++) {
                if (params[i].startsWith('entry=')) {
                    params[i] = 'entry=' + $(this).val();
                    exists = true;
                    break;
                }
            }
            if (!exists) {
                params.push('page=1');
                params.push('entry=' + $(this).val());
            }
            params = params.join('&');
            location.href = encodeURI(location.pathname + '?' + params);
        }
    });

    // Go To Page clicked
    $(".f_lr_goto_page_img").on('click', function() {
        let current_url = decodeURI(location.href);
        let page = $(".f_f_r_t_goto_ipt").val();
        let entry = $(".f_f_r_t_scnt_slt").val();
        if (current_url.endsWith('/')) {
            location.href = encodeURI(current_url + "?page=" + page + "&entry=" + entry);
        }
        else {
            let exists = false;
            let params = decodeURI(location.search).slice(1).split('&');
            for (let i = 0; i < params.length; i++) {
                if (params[i].startsWith('page=')) {
                    params[i] = 'page=' + page;
                    exists = true;
                    break;
                }
            }
            if (!exists) {
                params.push('page=' + page);
                params.push('entry=' + entry);
            }
            params = params.join('&');
            location.href = encodeURI(location.pathname + '?' + params);
        }
    });

    // ------------Left Filters Start------------

    // Sites
    $(".f_list_filter_site").on('click', function () {
        let filters = location.search;
        let filter_source = applied_filter_source;
        let id = $(this).prop('id');

        if ("" === filters) {
            if ("flfc10" === id && "" !== filter_source) {
                // all, remove 'source' from url
            }
            else if ("flfc11" === id && "copart" !== filter_source) {
                // copart, add or change 'source' in url
                location.href = encodeURI(location.pathname + '?params={"source": "copart"}');
            }
            else if ("flfc12" === id && "iaai" !== filter_source) {
                // iaai, add or change 'source' in url
                location.href = encodeURI(location.pathname + '?params={"source": "iaai"}');
            }
        }
        else {
            let exists = false;
            filters = decodeURI(location.search).slice(1).split('&');
            for (let i = 0; i < filters.length; i++) {
                if (filters[i].startsWith('params=')) {
                    let param = JSON.parse(filters[i].split('=')[1]);
                    if ("flfc10" === id && "" !== filter_source) {
                        delete param.source;
                    }
                    else if ("flfc11" === id && "copart" !== filter_source) {
                        param.source = "copart";
                    }
                    else if ("flfc12" === id && "iaai" !== filter_source) {
                        param.source = "iaai";
                    }
                    filters[i] = 'params=' + JSON.stringify(param);
                    exists = true;
                }
            }

            if (!exists) {
                if ("flfc10" === id && "" !== filter_source) {
                    // all, remove 'source' from url
                }
                else if ("flfc11" === id && "copart" !== filter_source) {
                    // copart, add or change 'source' in url
                    filters.push('params={"source": "copart"}');
                }
                else if ("flfc12" === id && "iaai" !== filter_source) {
                    // iaai, add or change 'source' in url
                    filters.push('params={"source": "iaai"}');
                }
            }

            for (let i = 0; i < filters.length; i++) {
                if (filters[i].startsWith('params=') && "params={}" === filters[i]) {
                    filters = filters.filter(item => "params={}" !== item);
                }
            }

            if (filters.length > 0)
                location.href = encodeURI(location.pathname + '?' + filters.join('&'));
            else
                location.href = location.pathname;
        }
    });

    // Already Sold
    // Featured Items
    // Make
    // Model
    // Year
    // Odometer
    // Location
    // ------------Left Filters End------------

    change_make_filter_input();
}

let clicked_makes = applied_filter_makes;

function change_make_filter_input() {
    $("#input_filter_make").on('input', function () {
        if ($(this).val().length === 1)
            return;

        let html = "";
        let makes = all_makes_for_filter;
        if ($(this).val().length === 0) {
            for (let i = 0; i < 10; i++)
                html += '<input type="checkbox" id="id_make_' + makes[i].make + '" class="checkbox_make"' + (clicked_makes.includes(makes[i].make) ? ' checked' : '') + '/><label for="id_make_' + makes[i].make + '">' + makes[i].make + ' (' + makes[i].count + ')</label> <br>';
        }
        else {
            makes = makes.filter(item => item.make.toLowerCase().includes($(this).val().toLowerCase()));
            for (let i = 0; i < makes.length; i++)
                html += '<input type="checkbox" id="id_make_' + makes[i].make + '" class="checkbox_make"' + (clicked_makes.includes(makes[i].make) ? ' checked' : '') + '/><label for="id_make_' + makes[i].make + '">' + makes[i].make + ' (' + makes[i].count + ')</label> <br>';
        }
        $("#div_filter_make").html(html);
        click_make_checkbox();
    });

    click_make_checkbox();
    click_make_filter();
}

function click_make_checkbox() {
    $(".checkbox_make").on('click', function () {
        let make_name = $(this).prop('id').substring(8);
        if ($(this).prop('checked'))
            clicked_makes.push(make_name);
        else
            clicked_makes = clicked_makes.filter(item => item !== make_name);
        let html = "";
        if ($("#id_filters_applied").html().includes("No Filters Applied")) {
            html = '<div id="id_filter_make_' + make_name + '" class="f_l_f_a_item filter_make">' + make_name + '<img class="f_list_fr_close" src="/static/product/custom/imgs/close.png"/></div>';
        }
        else if (clicked_makes.length > 0) {
            for (let i = 0; i < clicked_makes.length; i++)
                html += '<div id="id_filter_make_' + clicked_makes[i] + '" class="f_l_f_a_item filter_make">' + clicked_makes[i] + '<img class="f_list_fr_close" src="/static/product/custom/imgs/close.png"/></div>';
        }
        else {
            html = 'No Filters Applied';
        }
        $("#id_filters_applied").html(html);
        click_make_filter();

        let current_url = decodeURI(location.href);
        if (current_url.endsWith('/')) {
            location.href = encodeURI(current_url + '?makes=[' + clicked_makes[0] + ']');
        }
        else {
            let params = location.search.slice(1).split('&');
            params = params.filter(item => !item.startsWith('makes='));
            if (clicked_makes.length > 0)
                params.push('makes=[' + clicked_makes.join(',') + ']');
            params = params.join('&');
            location.href = encodeURI(location.pathname + '?' + params);
        }
    });
}

function click_make_filter() {
    $(".filter_make").on('click', function () {
        let make_name = $(this).prop('id').substring(15);
        if (make_name.includes(' ')) {
            let start_make = make_name.split(' ')[0];
            $("[id^=id_make_" + start_make + "]").prop('checked', false);
        }
        else {
            $("#id_make_" + make_name).prop('checked', false);
        }

        clicked_makes = clicked_makes.filter(item => item !== make_name);
        let html = "";
        if (clicked_makes.length > 0) {
            for (let i = 0; i < clicked_makes.length; i++)
                html += '<div id="id_filter_make_' + clicked_makes[i] + '" class="f_l_f_a_item filter_make">' + clicked_makes[i] + '<img class="f_list_fr_close" src="/static/product/custom/imgs/close.png"/></div>';
        }
        else {
            html = 'No Filters Applied';
        }
        $("#id_filters_applied").html(html);
        click_make_filter();

        let current_url = decodeURI(location.href);
        if (current_url.endsWith('/')) {
            location.href = encodeURI(current_url + '?makes=[' + clicked_makes[0] + ']');
        }
        else {
            let params = location.search.slice(1).split('&');
            params = params.filter(item => !item.startsWith('makes='));
            if (clicked_makes.length > 0)
                params.push('makes=[' + clicked_makes.join(',') + ']');
            params = params.join('&');
            location.href = encodeURI(location.pathname + '?' + params);
        }
    });
}
