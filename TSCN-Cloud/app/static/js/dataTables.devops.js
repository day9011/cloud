/*! 
datatables language file
*/

dt_lang_cn = {
    "sProcessing": "正在加载中......",
    "sLengthMenu": "每页显示 _MENU_ 条记录",
    "sZeroRecords": "对不起，查询不到相关数据！",
    "sEmptyTable": "表中无数据存在！",
    "sInfo": "当前显示 _START_ 到 _END_ 条，共 _TOTAL_ 条记录",
    "sInfoFiltered": "数据表中共为 _MAX_ 条记录",
    "sSearch": "搜索: ",
    "sInfoEmpty": "当前显示 0 到 0 条，共 0 条记录",
    "oPaginate": {
        "sFirst": "首页",
        "sPrevious": "上一页",
        "sNext": "下一页",
        "sLast": "末页"
    }
};

function get_content(url, label, value)
{
    var data = [];
    $.ajax({
        url: url,
        type:'POST',
        dataType:'json',
        async:false, 
        success:function(d){
            if('status' in d || 'content' in d){
                if (d['status'] == 0) {
                    for (i = 0; i < d['content'].length; i++ ){
                        data.push({ label: d["content"][i][label], value: d["content"][i][value] });
                    }
                }
            }
        }
    });
    return data;
}

function get_content_array(url, arr, value)
{
    var data = [];
    $.ajax({
        url: url,
        type:'POST',
        dataType:'json',
        async:false,
        success:function(d){
            if('status' in d || 'content' in d){
                if (d['status'] == 0) {
                    for (var i = 0; i < d['content'].length; i++ ){
                        var label1 = "";
                        var label2 = "";
                        for (var j = 0; j < arr.length; j++  ){
                            if (j == 0){
                                label1 = d["content"][i][arr[j]];
                            }else{
                                label2 = label2 + d["content"][i][arr[j]] +" ";
                            }
                        }
                        data.push({ label: label1+"("+label2+")", value: d["content"][i][value] });
                    }
                }
            }
        }
    });
    return data;
}

function createTable(Selector, dataUrl, tableFields, operationUrl, editorFields, scrollX, options){
    var defaultOptions = {
        'edit': true,
        'remove': true,
        'lengthMenu': [[10, 25, 50], [10, 25, 50]]
    }
    var settings = $.extend(defaultOptions, options)
    var lengthMenu = settings.lengthMenu;
    var scrollX = typeof scrollX != 'undefined' ? scrollX : true;
    var startRowIndex;
    var endRowIndex;
    var shiftdown = false;
    var multiSelect = false;

    tableOptions = {
        lengthMenu: lengthMenu,
        processing: true,
        serverSide: true,
        stateSave: true,
        dom: '<"float_right"l>trpi',
        //dom: 'T<"clear">lfrtip',
        ajax: {
               "url": dataUrl,
               "type": "POST"
              },
        columns: tableFields,
        // Chinese language
        oLanguage: dt_lang_cn,
        bSort: true,
        scrollX: scrollX,
        fnDrawCallback: function(settings){
            //跳转到页码
            var table = $(Selector).DataTable();
            var pageinfo = table.page.info();
            var page = $(Selector+'_paginate');
            var current_page = pageinfo.page;
            options = ""
            for(var i=0; i<pageinfo.pages; i++){
                if(current_page == i) {
                    options += '<option value="{0}" selected="selected">{1}</option>'.format(i, i + 1);
                }else{
                    options += '<option value="{0}">{1}</option>'.format(i, i + 1);
                }
            }
            var select = '<select class="form-control" style="position: relative; top: -1px;">{0}</select>'.format(options);
            var html = '<span style="position: relative; top: -13px;margin-right: 10px;">跳转到 {0} 页</span>'.format(select);
            page.find('span').remove();
            page.prepend(html);
            page.find('select').on('change', function(){
                table.page(parseInt(this.value)).draw(false);
            });
        }
    };

    if(typeof operationUrl != 'undefined'){

        var control = '';
        if (settings.edit == true){
            control += '<a href="" class="editor_edit glyphicon glyphicon-pencil" style="font-size:14px;"></a>'
        }

        if (settings.remove == true){
           control += '<a href="" style="font-size:14px; margin-left:8px;" class="editor_remove glyphicon glyphicon-remove"></a>'
        }

        controlBtns = {
                "data": null,
                "defaultContent": control,
                "bSortable": false
        };
        //add editor buttion to row
        tableFields.push(controlBtns);

        editor = new $.fn.dataTable.Editor( {
            ajax: {
                   "url": operationUrl,
                   "type": "POST"
                  },
            table: Selector,
            idSrc: "id",
            fields: editorFields
        });

        // Edit record
        if(settings.edit == true){
            $(Selector).on('click', 'a.editor_edit', function (e) {
                e.preventDefault();
                editor.buttons({'className': 'btn-primary', 'fn': function(){editor.submit();}}).edit($(this).closest('tr'));
            });            
        }

        // Delete a record
        if(settings.remove == true){
            $(Selector).on('click', 'a.editor_remove', function (e) {
                e.preventDefault();
                editor.buttons({'className':'btn-danger', 'fn': function(){editor.submit();}}).remove($(this).closest('tr'));
            });
        }

        //table tools
        insert_table_tools(editor, Selector, {'edit': settings.edit, 'remove': settings.remove});
    }

    table = $(Selector).DataTable(tableOptions);
    if($.cookie('clearSearch') == "1"){
        table.search('').columns().search('').draw();
        $.removeCookie('clearSearch');
    }
//    $("table").bind("contextmenu",function(){return false;});
//    $("table").bind("selectstart",function(){return false;});

//    $(document).keydown(function(e){
//        if(e.keyCode == 16){
//            shiftdown = true;
//        }
//    })
//
//    $(document).keyup(function(e){
//        if(e.keyCode == 16){
//            shiftdown = false;
//        }
//    })

    $(Selector+' tbody').on( 'click', 'tr', function (e) {
        // don't select with click edit and remove buttons

        if(multiSelect){
            $(this).siblings("tr").each(function(){
                if($(this).hasClass("selected")){
                    $(this).removeClass('selected');
                }
            })
            multiSelect = false;
            startRowIndex = 0;
            endRowIndex = 0;
        }

        if(e.target.tagName.toUpperCase() != 'A'){
            $(this).toggleClass('selected');
        }

//        var selectedRow = $(Selector).DataTable().rows('.selected').data().length;
//        if(selectedRow == 1){
//            startRowIndex = $(this).context._DT_RowIndex;
//        }else if(selectedRow == 2){
//            endRowIndex = $(this).context._DT_RowIndex;
//        }else{
//            startRowIndex = 0;
//            endRowIndex = 0;
//        }
//
//        if (startRowIndex < endRowIndex && shiftdown && multiSelect == false){
//            multiSelect = true;
//            $(this).siblings("tr").each(function(){
//                var rowIndex = $(this).context._DT_RowIndex;
//                if(rowIndex > startRowIndex && rowIndex < endRowIndex){
//                    $(this).addClass('selected');
//                }
//            })
//        }else if (startRowIndex > endRowIndex && shiftdown && multiSelect == false){
//            multiSelect = true;
//            $(this).siblings("tr").each(function(){
//                var rowIndex = $(this).context._DT_RowIndex;
//                if(rowIndex > endRowIndex && rowIndex < startRowIndex){
//                    $(this).addClass('selected');
//                }
//            })
//        }

    });
}

// data_render for datatable
function data_render(dataSource, filter){
    if(typeof dataSource == 'undefined' && typeof filter == 'undefined'){
        return null;
    }
    else{
        for(var i=0; i<dataSource.length; i++){
            if(dataSource[i].value == filter){
                return dataSource[i].label;
            }
        }
        // if can not found, return null to editor
        return null;
    }
}

// insert "Add" "Edit" "Remove" before datatable
function insert_table_tools(editor, Selector, options){
    var defaultOptions = {
        "btnAdd": {"text": "新增", "className": "btn-success", "id": "DT_TOOLS_BTN_ADD" },
        "btnEdit": {"text": "编辑", "className": "btn-primary", "id": "DT_TOOLS_BTN_EDIT"},
        "btnRemove": {"text": "删除", "className": "btn-danger", "id": "DT_TOOLS_BTN_REMOVE"},
        "edit": true,
        "remove": true
    };
    // override defaultTxt
    var settings = $.extend(defaultOptions, options);
    var addSelector = '#' + settings.btnAdd.id;
    var editSelector = '#' + settings.btnEdit.id;
    var removeSelector = '#' + settings.btnRemove.id;
    var style = /chrome/.test(navigator.userAgent.toLowerCase()) ? '-45px':'0px';
    var html = '<div class="btn-group btn-group-sm" id="DT_TOOLS_BTN" style="z-index: 999; margin-bottom:'+style+'">' +
                    '<div class="btn-group btn-group-sm">' +
                    '<button type="button" class="btn '+settings.btnAdd.className+'" id="'+settings.btnAdd.id+'">'+settings.btnAdd.text+'</button>' +
                    '</div>' +
                    '<div class="btn-group btn-group-sm" style="cursor: not-allowed;">' +
                    '<button type="button" disabled="disabled" class="btn" id="'+settings.btnEdit.id+'">'+settings.btnEdit.text+'</button>' +
                    '</div>' +
                    '<div class="btn-group btn-group-sm" style="cursor: not-allowed;">' +
                    '<button type="button" disabled="disabled" class="btn" id="'+settings.btnRemove.id+'">'+settings.btnRemove.text+'</button>' +
                    '</div>' +
                    '</div>';
    $(html).insertBefore(Selector);
    // add click
    $(addSelector).click(function(e){
        editor.buttons({'className': 'btn-success', 'fn': function(){editor.submit();}}).create();
    });

    $(editSelector).click(function(){
        editor.buttons({'className': 'btn-primary', 'fn': function(){editor.submit();}}).edit($(Selector).find('tr.selected'));
    });

    $(removeSelector).click(function(){
        editor.buttons({'className':'btn-danger', 'fn': function(){editor.submit();}}).remove($(Selector).find('tr.selected'));
    });

    $(Selector).click(function(e){
        var selectedRow = $(Selector).DataTable().rows('.selected').data().length;
        // button status
        var editStatus = false;
        var removeStatus = false;

        if(selectedRow == 0){
            editStatus = false;
            removeStatus = false;
        }else if(selectedRow == 1){
            editStatus = true;
            removeStatus = true;
        }else{
            editStatus = false;
            removeStatus = true;
        }
        // check if button is enabled
        editStatus = settings.edit ? editStatus : false;
        removeStatus = settings.remove ? removeStatus : false;
        // enable or disable according selected row(s).
        enable_disable_btn(editSelector, editStatus, settings.btnEdit.className);
        enable_disable_btn(removeSelector, removeStatus, settings.btnRemove.className);
    });

    // disable edit and remove button when redraw datatable
    $(Selector).on('draw.dt', function(){
        enable_disable_btn(editSelector, false, settings.btnEdit.className);
        enable_disable_btn(removeSelector, false, settings.btnRemove.className);       
    });
}

// enable or disable table tools button
function enable_disable_btn(Selector, status, className){
    if(status == true){
        $(Selector).removeAttr('disabled')
            .removeClass('btn-disabled')
            .addClass(className)
            .parent().css('cursor', 'pointer');
    }else{
        $(Selector).attr('disabled', 'disabled')
            .removeClass(className)
            .addClass('btn-disabled')
            .parent().css('cursor', 'not-allowed');
    }
}

function filterTable(Selector){
    //分类查询
    function filterColumn ( i ){
        $(Selector).DataTable().column( i ).search(
            $('#col'+i+'_filter').val()
        ).draw();
    }

    $('input.column_filter').on( 'keyup click', function () {
        $.cookie('clearSearch', 1);
        filterColumn( $(this).parents('tr').attr('data-column') );
    });


    //伸缩查询条件
    $("#condition_show").click(function(){
        $("#query_condition").slideToggle("fast");
    });
}

// ajax submit data
function submit_data(url, data, type, dataType, callback){
    var dataType = (typeof dataType == 'undefined') ? 'json': dataType;
    $.ajax({
        url: url,
        type: type,
        data: data,
        dataType: dataType,
        success: function(d){
            callback(d);
        },
        error: function(d){
            callback(d, 1);
        }
    });
}

// modal
function modal(content){
    if(typeof content == 'string' && content == 'hide'){
        $('body>div#modal_showcontent').modal('hide');
        return;
    }
    $('body>div#modal_showcontent').remove();
    var html_raw = '' +
'<div class="modal" id="modal_showcontent">' +
'  <div class="modal-dialog">' +
'    <div class="modal-content">' +
'      <div class="modal-header">' +
'        <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>' +
'        <h4 class="modal-title">'+content.title+'</h4>' +
'      </div>' +
'      <div class="modal-body">' + content.content +
'      </div>{0}' +
'    </div><!-- /.modal-content -->' +
'  </div><!-- /.modal-dialog -->' +
'</div><!-- /.modal -->';
    // if add footer to modal window
    if(typeof content.footer == 'undefined'){
        var html = html_raw.format('<div class="modal-footer"><button type="button" class="btn btn-default" data-dismiss="modal">确定</button></div>');
    }else{
        var html = html_raw.format(' ');
    }

    // add dismiss button to footer button
    if(typeof content.callback != 'undefined' && $.isFunction(content.callback)){
        var html = html_raw.format('<div class="modal-footer"><button type="button" id="modal_show_content_btn">确定</button></div>');
    }

    // add callback to footer button
    if(typeof content.data == 'undefined'){
        content.data = ''
    }

    $('body').append(html);
    if(typeof content.callback != 'undefined' && $.isFunction(content.callback)){
        $('#modal_show_content_btn').click(function(){
            content.callback(content.data)
        });
    }
    $('body>div#modal_showcontent').modal({'backdrop': 'static'});
}

function loading(container, action, opacity){
    // show loading icon
    $container = $(container);
    var color = (typeof opacity == 'undefined') ? 0 : opacity;
    if(action == 'on'){
        var con_width = $container.width();
        var con_height = $container.height();
        $container.css('position', 'relative');
        // html
        var bg_html_raw='<div class="dynamic_loading_icon_bg" style="position: absolute;top: 0;left: 0;z-index: 3;width:{0}px;height:{1}px;background: #000;opacity: {2};"></div>';
        var fg_html_raw = '<div class="dynamic_loading_icon_fg" style="position:absolute; z-index:4; font-size:30px;  width:30px; top:{0}px; left:{1}px;"><i class="fa fa-spinner fa-spin"></i></div>';

        // generate html
        bg_html = bg_html_raw.format(con_width, con_height, color);
        fg_html = fg_html_raw.format(con_height/2-15, con_width/2-15);

        $container.find('div.dynamic_loading_icon_bg').remove();
        $container.find('div.dynamic_loading_icon_fg').remove();
        $container.prepend(bg_html);
        $container.prepend(fg_html);
    }else{
        $container.find('div.dynamic_loading_icon_bg').fadeOut('slow');
        $container.find('div.dynamic_loading_icon_fg').fadeOut('slow');        
    }
}