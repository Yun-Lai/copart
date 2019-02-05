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
    if($("#params").attr('url').includes('sort=') === false){
        console.log('Ajax params: ' + params);
        params += "&sort={'sort_by':'year','sort_type':'desc'}";
    }
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
    $("th[class='h'] span").attr('style', 'cursor:pointer');

    if($("#params").attr('url').includes('sort=')){
        console.log('param: ', $("#params").attr('url'));
        let param = $("#params").attr('url').split('sort=')[1];
        console.log(param.split('&')[0]);
        param = JSON.parse(param.split('&')[0]);
        console.log(param.sort_by);
        $("th[class='h'][id!='lots_" + param.sort_by + "']").attr('sorting_1', 'disabled');
        $("th[class='h'][id!='lots_" + param.sort_by + "']").removeAttr('sort_type');
        $("th[class='h'][id!='lots_" + param.sort_by + "'] span i").attr('class', 'glyphicon glyphicon-sort');

        $("th[class='h'][id='lots_" + param.sort_by + "']").attr({
                sort_type:param.sort_type,
                sorting_1: 'enabled'
            });
        if(param.sort_type === "desc"){
            $("th[class='h'][id='lots_" + param.sort_by + "'] span i").attr('class', 'glyphicon glyphicon-sort-by-attributes-alt');

        }
        else{
            $("th[class='h'][id='lots_" + param.sort_by + "'] span i").attr('class', 'glyphicon glyphicon-sort-by-attributes');
        }
    }
    else{ // None of Sorting
        $("th[class='h']").attr('sorting_1', 'disabled');
        $("th[class='h']").removeAttr('sort_type');
    }

    // data table load
    if (jQuery("#f_list_page_mark").val() === "1") {
        jQuery('#c_seach_tb').DataTable({
            "lengthMenu": [[100], [100]],
            pagerPosition: 'both',
            "ordering": false
            // "order": [[1, "desc"]],
        });
    }

    jQuery(".h span").on('click', function (e) {
        // if(e.target !==this){
        //     return;
        // }
        console.log('Theader Click event OK! --' + $(this).parent().attr('id'));
        let status;
        if($(this).parent().attr('sort_type')){
            if('asc' === $(this).parent().attr('sort_type')){
                console.log('Descending');
                status = 'desc';
            }
            else if('desc' === $(this).parent().attr('sort_type')){
                console.log('Ascending');
                status = 'asc'
            }
            // $(this).attr('sort_type', status)
        }
        //initial status
        else{
            status = 'desc';
            // $(this).attr('sort_type', 'desc')
        }

        /// back end
        var sort_by = $(this).parent().attr('id').split('lots_')[1];
        let current_url = $("#params").attr('url');
        console.log('aaaaaaaaaa', current_url);
        let params = current_url.split('&');
        for (let i = 0; i < params.length; i++) {
            if (params[i].startsWith('sort=') || params[i] === "" ) {
                console.log('delete ---', params);
                params.splice(i, 1);
            }
        }
        console.log(params);
        params.push('sort={\"sort_by\":\"'+sort_by +'\", \"sort_type\":\"'+ status + '\"}');
        console.log('param2-- ', params);
        params = params.join('&');
        console.log('param3-- ', params);
        $("#params").attr('url', params);
        // ajax_get_vehicles();

        let initial_params = $("#initial").attr('initial');
        // let params = $("#params").attr('url');
        let shows_status = $("#shows").attr('status');
        if (params)
            params = '&' + params;
        let path = encodeURI('/lots_by_search/?' + initial_params + params + '&status=' + shows_status);
        console.log(path);
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



    });
    // var sort = $("#sort").val();
    //  $.ajax({
    //   url:'fetch_details.php',
    //   type:'post',
    //   data:{columnName:columnName,sort:sort},
    //   success: function(response){
    //
    //    $("#empTable tr:not(:first)").remove();
    //
    //    $("#empTable").append(response);
    //    if(sort == "asc"){
    //      $("#sort").val("desc");
    //    }else{
    //      $("#sort").val("asc");
    //    }
    //
    //   }
    //  });

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

    change_sales_date_filter_input("sale_date");
    on_click_sale_date_checkboxes("sale_date");
    on_click_applied_sale_date("sale_date");
    change_engine_type_filter_input("engine_type");
    on_click_engine_type_checkboxes("engine_type");
    on_click_applied_engine_type("engine_type");
    change_transmission_filter_input("transmission");
    on_click_transmission_checkboxes("transmission");
    on_click_applied_transmission("transmission");
    change_drive_train_filter_input("drive_train");
    on_click_drive_train_checkboxes("drive_train");
    on_click_applied_drive_train("drive_train");
    change_cylinder_filter_input("cylinder");
    on_click_cylinder_checkboxes("cylinder");
    on_click_applied_cylinder("cylinder");

    change_fuel_filter_input("fuel");
    on_click_fuel_checkboxes("fuel");
    on_click_applied_fuel("fuel");

    change_body_style_filter_input("body_style");
    on_click_body_style_checkboxes("body_style");
    on_click_applied_body_style("body_style");

    change_vehicle_type_filter_input("vehicle");
    on_click_vehicle_type_checkboxes("vehicle");
    on_click_applied_vehicle_type("vehicle");

    change_damage_filter_input("damage");
    on_click_damage_checkboxes("damage");
    on_click_applied_damage("damage");

    change_doctype_filter_input("doctype");
    on_click_doctype_checkboxes("doctype");
    on_click_applied_doctype("doctype");


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
            for (let i = 0; i < all_years_for_filter.length; i++)
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
            for (let i = 0; i < locations.length; i++)
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

// ////////////////////////

let clicked_sale_dates = applied_filter_sale_dates;
function change_sales_date_filter_input(initial) {
    $("#input_filter_" + initial).on('input', function () {
        if ($(this).val().length === 1)
            return;

        let html = "";
        let sale_dates = all_sale_dates_for_filter;
        let to = sale_dates.length >10 ? 10 : sale_dates.length;
        if ($(this).val().length === 0) {
            for (let i = 0; i < sale_dates.length; i++)
                html += '<input type="checkbox" id="id_' + initial + '_' + sale_dates[i]['sale_day'] + '" class="checkbox_' + initial + '"' + (clicked_sale_dates.includes(sale_dates[i]['sale_day']) ? ' checked' : '') + '/><label for="id_' + initial + '_' + sale_dates[i]['sale_day'] + '">' + sale_dates[i]['sale_day'] + ' (' + sale_dates[i]['count'] + ')</label> <br>';
        }
        else {
            sale_dates = sale_dates.filter(item => item['sale_day'].toLowerCase().includes($(this).val().toLowerCase()));
            for (let i = 0; i < sale_dates.length; i++)
                html += '<input type="checkbox" id="id_' + initial + '_' + sale_dates[i]['sale_day'] + '" class="checkbox_' + initial + '"' + (clicked_sale_dates.includes(sale_dates[i]['sale_day']) ? ' checked' : '') + '/><label for="id_' + initial + '_' + sale_dates[i]['sale_day'] + '">' + sale_dates[i]['sale_day'] + ' (' + sale_dates[i]['count'] + ')</label> <br>';
        }
        $("#div_filter_" + initial).html(html);
        on_click_sale_date_checkboxes("sale_date");
    });
}
function on_click_sale_date_checkboxes(initial) {
    $(".checkbox_" + initial).on('click', function () {
        let name = $(this).prop('id').substring(4 + initial.length);
        console.log('2th name: ' + name);
        let filters_applied = $("#id_filters_applied");

        let tab_name = name.replace(/_/g, '/');

        if ($(this).prop('checked')) {
            clicked_sale_dates.push(tab_name);
            let html = '<div id="id_filter_' + initial + '_' + name + '" class="f_l_f_a_item filter_' + initial + '">' + tab_name + '<img class="f_list_fr_close" src="/static/product/custom/imgs/close.png"/></div>';
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
            clicked_sale_dates = clicked_sale_dates.filter(item => item !== tab_name);
            // let start = name.split(' ')[0];
            $("[id=\"id_filter_" + initial + "_" + name + "\"]").remove();
        }

        on_click_applied_sale_date("sale_date");

        $("#params").attr('url', make_url("sale_dates", name, clicked_sale_dates));
        ajax_get_vehicles();
    });
}
function on_click_applied_sale_date(initial) {
    $(".filter_" + initial).on('click', function () {
        let name = $(this).prop('id').substring(11 + initial.length);
        console.log('3th name: ' + name);
        let tab_name = name.replace(/_/g, '/');
        // let start = name.split(' ')[0];
        $("[id=\"id_" + initial + "_" + name + "\"]").prop('checked', false);

        clicked_sale_dates = clicked_sale_dates.filter(item => item !== tab_name);

        $("[id=\"id_filter_" + initial + "_" + name + "\"").remove();

        $("#params").attr('url', make_url("sale_dates", name, clicked_sale_dates));
        ajax_get_vehicles();
    });
}


let clicked_engine_types = applied_filter_engine_types;
function change_engine_type_filter_input(initial) {
    $("#input_filter_" + initial).on('input', function () {
        // if ($(this).val().length === 1)
        //     return;

        let html = "";
        let filters = all_engine_types_for_filter;
        let to = filters.length > 10 ? 10: filters.length;
        if ($(this).val().length === 0) {
            for (let i = 0; i < filters.length; i++)
                html += '<input type="checkbox" id="id_' + initial + '_' + filters[i][initial] + '" class="checkbox_' + initial + '"' + (clicked_engine_types.includes(filters[i][initial]) ? ' checked' : '') + '/><label for="id_' + initial + '_' + filters[i][initial] + '">' + filters[i][initial] + ' (' + filters[i]['count'] + ')</label> <br>';
        }
        else {
            filters = filters.filter(item => item[initial].toLowerCase().includes($(this).val().toLowerCase()));
            for (let i = 0; i < filters.length; i++)
                html += '<input type="checkbox" id="id_' + initial + '_' + filters[i][initial] + '" class="checkbox_' + initial + '"' + (clicked_engine_types.includes(filters[i][initial]) ? ' checked' : '') + '/><label for="id_' + initial + '_' + filters[i][initial] + '">' + filters[i][initial] + ' (' + filters[i]['count'] + ')</label> <br>';
        }
        $("#div_filter_" + initial).html(html);
        on_click_engine_type_checkboxes("engine_type");
    });
}
function on_click_engine_type_checkboxes(initial) {
    $(".checkbox_" + initial).on('click', function () {
        let name = $(this).prop('id').substring(4 + initial.length);
        let filters_applied = $("#id_filters_applied");

        let tab_name = name.replace(/-/g, '.');

        if ($(this).prop('checked')) {
            clicked_engine_types.push(tab_name);
            let html = '<div id="id_filter_' + initial + '_' + name + '" class="f_l_f_a_item filter_' + initial + '">' + tab_name + '<img class="f_list_fr_close" src="/static/product/custom/imgs/close.png"/></div>';
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
            clicked_engine_types = clicked_engine_types.filter(item => item !== tab_name);
            let start = name.split(' ')[0];
            $("[id^=id_filter_" + initial + "_" + start + "]").remove();
        }

        on_click_applied_engine_type("engine_type");

        $("#params").attr('url', make_url("engine_types", name, clicked_engine_types));
        ajax_get_vehicles();
    });
}
function on_click_applied_engine_type(initial) {
    $(".filter_" + initial).on('click', function () {
        let name = $(this).prop('id').substring(11 + initial.length);
        let start = name.split(' ')[0];

        let tab_name = name.replace(/-/g, '.');

        $("[id^=id_" + initial + "_" + start + "]").prop('checked', false);

        clicked_engine_types = clicked_engine_types.filter(item => item !== tab_name);

        $("[id^=id_filter_" + initial + "_" + start + "]").remove();

        $("#params").attr('url', make_url("engine_types", name, clicked_engine_types));
        ajax_get_vehicles();
    });
}

let clicked_transmissions = applied_filter_transmissions;
function change_transmission_filter_input(initial) {
    $("#input_filter_" + initial).on('input', function () {
        if ($(this).val().length === 1)
            return;

        let html = "";
        let filters = all_transmissions_for_filter;
        let to = filters.length > 10 ? 10 : filters.length;
        if ($(this).val().length === 0) {
            for (let i = 0; i < filters.length; i++)
                html += '<input type="checkbox" id="id_' + initial + '_' + filters[i][initial] + '" class="checkbox_' + initial + '"' + (clicked_transmissions.includes(filters[i][initial]) ? ' checked' : '') + '/><label for="id_' + initial + '_' + filters[i][initial] + '">' + filters[i][initial] + ' (' + filters[i]['count'] + ')</label> <br>';
        }
        else {
            filters = filters.filter(item => item[initial].toLowerCase().includes($(this).val().toLowerCase()));
            for (let i = 0; i < filters.length; i++)
                html += '<input type="checkbox" id="id_' + initial + '_' + filters[i][initial] + '" class="checkbox_' + initial + '"' + (clicked_transmissions.includes(filters[i][initial]) ? ' checked' : '') + '/><label for="id_' + initial + '_' + filters[i][initial] + '">' + filters[i][initial] + ' (' + filters[i]['count'] + ')</label> <br>';
        }
        $("#div_filter_" + initial).html(html);
        on_click_transmission_checkboxes("transmission");
    });
}
function on_click_transmission_checkboxes(initial) {
    $(".checkbox_" + initial).on('click', function () {
        let name = $(this).prop('id').substring(4 + initial.length);
        let filters_applied = $("#id_filters_applied");

        console.log('2th name: ' + name);

        if ($(this).prop('checked')) {
            clicked_transmissions.push(name);
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
            clicked_transmissions = clicked_transmissions.filter(item => item !== name);
            let start = name.split(' ')[0];
            $("[id^=id_filter_" + initial + "_" + start + "]").remove();
        }

        on_click_applied_transmission("transmission");

        $("#params").attr('url', make_url("transmissions", name, clicked_transmissions));
        ajax_get_vehicles();
    });
}
function on_click_applied_transmission(initial) {
    $(".filter_" + initial).on('click', function () {
        let name = $(this).prop('id').substring(11 + initial.length);
        let start = name.split(' ')[0];

        console.log('3th name: ' + name);

        $("[id^=id_" + initial + "_" + start + "]").prop('checked', false);

        clicked_transmissions = clicked_transmissions.filter(item => item !== name);

        $("[id^=id_filter_" + initial + "_" + start + "]").remove();

        $("#params").attr('url', make_url("transmissions", name, clicked_transmissions));
        ajax_get_vehicles();
    });
}

let clicked_drive_trains = applied_filter_drive_trains;
function change_drive_train_filter_input(initial) {
    $("#input_filter_" + initial).on('input', function () {
        if ($(this).val().length === 1)
            return;

        let html = "";
        let filters = all_drive_trains_for_filter;
        var to = filters.length >10 ? 10 : filters.length;
        console.log(filters);
        if ($(this).val().length === 0) {
            for (let i = 0; i < filters.length; i++){

                let search_name = filters[i]['drive'].replace('_', '/');
                html += '<input type="checkbox" id="id_' + initial + '_' + filters[i]['drive'] + '" class="checkbox_' + initial + '"' + (clicked_drive_trains.includes(filters[i]['drive']) ? ' checked' : '') + '/><label for="id_' + initial + '_' + filters[i]['drive'] + '">' + search_name + ' (' + filters[i]['count'] + ')</label> <br>';
            }

        }
        else {
            console.log('key presss....');
            filters = filters.filter(item => item['drive'].replace('_', '/').toLowerCase().includes($(this).val().toLowerCase()));
            for (let i = 0; i < filters.length; i++){
                let search_name = filters[i]['drive'].replace('_', '/');
                html += '<input type="checkbox" id="id_' + initial + '_' + filters[i]['drive'] + '" class="checkbox_' + initial + '"' + (clicked_drive_trains.includes(filters[i]['drive']) ? ' checked' : '') + '/><label for="id_' + initial + '_' + filters[i]['drive'] + '">' + search_name + ' (' + filters[i]['count'] + ')</label> <br>';
            }

        }
        $("#div_filter_" + initial).html(html);
        on_click_drive_train_checkboxes("drive_train");
    });
}
function on_click_drive_train_checkboxes(initial) {
    $(".checkbox_" + initial).on('click', function () {
        let name = $(this).prop('id').substring(4 + initial.length);
        let filters_applied = $("#id_filters_applied");

        let tab_name = name.replace('_', '/');

        console.log('2th name: ' + name);

        if ($(this).prop('checked')) {
            clicked_drive_trains.push(tab_name);
            let html = '<div id="id_filter_' + initial + '_' + name + '" class="f_l_f_a_item filter_' + initial + '">' + tab_name + '<img class="f_list_fr_close" src="/static/product/custom/imgs/close.png"/></div>';
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
            clicked_drive_trains = clicked_drive_trains.filter(item => item !== tab_name);
            // let start = name.split(' ')[0];
            $("[id=\"id_filter_" + initial + "_" + name + "\"]").remove();
        }

        on_click_applied_drive_train("drive_train");

        $("#params").attr('url', make_url("drive_trains", name, clicked_drive_trains));
        ajax_get_vehicles();
    });
}
function on_click_applied_drive_train(initial) {
    $(".filter_" + initial).on('click', function () {
        let name = $(this).prop('id').substring(11 + initial.length);
        // let start = name.split(' ')[0];

        let tab_name = name.replace('_', '/');
        console.log('3th name: ' + name);

        $("[id=\"id_" + initial + "_" + name + "\"]").prop('checked', false);

        clicked_drive_trains = clicked_drive_trains.filter(item => item !== tab_name);

        $("[id=\"id_filter_" + initial + "_" + name + "\"]").remove();

        $("#params").attr('url', make_url("drive_trains", name, clicked_drive_trains));
        ajax_get_vehicles();
    });
}

let clicked_cylinders = applied_filter_cylinders;
function change_cylinder_filter_input(initial) {
    $("#input_filter_" + initial).on('input', function () {
        // if ($(this).val().length === 1)
        //     return;

        let html = "";
        let filters = all_cylinders_for_filter;
        if ($(this).val().length === 0) {
            console.log(filters);
            var to = filters.length > 10 ? 10 : filters.length;
            for (let i = 0; i < filters.length; i++)
                html += '<input type="checkbox" id="id_' + initial + '_' + filters[i]['cylinders'] + '" class="checkbox_' + initial + '"' + (clicked_cylinders.includes(filters[i]['cylinders']) ? ' checked' : '') + '/><label for="id_' + initial + '_' + filters[i]['cylinders'] + '">' + filters[i]['cylinders'] + ' (' + filters[i]['count'] + ')</label> <br>';
        }
        else {
            filters = filters.filter(item => String(item['cylinders']).toLowerCase().includes($(this).val().toLowerCase()));
            for (let i = 0; i < filters.length; i++)
                html += '<input type="checkbox" id="id_' + initial + '_' + filters[i]['cylinders'] + '" class="checkbox_' + initial + '"' + (clicked_cylinders.includes(filters[i]['cylinders']) ? ' checked' : '') + '/><label for="id_' + initial + '_' + filters[i]['cylinders'] + '">' + filters[i]['cylinders'] + ' (' + filters[i]['count'] + ')</label> <br>';
        }
        $("#div_filter_" + initial).html(html);
        on_click_cylinder_checkboxes("cylinder");
    });
}
function on_click_cylinder_checkboxes(initial) {
    $(".checkbox_" + initial).on('click', function () {
        let name = $(this).prop('id').substring(4 + initial.length);
        let filters_applied = $("#id_filters_applied");

        console.log('2th name: ' + name);

        if ($(this).prop('checked')) {
            clicked_cylinders.push(name);
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
            clicked_cylinders = clicked_cylinders.filter(item => item !== name);
            // let start = name.split(' ')[0];
            $("[id=\"id_filter_" + initial + "_" + name + "\"]").remove();
        }

        on_click_applied_cylinder("cylinder");

        $("#params").attr('url', make_url("cylinderss", name, clicked_cylinders));
        ajax_get_vehicles();
    });
}
function on_click_applied_cylinder(initial) {
    $(".filter_" + initial).on('click', function () {
        let name = $(this).prop('id').substring(11 + initial.length);
        // let start = name.split(' ')[0];
        console.log('3th name: ' + name);

        $("[id=\"id_" + initial + "_" + name + "\"]").prop('checked', false);

        clicked_cylinders = clicked_cylinders.filter(item => item !== name);

        $("[id=\"id_filter_" + initial + "_" + name + "\"]").remove();

        $("#params").attr('url', make_url("cylinderss", name, clicked_cylinders));
        ajax_get_vehicles();
    });
}

let clicked_fuels = applied_filter_fuels;
function change_fuel_filter_input(initial) {
    $("#input_filter_" + initial).on('input', function () {
        if ($(this).val().length === 1)
            return;

        let html = "";
        let search_res = "";
        let filters = all_fuels_for_filter;
        if ($(this).val().length === 0) {
            console.log(filters);
            filters = all_fuels_for_filter;
            var to = filters.length > 10 ? 10 : filters.length;
            for (let i = 0; i < filters.length; i++){
                search_res = filters[i].fuel.charAt(0) + filters[i].fuel.slice(1).toLowerCase();
                html += '<input type="checkbox" id="id_' + initial + '_' + filters[i][initial] + '" class="checkbox_' + initial + '"' + (clicked_fuels.includes(filters[i][initial]) ? ' checked' : '') + '/><label for="id_' + initial + '_' + filters[i].fuel + '">' + search_res + ' (' + filters[i]['count'] + ')</label> <br>';
            }
        }
        else {

            filters = filters.filter(item => item[initial].toLowerCase().includes($(this).val().toLowerCase()));
            for (let i = 0; i < filters.length; i++){
                search_res = filters[i][initial].charAt(0) + filters[i][initial].slice(1).toLowerCase();
                html += '<input type="checkbox" id="id_' + initial + '_' + filters[i][initial] + '" class="checkbox_' + initial + '"' + (clicked_fuels.includes(filters[i][initial]) ? ' checked' : '') + '/><label for="id_' + initial + '_' + filters[i][initial] + '">' + search_res + ' (' + filters[i]['count'] + ')</label> <br>';
            }
        }
        $("#div_filter_" + initial).html(html);
        on_click_fuel_checkboxes("fuel");
    });
}
function on_click_fuel_checkboxes(initial) {
    $(".checkbox_" + initial).on('click', function () {
        let name = $(this).prop('id').substring(4 + initial.length);
        let filters_applied = $("#id_filters_applied");

        console.log('2th name: ' + name);
        let tab_name = name.toLowerCase();
        tab_name = tab_name.charAt(0).toUpperCase() + tab_name.slice(1);
        console.log('2th tab_name: ' + tab_name);
        if ($(this).prop('checked')) {
            clicked_fuels.push(name);
            let html = '<div id="id_filter_' + initial + '_' + name + '" class="f_l_f_a_item filter_' + initial + '">' + tab_name + '<img class="f_list_fr_close" src="/static/product/custom/imgs/close.png"/></div>';
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
            clicked_fuels = clicked_fuels.filter(item => item !== name);
            // let start = name.split(' ')[0];
            $("[id=\"id_filter_" + initial + "_" + name + "\"]").remove();
        }

        on_click_applied_fuel("fuel");

        $("#params").attr('url', make_url("fuels", name, clicked_fuels));
        ajax_get_vehicles();
    });
}
function on_click_applied_fuel(initial) {
    $(".filter_" + initial).on('click', function () {
        let name = $(this).prop('id').substring(11 + initial.length);
        // let start = name.split(' ')[0];
        let tab_name = name.toLowerCase();
        tab_name = tab_name.charAt(0).toUpperCase() + tab_name.slice(1);
        console.log('3th name: ' + name);
        console.log('3th tab_name: ' + tab_name);

        $("[id=\"id_" + initial + "_" + name + "\"]").prop('checked', false);

        clicked_fuels = clicked_fuels.filter(item => item !== name);

        $("[id=\"id_filter_" + initial + "_" + name + "\"]").remove();

        $("#params").attr('url', make_url("fuels", name, clicked_fuels));
        ajax_get_vehicles();
    });
}

let clicked_body_styles = applied_filter_body_styles;
function change_body_style_filter_input(initial) {
    $("#input_filter_" + initial).on('input', function () {
        if ($(this).val().length === 1)
            return;

        let html = "";
        let search_res = "";
        let filters = all_body_styles_for_filter;
        if ($(this).val().length === 0) {
            filters = all_body_styles_for_filter;
            var to = filters.length > 10 ? 10 : filters.length;
            for (let i = 0; i < filters.length; i++){
                search_res = filters[i].body_style.charAt(0) + filters[i].body_style.slice(1).toLowerCase();
                html += '<input type="checkbox" id="id_' + initial + '_' + filters[i][initial] + '" class="checkbox_' + initial + '"' + (clicked_body_styles.includes(filters[i][initial]) ? ' checked' : '') + '/><label for="id_' + initial + '_' + filters[i].body_style + '">' + search_res + ' (' + filters[i]['count'] + ')</label> <br>';
            }
        }
        else {

            filters = filters.filter(item => item[initial].toLowerCase().includes($(this).val().toLowerCase()));
            for (let i = 0; i < filters.length; i++){
                search_res = filters[i][initial].charAt(0) + filters[i][initial].slice(1).toLowerCase();
                html += '<input type="checkbox" id="id_' + initial + '_' + filters[i][initial] + '" class="checkbox_' + initial + '"' + (clicked_body_styles.includes(filters[i][initial]) ? ' checked' : '') + '/><label for="id_' + initial + '_' + filters[i][initial] + '">' + search_res + ' (' + filters[i]['count'] + ')</label> <br>';
            }
        }
        $("#div_filter_" + initial).html(html);
        on_click_body_style_checkboxes("body_style");
    });
}
function on_click_body_style_checkboxes(initial) {
    $(".checkbox_" + initial).on('click', function () {
        let name = $(this).prop('id').substring(4 + initial.length);
        let filters_applied = $("#id_filters_applied");

        console.log('2th name: ' + name);
        let tab_name = name.toLowerCase();
        tab_name = tab_name.charAt(0).toUpperCase() + tab_name.slice(1);
        console.log('2th tab_name: ' + tab_name);
        if ($(this).prop('checked')) {
            clicked_body_styles.push(name);
            let html = '<div id="id_filter_' + initial + '_' + name + '" class="f_l_f_a_item filter_' + initial + '">' + tab_name + '<img class="f_list_fr_close" src="/static/product/custom/imgs/close.png"/></div>';
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
            clicked_body_styles = clicked_body_styles.filter(item => item !== name);
            // let start = name.split(' ')[0];
            $("[id=\"id_filter_" + initial + "_" + name + "\"]").remove();
        }

        on_click_applied_body_style("body_style");

        $("#params").attr('url', make_url("body_styles", name, clicked_body_styles));
        ajax_get_vehicles();
    });
}
function on_click_applied_body_style(initial) {
    $(".filter_" + initial).on('click', function () {
        let name = $(this).prop('id').substring(11 + initial.length);
        // let start = name.split(' ')[0];
        let tab_name = name.toLowerCase();
        tab_name = tab_name.charAt(0).toUpperCase() + tab_name.slice(1);
        console.log('3th name: ' + name);
        console.log('3th tab_name: ' + tab_name);

        $("[id=\"id_" + initial + "_" + name + "\"]").prop('checked', false);

        clicked_body_styles = clicked_body_styles.filter(item => item !== name);

        $("[id=\"id_filter_" + initial + "_" + name + "\"]").remove();

        $("#params").attr('url', make_url("body_styles", name, clicked_body_styles));
        ajax_get_vehicles();
    });
}

let clicked_vehicle_types = applied_filter_vehicle_types;
function change_vehicle_type_filter_input(initial) {
    $("#input_filter_" + initial).on('input', function () {
        if ($(this).val().length === 1)
            return;

        let html = "";
        let search_res = "";
        let filters = all_vehicle_types_for_filter;
        if ($(this).val().length === 0) {
            console.log(filters);
            filters = all_vehicle_types_for_filter;
            var to = filters.length > 10 ? 10 : filters.length;
            for (let i = 0; i < filters.length; i++){
                html += '<input type="checkbox" id="id_' + initial + '_' + filters[i]["type"] + '" class="checkbox_' + initial + '"' + (clicked_vehicle_types.includes(filters[i]["type"]) ? ' checked' : '') + '/><label for="id_' + initial + '_' + filters[i]["type"] + '">' + filters[i]["type"] + ' (' + filters[i]['count'] + ')</label> <br>';
            }
        }
        else {

            filters = filters.filter(item => item["type"].toLowerCase().includes($(this).val().toLowerCase()));
            for (let i = 0; i < filters.length; i++){
                search_res = filters[i]["type"].charAt(0) + filters[i]["type"].slice(1).toLowerCase();
                html += '<input type="checkbox" id="id_' + initial + '_' + filters[i]["type"] + '" class="checkbox_' + initial + '"' + (clicked_vehicle_types.includes(filters[i]["type"]) ? ' checked' : '') + '/><label for="id_' + initial + '_' + filters[i]["type"] + '">' + filters[i]["type"] + ' (' + filters[i]['count'] + ')</label> <br>';
            }
        }
        $("#div_filter_" + initial).html(html);
        on_click_vehicle_type_checkboxes("vehicle_type");
    });
}
function on_click_vehicle_type_checkboxes(initial) {
    $(".checkbox_" + initial).on('click', function () {
        let name = $(this).prop('id').substring(4 + initial.length);
        let filters_applied = $("#id_filters_applied");

        console.log('2th name: ' + name);
        if ($(this).prop('checked')) {
            clicked_vehicle_types.push(name);
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
            clicked_vehicle_types = clicked_vehicle_types.filter(item => item !== name);
            // let start = name.split(' ')[0];
            $("[id=\"id_filter_" + initial + "_" + name + "\"]").remove();
        }

        on_click_applied_vehicle_type("vehicle_type");

        $("#params").attr('url', make_url("vehicle_types", name, clicked_vehicle_types));
        ajax_get_vehicles();
    });
}
function on_click_applied_vehicle_type(initial) {
    $(".filter_" + initial).on('click', function () {
        let name = $(this).prop('id').substring(11 + initial.length);
        console.log('3th name: ' + name);

        $("[id=\"id_" + initial + "_" + name + "\"]").prop('checked', false);

        clicked_vehicle_types = clicked_vehicle_types.filter(item => item !== name);

        $("[id=\"id_filter_" + initial + "_" + name + "\"]").remove();

        $("#params").attr('url', make_url("vehicle_types", name, clicked_vehicle_types));
        ajax_get_vehicles();
    });
}

let clicked_damages = applied_filter_damages;
function change_damage_filter_input(initial) {
    $("#input_filter_" + initial).on('input', function () {
        if ($(this).val().length === 1)
            return;

        let html = "";
        let search_res = "";
        let filters = all_damages_for_filter;
        if ($(this).val().length === 0) {
            filters = all_damages_for_filter;
            var to = filters.length > 10 ? 10 : filters.length;
            for (let i = 0; i < filters.length; i++){
                html += '<input type="checkbox" id="id_' + initial + '_' + filters[i]["lot_1st_damage"] + '" class="checkbox_' + initial + '"' + (clicked_damages.includes(filters[i]["lot_1st_damage"]) ? ' checked' : '') + '/><label for="id_' + initial + '_' + filters[i]["lot_1st_damage"] + '">' + filters[i]["lot_1st_damage"] + ' (' + filters[i]['count'] + ')</label> <br>';
            }
        }
        else {

            filters = filters.filter(item => item["lot_1st_damage"].toLowerCase().includes($(this).val().toLowerCase()));
            for (let i = 0; i < filters.length; i++){
                search_res = filters[i]["lot_1st_damage"].charAt(0) + filters[i]["lot_1st_damage"].slice(1).toLowerCase();
                html += '<input type="checkbox" id="id_' + initial + '_' + filters[i]["lot_1st_damage"] + '" class="checkbox_' + initial + '"' + (clicked_damages.includes(filters[i]["lot_1st_damage"]) ? ' checked' : '') + '/><label for="id_' + initial + '_' + filters[i]["lot_1st_damage"] + '">' + filters[i]["lot_1st_damage"] + ' (' + filters[i]['count'] + ')</label> <br>';
            }
        }
        $("#div_filter_" + initial).html(html);
        on_click_damage_checkboxes("damage");
    });
}
function on_click_damage_checkboxes(initial) {
    $(".checkbox_" + initial).on('click', function () {
        let name = $(this).prop('id').substring(4 + initial.length);
        let filters_applied = $("#id_filters_applied");

        console.log('2th name: ' + name);
        if ($(this).prop('checked')) {
            clicked_damages.push(name);
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
            clicked_damages = clicked_damages.filter(item => item !== name);
            // let start = name.split(' ')[0];
            $("[id=\"id_filter_" + initial + "_" + name + "\"]").remove();
        }

        on_click_applied_damage("damage");

        $("#params").attr('url', make_url("damages", name, clicked_damages));
        ajax_get_vehicles();
    });
}
function on_click_applied_damage(initial) {
    $(".filter_" + initial).on('click', function () {
        let name = $(this).prop('id').substring(11 + initial.length);
        console.log('3th name: ' + name);

        $("[id=\"id_" + initial + "_" + name + "\"]").prop('checked', false);

        clicked_damages = clicked_damages.filter(item => item !== name);

        $("[id=\"id_filter_" + initial + "_" + name + "\"]").remove();

        $("#params").attr('url', make_url("damages", name, clicked_damages));
        ajax_get_vehicles();
    });
}

let clicked_doctypes = applied_filter_doctypes;
function change_doctype_filter_input(initial) {
    $("#input_filter_" + initial).on('input', function () {
        if ($(this).val().length === 1)
            return;

        let html = "";
        let search_res = "";
        let filters = all_doctypes_for_filter;
        if ($(this).val().length === 0) {
            filters = all_doctypes_for_filter;
            var to = filters.length > 10 ? 10 : filters.length;
            for (let i = 0; i < filters.length; i++){
                html += '<input type="checkbox" id="id_' + initial + '_' + filters[i]["doc_type_td"] + '" class="checkbox_' + initial + '"' + (clicked_doctypes.includes(filters[i]["doc_type_td"]) ? ' checked' : '') + '/><label for="id_' + initial + '_' + filters[i]["doc_type_td"] + '">' + filters[i]["doc_type_td"] + ' (' + filters[i]['count'] + ')</label> <br>';
            }
        }
        else {

            filters = filters.filter(item => item["doc_type_td"].toLowerCase().includes($(this).val().toLowerCase()));
            for (let i = 0; i < filters.length; i++){
                search_res = filters[i]["doc_type_td"].charAt(0) + filters[i]["doc_type_td"].slice(1).toLowerCase();
                html += '<input type="checkbox" id="id_' + initial + '_' + filters[i]["doc_type_td"] + '" class="checkbox_' + initial + '"' + (clicked_doctypes.includes(filters[i]["doc_type_td"]) ? ' checked' : '') + '/><label for="id_' + initial + '_' + filters[i]["doc_type_td"] + '">' + filters[i]["doc_type_td"] + ' (' + filters[i]['count'] + ')</label> <br>';
            }
        }
        $("#div_filter_" + initial).html(html);
        on_click_doctype_checkboxes("doctype");
    });
}
function on_click_doctype_checkboxes(initial) {
    $(".checkbox_" + initial).on('click', function () {
        let name = $(this).prop('id').substring(4 + initial.length);
        let filters_applied = $("#id_filters_applied");

        console.log('2th name: ' + name);
        if ($(this).prop('checked')) {
            clicked_doctypes.push(name);
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
            clicked_doctypes = clicked_doctypes.filter(item => item !== name);
            // let start = name.split(' ')[0];
            $("[id=\"id_filter_" + initial + "_" + name + "\"]").remove();
        }

        on_click_applied_doctype("doctype");

        $("#params").attr('url', make_url("doctypes", name, clicked_doctypes));
        ajax_get_vehicles();
    });
}
function on_click_applied_doctype(initial) {
    $(".filter_" + initial).on('click', function () {
        let name = $(this).prop('id').substring(11 + initial.length);
        console.log('3th name: ' + name);

        $("[id=\"id_" + initial + "_" + name + "\"]").prop('checked', false);

        clicked_doctypes = clicked_doctypes.filter(item => item !== name);

        $("[id=\"id_filter_" + initial + "_" + name + "\"]").remove();

        $("#params").attr('url', make_url("doctypes", name, clicked_doctypes));
        ajax_get_vehicles();
    });
}