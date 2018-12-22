jQuery(function () {
    $(document).ajaxStart(function () {
        $("body").addClass("loading");
    }).ajaxStop(function () {
        $("body").removeClass("loading");
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
                    location.href = "/lot/" + response['lot'];
                else {
                    // raise 404 page
                }
            }
        });
    });
}

function ajax_get_vehicles() {
    let initial_params = $("#initial").attr('initial');
    let params = $("#params").attr('url');
    let shows_status = $("#shows").attr('status');
    if (params)
        params = '&' + params;
    let path = encodeURI('/lots_by_search/?' + initial_params + params + '&status=' + shows_status);
    $.ajax({
        type: 'GET',
        url: '/ajax_get_vehicles/?' + initial_params + params,
        data: {'status': shows_status},
        success: function (response) {
            $("#list_content").html(response);
            front_list_event_proc_funcs();
            window.history.pushState({route: path}, "EVILEG", path);
        },
        error: function (response) {

        }
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

            let status = eval($("#shows").attr('status'));
            let selected_filter = $(this).html().split('</i>')[1];
            status = status.filter(item => item !== selected_filter);
            $('#shows').attr('status', "['" + status.join("','") + "']");

        } else {
            jQuery(this).children("i").removeClass("fa-plus-square");
            jQuery(this).children("i").addClass("fa-minus-square");
            jQuery(this).next(".f_l_f_cnt").removeClass("g_none_dis");

            let status = eval($("#shows").attr('status'));
            let selected_filter = $(this).html().split('</i>')[1];
            status.push(selected_filter);
            $('#shows').attr('status', "['" + status.join("','") + "']");
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
        let current_url = $("#params").attr('url');
        if ('' === current_url) {
            $("#params").attr('url', "page=1&entry=" + $(this).val());
        }
        else {
            let exists = false;
            let params = current_url.split('&');
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
            $("#params").attr('url', params);
        }
        ajax_get_vehicles();
    });

    // Go To Page clicked
    $(".f_lr_goto_page_img").on('click', function() {
        let current_url = $("#params").attr('url');
        let page = $(".f_f_r_t_goto_ipt").val();
        let entry = $(".f_f_r_t_scnt_slt").val();
        if ('' === current_url) {
            $("#params").attr('url', "page=" + page + "&entry=" + entry);
        }
        else {
            let exists = false;
            let params = current_url.split('&');
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
            $("#params").attr('url', params);
        }
        ajax_get_vehicles();
    });

    $(".f_list_page_num a").on('click', function() {
        let current_url = $("#params").attr('url');
        let page = $(this).attr('page');
        let entry = $(".f_f_r_t_scnt_slt").val();
        if ('' === current_url) {
            $("#params").attr('url', "page=" + page + "&entry=" + entry);
        }
        else {
            let exists = false;
            let params = current_url.split('&');
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
            $("#params").attr('url', params);
        }
        ajax_get_vehicles();
    });

    // ------------Left Filters Start------------

    // Sites
    $(".f_list_filter_site").on('click', function () {
        let filters = $("#params").attr('url');
        let filter_source = applied_filter_source;
        let id = $(this).prop('id');

        if ("" === filters) {
            if ("flfc10" === id && "" !== filter_source) {
                // all, remove 'source' from url
            }
            else if ("flfc11" === id && "copart" !== filter_source) {
                // copart, add or change 'source' in url
                $("#params").attr('url', 'params={"source":"copart"}');
            }
            else if ("flfc12" === id && "iaai" !== filter_source) {
                // iaai, add or change 'source' in url
                $("#params").attr('url', 'params={"source":"iaai"}');
            }
        }
        else {
            let exists = false;
            filters = filters.split('&');
            for (let i = 0; i < filters.length; i++) {
                if (filters[i].startsWith('params=')) {
                    let param = JSON.parse(filters[i].split('=')[1]);
                    if ("flfc10" === id && "" !== filter_source) {
                        delete param['source'];
                    }
                    else if ("flfc11" === id && "copart" !== filter_source) {
                        param['source'] = "copart";
                    }
                    else if ("flfc12" === id && "iaai" !== filter_source) {
                        param['source'] = "iaai";
                    }
                    filters[i] = 'params=' + JSON.stringify(param);
                    exists = true;
                    break;
                }
            }

            if (!exists) {
                if ("flfc10" === id && "" !== filter_source) {
                    // all, remove 'source' from url
                }
                else if ("flfc11" === id && "copart" !== filter_source) {
                    // copart, add or change 'source' in url
                    filters.push('params={"source":"copart"}');
                }
                else if ("flfc12" === id && "iaai" !== filter_source) {
                    // iaai, add or change 'source' in url
                    filters.push('params={"source":"iaai"}');
                }
            }

            for (let i = 0; i < filters.length; i++) {
                if (filters[i].startsWith('params=') && "params={}" === filters[i]) {
                    filters = filters.filter(item => "params={}" !== item);
                }
            }

            if (filters.length > 0)
                $("#params").attr('url', filters.join('&'));
            else
                $("#params").attr('url', "");
        }
        ajax_get_vehicles();
    });

    // Already Sold
    $("#flfc100").on('click', function () {
        let filters = $("#params").attr('url');
        let checked = $(this).prop('checked');

        if ("" === filters) {
            if (checked)
                $("#params").attr('url', 'params={"sold":"yes"}');
        }
        else {
            let exists = false;
            filters = filters.split('&');
            for (let i = 0; i < filters.length; i++) {
                if (filters[i].startsWith('params=')) {
                    let param = JSON.parse(filters[i].split('=')[1]);
                    if (checked)
                        param.sold = "yes";
                    else
                        delete param['sold'];
                    filters[i] = 'params=' + JSON.stringify(param);
                    exists = true;
                    break;
                }
            }

            if (!exists) {
                if (checked)
                    filters.push('params={"sold":"yes"}');
            }

            for (let i = 0; i < filters.length; i++) {
                if (filters[i].startsWith('params=') && "params={}" === filters[i]) {
                    filters = filters.filter(item => "params={}" !== item);
                }
            }

            if (filters.length > 0)
                $("#params").attr('url', filters.join('&'));
            else
                $("#params").attr('url', "");
        }
        ajax_get_vehicles();
    });

    // Featured Items
    change_featured_filter_input();
    on_click_featured_checkboxes("featured");
    on_click_applied_featured("featured");
    // Make
    change_make_filter_input();
    on_click_make_checkboxes("make");
    on_click_applied_make("make");
    // Model
    change_model_filter_input("model");
    on_click_model_checkboxes("model");
    on_click_applied_model("model");
    // Year
    change_year_filter_input("year");
    on_click_year_checkboxes("year");
    on_click_applied_year("year");
    // Odometer
    // change_odometer_filter_input("odometer");
    // on_click_odometer_checkboxes("odometer");
    // on_click_applied_odometer("odometer");
    // Location
    change_location_filter_input("location");
    on_click_location_checkboxes("location");
    on_click_applied_location("location");
    // ------------Left Filters End------------
}

function make_url(initial, name, filter_list) {
    let url = "";
    let filters = $("#params").attr('url');
    if ("" === filters) {
        url = 'params={"' + initial + '":["' + name + '"]}';
    }
    else {
        let exists = false;
        filters = filters.split('&');
        for (let i = 0; i < filters.length; i++) {
            if (filters[i].startsWith('params=')) {
                let param = JSON.parse(filters[i].split('=')[1]);
                if (initial in param && 0 === filter_list.length)
                    delete param[initial];
                else
                    param[initial] = filter_list;
                filters[i] = 'params=' + JSON.stringify(param);
                exists = true;
                break;
            }
        }

        let exists_initial_filter = false;
        for (let i = 0; i < filters.length; i++) {
            if (filters[i].startsWith(initial.substring(0, initial.length - 1) + '=')) {
                exists_initial_filter = true;
                exists = true;
                break;
            }
        }
        if (exists_initial_filter)
            filters = filters.filter(item => !item.startsWith(initial.substring(0, initial.length - 1) + '='));

        if (!exists) {
            filters.push('params={"' + initial + '":["' + name + '"]}');
        }

        for (let i = 0; i < filters.length; i++) {
            if (filters[i].startsWith('params=') && "params={}" === filters[i]) {
                filters = filters.filter(item => "params={}" !== item);
            }
        }

        if (filters.length > 0)
            url = filters.join('&');
        else
            url = '';
    }
    return url;
}

let clicked_features = applied_filter_features;
function change_featured_filter_input() {
    // console.log('input', 'featured', 'function', clicked_features);
    $("#input_filter_featured").on('input', function () {
        // console.log('input', 'featured', 'event', clicked_features);
        let html = "";
        let features = all_features_for_filter;
        if ($(this).val().length !== 0)
            features = features.filter(item => item.feature.toLowerCase().includes($(this).val().toLowerCase()));
        for (let i = 0; i < features.length; i++)
            html += '<input type="checkbox" id="id_featured_' + features[i].feature + '" class="checkbox_featured"' + (clicked_features.includes(features[i].feature) ? ' checked' : '') + '/><label for="id_featured_' + features[i].feature + '">' + features[i].feature + ' (' + features[i].count + ')</label> <br>';
        $("#div_filter_featured").html(html);
        on_click_featured_checkboxes("featured");
    });
}

function on_click_featured_checkboxes(initial) {
    // console.log('checkbox', initial, 'function', clicked_features);
    $(".checkbox_" + initial).on('click', function () {
        // console.log('checkbox', initial, 'event', clicked_features);
        let name = $(this).prop('id').substring(4 + initial.length);
        let filters_applied = $("#id_filters_applied");
        let checked = $(this).prop('checked');

        if (checked) {
            clicked_features.push(name);
            let html = '<div id="id_filter_' + initial + '_' + name + '" class="f_l_f_a_item filter_' + initial + '">' + name + '<img class="f_list_fr_close" src="/static/product/custom/imgs/close.png"/></div>';
            if (filters_applied.html().includes("No Filters Applied")) {
                filters_applied.html(html);
            }
            else {
                let new_feature = document.createElement('div');
                new_feature.innerHTML = html;
                document.getElementById('id_filters_applied').appendChild(new_feature);
            }
        }
        else {
            clicked_features = clicked_features.filter(item => item !== name);
            let start = name.split(' ')[0];
            $("[id^=id_filter_" + initial + "_" + start + "]").remove();
        }

        on_click_applied_featured("featured");

        $("#params").attr('url', make_url("featured", name, clicked_features));
        ajax_get_vehicles();
    });
}

function on_click_applied_featured(initial) {
    // console.log('applied', initial, 'function', clicked_features);
    $(".filter_" + initial).on('click', function () {
        // console.log('applied', initial, 'event', clicked_features);
        let name = $(this).prop('id').substring(11 + initial.length);
        let start = name.split(' ')[0];
        $("[id^=id_" + initial + "_" + start + "]").prop('checked', false);

        clicked_features = clicked_features.filter(item => item !== name);

        $("[id^=id_filter_" + initial + "_" + start + "]").remove();

        $("#params").attr('url', make_url("featured", name, clicked_features));
        ajax_get_vehicles();
    });
}

let clicked_makes = applied_filter_makes;
function change_make_filter_input() {
    // console.log('input', 'make', 'function', clicked_makes);
    $("#input_filter_make").on('input', function () {
        // console.log('input', 'make', 'event', clicked_makes);
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
        on_click_make_checkboxes("make");
    });
}
function on_click_make_checkboxes(initial) {
    // console.log('checkbox', initial, 'function', clicked_makes);
    $(".checkbox_" + initial).on('click', function () {
        // console.log('checkbox', initial, 'event', clicked_makes);
        let name = $(this).prop('id').substring(4 + initial.length);
        let filters_applied = $("#id_filters_applied");

        if ($(this).prop('checked')) {
            clicked_makes.push(name);
            let html = '<div id="id_filter_' + initial + '_' + name + '" class="f_l_f_a_item filter_' + initial + '">' + name + '<img class="f_list_fr_close" src="/static/product/custom/imgs/close.png"/></div>';
            if (filters_applied.html().includes("No Filters Applied")) {
                filters_applied.html(html);
            }
            else {
                let new_feature = document.createElement('div');
                new_feature.innerHTML = html;
                document.getElementById('id_filters_applied').appendChild(new_feature);
            }
        }
        else {
            clicked_makes = clicked_makes.filter(item => item !== name);
            let start = name.split(' ')[0];
            $("[id^=id_filter_" + initial + "_" + start + "]").remove();
        }

        on_click_applied_make("make");

        $("#params").attr('url', make_url("makes", name, clicked_makes));
        ajax_get_vehicles();
    });
}
function on_click_applied_make(initial) {
    // console.log('applied', initial, 'function', clicked_makes);
    $(".filter_" + initial).on('click', function () {
        // console.log('applied', initial, 'event', clicked_makes);
        let name = $(this).prop('id').substring(11 + initial.length);
        let start = name.split(' ')[0];
        $("[id^=id_" + initial + "_" + start + "]").prop('checked', false);

        clicked_makes = clicked_makes.filter(item => item !== name);

        $("[id^=id_filter_" + initial + "_" + start + "]").remove();

        $("#params").attr('url', make_url("makes", name, clicked_makes));
        ajax_get_vehicles();
    });
}

let clicked_models = applied_filter_models;
function change_model_filter_input(initial) {
    $("#input_filter_" + initial).on('input', function () {
        if ($(this).val().length === 1)
            return;

        let html = "";
        let models = all_models_for_filter;
        if ($(this).val().length === 0) {
            for (let i = 0; i < 10; i++)
                html += '<input type="checkbox" id="id_' + initial + '_' + models[i][initial] + '" class="checkbox_' + initial + '"' + (clicked_models.includes(models[i][initial]) ? ' checked' : '') + '/><label for="id_' + initial + '_' + models[i][initial] + '">' + models[i][initial] + ' (' + models[i]['count'] + ')</label> <br>';
        }
        else {
            models = models.filter(item => item[initial].toLowerCase().includes($(this).val().toLowerCase()));
            for (let i = 0; i < models.length; i++)
                html += '<input type="checkbox" id="id_' + initial + '_' + models[i][initial] + '" class="checkbox_' + initial + '"' + (clicked_models.includes(models[i][initial]) ? ' checked' : '') + '/><label for="id_' + initial + '_' + models[i][initial] + '">' + models[i][initial] + ' (' + models[i]['count'] + ')</label> <br>';
        }
        $("#div_filter_" + initial).html(html);
        on_click_model_checkboxes("model");
    });
}
function on_click_model_checkboxes(initial) {
    $(".checkbox_" + initial).on('click', function () {
        let name = $(this).prop('id').substring(4 + initial.length);
        let filters_applied = $("#id_filters_applied");

        if ($(this).prop('checked')) {
            clicked_models.push(name);
            let html = '<div id="id_filter_' + initial + '_' + name + '" class="f_l_f_a_item filter_' + initial + '">' + name + '<img class="f_list_fr_close" src="/static/product/custom/imgs/close.png"/></div>';
            if (filters_applied.html().includes("No Filters Applied")) {
                filters_applied.html(html);
            }
            else {
                let new_feature = document.createElement('div');
                new_feature.innerHTML = html;
                document.getElementById('id_filters_applied').appendChild(new_feature);
            }
        }
        else {
            clicked_models = clicked_models.filter(item => item !== name);
            let start = name.split(' ')[0];
            $("[id^=id_filter_" + initial + "_" + start + "]").remove();
        }

        on_click_applied_model("model");

        $("#params").attr('url', make_url("models", name, clicked_models));
        ajax_get_vehicles();
    });
}
function on_click_applied_model(initial) {
    $(".filter_" + initial).on('click', function () {
        let name = $(this).prop('id').substring(11 + initial.length);
        let start = name.split(' ')[0];
        $("[id^=id_" + initial + "_" + start + "]").prop('checked', false);

        clicked_models = clicked_models.filter(item => item !== name);

        $("[id^=id_filter_" + initial + "_" + start + "]").remove();

        $("#params").attr('url', make_url("models", name, clicked_models));
        ajax_get_vehicles();
    });
}

let clicked_years = applied_filter_years;
function change_year_filter_input(initial) {
    $("#input_filter_" + initial).on('input', function () {
        if ($(this).val().length === 1)
            return;

        let html = "";
        let years = all_years_for_filter;
        if ($(this).val().length === 0) {
            for (let i = 0; i < 10; i++)
                html += '<input type="checkbox" id="id_' + initial + '_' + years[i][initial] + '" class="checkbox_' + initial + '"' + (clicked_years.includes(years[i][initial]) ? ' checked' : '') + '/><label for="id_' + initial + '_' + years[i][initial] + '">' + years[i][initial] + ' (' + years[i]['count'] + ')</label> <br>';
        }
        else {
            years = years.filter(item => item[initial].toLowerCase().includes($(this).val().toLowerCase()));
            for (let i = 0; i < years.length; i++)
                html += '<input type="checkbox" id="id_' + initial + '_' + years[i][initial] + '" class="checkbox_' + initial + '"' + (clicked_years.includes(years[i][initial]) ? ' checked' : '') + '/><label for="id_' + initial + '_' + years[i][initial] + '">' + years[i][initial] + ' (' + years[i]['count'] + ')</label> <br>';
        }
        $("#div_filter_" + initial).html(html);
        on_click_year_checkboxes("year");
    });
}
function on_click_year_checkboxes(initial) {
    $(".checkbox_" + initial).on('click', function () {
        let name = $(this).prop('id').substring(4 + initial.length);
        let filters_applied = $("#id_filters_applied");

        if ($(this).prop('checked')) {
            clicked_years.push(name);
            let html = '<div id="id_filter_' + initial + '_' + name + '" class="f_l_f_a_item filter_' + initial + '">' + name + '<img class="f_list_fr_close" src="/static/product/custom/imgs/close.png"/></div>';
            if (filters_applied.html().includes("No Filters Applied")) {
                filters_applied.html(html);
            }
            else {
                let new_feature = document.createElement('div');
                new_feature.innerHTML = html;
                document.getElementById('id_filters_applied').appendChild(new_feature);
            }
        }
        else {
            clicked_years = clicked_years.filter(item => item !== name);
            let start = name.split(' ')[0];
            $("[id^=id_filter_" + initial + "_" + start + "]").remove();
        }

        on_click_applied_year("year");

        $("#params").attr('url', make_url("years", name, clicked_years));
        ajax_get_vehicles();
    });
}
function on_click_applied_year(initial) {
    $(".filter_" + initial).on('click', function () {
        let name = $(this).prop('id').substring(11 + initial.length);
        let start = name.split(' ')[0];
        $("[id^=id_" + initial + "_" + start + "]").prop('checked', false);

        clicked_years = clicked_years.filter(item => item !== name);

        $("[id^=id_filter_" + initial + "_" + start + "]").remove();

        $("#params").attr('url', make_url("years", name, clicked_years));
        ajax_get_vehicles();
    });
}

let clicked_odometers = applied_filter_odometers;
function change_odometer_filter_input(initial) {
    $("#input_filter_" + initial).on('input', function () {
        if ($(this).val().length === 1)
            return;

        let html = "";
        let odometers = all_odometers_for_filter;
        if ($(this).val().length === 0) {
            for (let i = 0; i < 10; i++)
                html += '<input type="checkbox" id="id_' + initial + '_' + odometers[i][initial] + '" class="checkbox_' + initial + '"' + (clicked_odometers.includes(odometers[i][initial]) ? ' checked' : '') + '/><label for="id_' + initial + '_' + odometers[i][initial] + '">' + odometers[i][initial] + ' (' + odometers[i]['count'] + ')</label> <br>';
        }
        else {
            odometers = odometers.filter(item => item[initial].toLowerCase().includes($(this).val().toLowerCase()));
            for (let i = 0; i < odometers.length; i++)
                html += '<input type="checkbox" id="id_' + initial + '_' + odometers[i][initial] + '" class="checkbox_' + initial + '"' + (clicked_odometers.includes(odometers[i][initial]) ? ' checked' : '') + '/><label for="id_' + initial + '_' + odometers[i][initial] + '">' + odometers[i][initial] + ' (' + odometers[i]['count'] + ')</label> <br>';
        }
        $("#div_filter_" + initial).html(html);
        on_click_odometer_checkboxes("odometer");
    });
}
function on_click_odometer_checkboxes(initial) {
    $(".checkbox_" + initial).on('click', function () {
        let name = $(this).prop('id').substring(4 + initial.length);
        let filters_applied = $("#id_filters_applied");

        if ($(this).prop('checked')) {
            clicked_odometers.push(name);
            let html = '<div id="id_filter_' + initial + '_' + name + '" class="f_l_f_a_item filter_' + initial + '">' + name + '<img class="f_list_fr_close" src="/static/product/custom/imgs/close.png"/></div>';
            if (filters_applied.html().includes("No Filters Applied")) {
                filters_applied.html(html);
            }
            else {
                let new_feature = document.createElement('div');
                new_feature.innerHTML = html;
                document.getElementById('id_filters_applied').appendChild(new_feature);
            }
        }
        else {
            clicked_odometers = clicked_odometers.filter(item => item !== name);
            let start = name.split(' ')[0];
            $("[id^=id_filter_" + initial + "_" + start + "]").remove();
        }

        on_click_applied_odometer("odometer");

        $("#params").attr('url', make_url("odometers", name, clicked_odometers));
        ajax_get_vehicles();
    });
}
function on_click_applied_odometer(initial) {
    $(".filter_" + initial).on('click', function () {
        let name = $(this).prop('id').substring(11 + initial.length);
        let start = name.split(' ')[0];
        $("[id^=id_" + initial + "_" + start + "]").prop('checked', false);

        clicked_odometers = clicked_odometers.filter(item => item !== name);

        $("[id^=id_filter_" + initial + "_" + start + "]").remove();

        $("#params").attr('url', make_url("odometers", name, clicked_odometers));
        ajax_get_vehicles();
    });
}

let clicked_locations = applied_filter_locations;
function change_location_filter_input(initial) {
    $("#input_filter_" + initial).on('input', function () {
        if ($(this).val().length === 1)
            return;

        let html = "";
        let locations = all_locations_for_filter;
        if ($(this).val().length === 0) {
            for (let i = 0; i < 10; i++)
                html += '<input type="checkbox" id="id_' + initial + '_' + locations[i][initial] + '" class="checkbox_' + initial + '"' + (clicked_locations.includes(locations[i][initial]) ? ' checked' : '') + '/><label for="id_' + initial + '_' + locations[i][initial] + '">' + locations[i][initial] + ' (' + locations[i]['count'] + ')</label> <br>';
        }
        else {
            locations = locations.filter(item => item[initial].toLowerCase().includes($(this).val().toLowerCase()));
            for (let i = 0; i < locations.length; i++)
                html += '<input type="checkbox" id="id_' + initial + '_' + locations[i][initial] + '" class="checkbox_' + initial + '"' + (clicked_locations.includes(locations[i][initial]) ? ' checked' : '') + '/><label for="id_' + initial + '_' + locations[i][initial] + '">' + locations[i][initial] + ' (' + locations[i]['count'] + ')</label> <br>';
        }
        $("#div_filter_" + initial).html(html);
        on_click_location_checkboxes("location");
    });
}
function on_click_location_checkboxes(initial) {
    $(".checkbox_" + initial).on('click', function () {
        let name = $(this).prop('id').substring(4 + initial.length);
        let filters_applied = $("#id_filters_applied");

        if ($(this).prop('checked')) {
            clicked_locations.push(name);
            let html = '<div id="id_filter_' + initial + '_' + name + '" class="f_l_f_a_item filter_' + initial + '">' + name + '<img class="f_list_fr_close" src="/static/product/custom/imgs/close.png"/></div>';
            if (filters_applied.html().includes("No Filters Applied")) {
                filters_applied.html(html);
            }
            else {
                let new_feature = document.createElement('div');
                new_feature.innerHTML = html;
                document.getElementById('id_filters_applied').appendChild(new_feature);
            }
        }
        else {
            clicked_locations = clicked_locations.filter(item => item !== name);
            let start = name.split(' ')[0];
            $("[id^=id_filter_" + initial + "_" + start + "]").remove();
        }

        on_click_applied_location("location");

        $("#params").attr('url', make_url("locations", name, clicked_locations));
        ajax_get_vehicles();
    });
}
function on_click_applied_location(initial) {
    $(".filter_" + initial).on('click', function () {
        let name = $(this).prop('id').substring(11 + initial.length);
        let start = name.split(' ')[0];
        $("[id^=id_" + initial + "_" + start + "]").prop('checked', false);

        clicked_locations = clicked_locations.filter(item => item !== name);

        $("[id^=id_filter_" + initial + "_" + start + "]").remove();

        $("#params").attr('url', make_url("locations", name, clicked_locations));
        ajax_get_vehicles();
    });
}