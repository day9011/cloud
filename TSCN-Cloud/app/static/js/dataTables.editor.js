/*!
 * File:        dataTables.editor.js
 * Version:     0.1
 * Author:      Chengbing
 */
(function($) {

i18n = {
    create: {
        button: "添加",
        title:  "添加记录",
        submit: "添加"
    },
    edit: {
        button: "编辑",
        title:  "编辑数据",
        submit: "更新"
    },
    remove: {
        button: "删除",
        title:  "删除记录",
        submit: "删除",
        confirm: "是否删除 {0} 条选中的记录？"
    },
    error: {
        system: "系统错误，请联系管理员！",
        field: "输入类型错误，请检查！",
        invalidExp: "非法的正则表达式"
    }
};

$.fn.dataTable.Editor = function(options){
    var self = this;
    var defaults = {
        ajax: {
            "url": "",
            "type": ""
        },
        table: "",
        settings: "",
        fields: [],
        i18n: i18n
    }
    var settings = $.extend(defaults, options);
    // data related
    self.d = {};
    self.m = {};
    // datatable selector
    self.d.dom = settings.table;
    self.d.url = settings.ajax.url;
    self.d.type = settings.ajax.type;
    self.d.fields = settings.fields;
    self.d.action = "";
    self.d.dataId = "";
    self.d.idSrc = settings.idSrc;
    self.d.data = "";
    // modal window
    self.m.title = null;
    self.m.btnTxt = null;
    self.m.btnFn = null;
    self.m.id = "DT_ED_WD";
    self.m.selector = 'body #' + self.m.id;
    self.m.btnId = 'DT_ED_WD_BTN';
    self.m.formId = 'DT_ED_WD_FORM';
    self.m.statusId = 'DT_ED_WD_STAUS';
    self.m.formSelector = self.m.selector  + ' #' + self.m.formId;
    self.m.btnSelector = self.m.selector + ' #' + self.m.btnId;
    self.m.statusSelector = self.m.selector + ' #' + self.m.statusId;
    self.m.className = null;
    //language
    self.i18n = settings.i18n;

    // editor object method
    self.init = create_window.bind(self);
    self.title = title.bind(self);
    self.buttons = buttons.bind(self);
    // add data
    self.create = create.bind(self);
    // edit data
    self.edit = edit.bind(self);
    // remove data
    self.remove = remove.bind(self);
    // submit form data
    self.submit = submit.bind(self);
}

function create_window(contents)
{
    var self = this;
    var wd_body;
    var action = self.d.action || 'create';
    try{
        var wd_title = self.m.title || self.i18n[action].title;
        var wd_btn = self.m.btnTxt || self.i18n[action].submit;
    }catch(e){
        alert('非法的action！');
    }
    var btnClassName = $.trim(self.m.className) || 'btn-primary';
    html = '<div class="modal fade" id="'+$.trim(self.m.id)+'" tabindex="-1" style="top:0px;" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">' +
    '<div class="modal-dialog" style="margin-top:70px;">' +
        '<div class="modal-content">' +
            '<div class="modal-header">' +
                '<button type="button" class="close" data-dismiss="modal" aria-hidden="false">x</button>' +
                    '<h4 class="modal-title">'+ $.trim(wd_title) +'</h4>' +
            '</div>' +
            '<div class="modal-body">' +
            contents +
            '</div>' +
            '<div class="modal-footer">' +
                '<div id="'+$.trim(self.m.statusId)+'" style="display:none;font-size:14px;"></div>' +
                '<button type="button" class="btn '+$.trim(btnClassName)+'" id="'+$.trim(self.m.btnId)+'">' + $.trim(wd_btn) +'</button>' +
            '</div>' +
        '</div>' +
    '</div>' +
    '</div>';
    $(self.m.selector).remove();
    $('body').append(html);
}

// set modal window title
function title(boxTitle)
{
    var self = this;
    self.m.title = $.trim(boxTitle);
    return self;
}

// set modal window button
function buttons(options)
{
    var self = this;
    if (typeof options.label != 'undefined'){
        self.m.btnTxt = $.trim(options.label);
    }
    if (typeof options.className != 'undefined'){
        self.m.className = $.trim(options.className);   
    }
    if ($.isFunction(options.fn)){
        self.m.btnFn = options.fn;
    }else{
        self.m.btnFn = function(){alert('未指定有效的function!');}
    }
    return self;
}

// create data
function create()
{
    var self = this;
    self.d.action = 'create';
    self.d.data = null;
    var contents = gen_content(self.d.fields, null, self.m.formId, self.d.action);
    self.init(contents);
    $(self.m.btnSelector).click(self.m.btnFn);
    $(self.m.selector).modal();
}

//edit data
function edit(row)
{
    var self = this;
    self.d.action = 'edit';
    var data = get_data(self.d.dom, row);
    if(data.length == 0){
        alert('获取datatable数据失败!');
       return false; 
    }
    self.d.data = data =  data[0];
    self.d.dataId = data[self.d.idSrc];
    var contents = gen_content(self.d.fields, data, self.m.formId, self.d.action);
    self.init(contents);
    $(self.m.btnSelector).click(self.m.btnFn);
    $(self.m.selector).modal();
}

//remove data
function remove(rows){
    var self = this;
    self.d.action = 'remove';
    var data = get_data(self.d.dom, rows);
    if(data.length == 0){
        alert('获取datatable数据失败!');
       return false; 
    }
    self.d.data = data;
    self.init(self.i18n.remove.confirm.format(data.length));
    $(self.m.btnSelector).click(self.m.btnFn);
    $(self.m.selector).modal();
}

// submit form data
function submit()
{
    var self = this;
    var formData = "";
    var fields = self.d.fields;
    if(self.d.action == 'create' || self.d.action == 'edit'){
        if(self.d.action == 'create'){
            formData = 'action='+$.trim(self.d.action);
        }
        else{
            formData = 'action='+self.d.action+'&id='+$.trim(self.d.dataId);
        }
        try{
            var from_has_error = false;
            // reset error msg
            show_submit_error(self);
            for(var k in fields){
                var name = fields[k].name;
                // input type
                if(typeof fields[k].type == 'undefined'){
                    var input_value = $.trim($(self.m.formSelector+' #IN_'+name).val());
                    // if defined filter, check if the input value is valid
                    if(fields[k].filter){
                        // if define filter, check the input value using regexp
                        try{
                            var msg = fields[k].filter.msg || settings.i18n.error.field;
                            var re = new RegExp(fields[k].filter.regExp);
                            if(!re.test(input_value)){
                                //invalid input
                                show_submit_error(self, msg, name, true);
                                from_has_error = true;
                            }else{
                                //valid input
                                formData += '&data['+name+']='+input_value;
                            }
                        }catch(e){
                            //invalid regExp
                            throw new Error(self.i18n.error.invalidExp);
                        }
                    }else{
                        // if not define filter, use the input value directly
                        formData += '&data['+name+']='+input_value;
                    }                
                }else if(fields[k].type.toLowerCase() == 'select'){
                    // type is select
                    var selected_value = $(self.m.formSelector+' #IN_'+name).find('option:selected').val();
                    formData += '&data['+name+']='+$.trim(selected_value);
                }
            }
            if(from_has_error){
                return false;
            }
        }
        catch(e){
            alert(e.message);
            return false;
        }
    }
    else if(self.d.action == 'remove'){
        var removeData = self.d.data;
        formData = 'action=' + $.trim(self.d.action);
        for(var i = 0; i<removeData.length; i++){
            formData += '&id[]=' + $.trim(removeData[i][self.d.idSrc]);
        }
    }

    //submit form data
    $.ajax({
        url: self.d.url,
        type: self.d.type,
        data: formData,
        dataType:'json'
    }).done(function(data){
        if(typeof data.error != 'undefined'){
            // return data has error
            show_submit_error(self, data.error);
        }else if(typeof data.fieldErrors != 'undefined'){
            // return data has fieldErrors
            for(var k in data.fieldErrors){
                show_submit_error(self, data.fieldErrors[k].status, data.fieldErrors[k].name, true);
            }
        }
        else
        {
            // success
            $(self.m.selector).modal('hide');
            $(self.d.dom).DataTable().draw(false);
        }
    }).fail(function(data){
        show_submit_error(self, self.i18n.error.system)
        return false;
    });
}

// show error msg to editor user
function show_submit_error(editorObj, msg, name, keepFieldError){
    var self = editorObj;
    $status_dom = $(self.m.statusSelector);
    $filed_err_dom =$(self.m.formSelector + ' div.show_field_err');
    // if msg is undefined, clear field error and status error
    if(!msg){
        $filed_err_dom.empty().fadeOut('fast').parent().removeClass('has-error');
        $status_dom.empty().fadeOut('fast');
        return null;
    }
    if(!keepFieldError){
        $filed_err_dom.empty().fadeOut('fast').parent().removeClass('has-error');
    }
    if(name){
        $(self.m.formSelector + ' #ERR_' + name).text(msg).fadeIn('fast')
            .parent().addClass('has-error');        
    }else{
        //clear field error msg
        $status_dom.css('color', '#ff0000').text(msg).fadeIn('fast');
    }
    $(self.m.selector + ' .modal-dialog').shake(2, 7, 300);
}

// generate content for modal window from editor fields
function gen_content(fields, data, formId, type)
{
    var contents = '<form role="form" id="'+formId+'" class="form-horizontal">';
    for(var i=0; i<fields.length; i++){
        if(fields[i].edit == false && type == "edit"){
            continue;
        }
        if(typeof fields[i].type == 'undefined'){
            var label = fields[i].label;
            var name = fields[i].name;
            var default_value = fields[i].default;
            if(default_value == null){
                default_value = "";
            }
            var value = (type == "create") ? default_value : data[name];
            contents += '<div class="form-group">' +
                '<label for="IN_'+name+'" class="col-sm-2 control-label">'+label+'</label>' +
                '<div class="col-sm-10"><input type="text" class="form-control" id="IN_'+name+'" name="'+name+'" value="'+value+'" />' +
                '<div id="ERR_'+name+'" class="show_field_err" style="color:#ff0000; display:none;"></div>' +
                '</div>' +
                '</div>';
        }
        else if(fields[i].type.toLowerCase() == 'select'){
            var options = "";
            var selected = (type == "create") ? "" : 'selected="true"'
            var selectedValue = (type == "create") ? null : data[fields[i].name];
            for(var j=0; j<fields[i].ipOpts.length; j++){
                var value = fields[i].ipOpts[j].value;
                var label = fields[i].ipOpts[j].label;
                if(value == selectedValue){
                    options += '<option value="'+value+'" '+selected+'>'+label+'</option>';
                }
                else{
                    options += '<option value="'+value+'">'+label+'</option>';   
                }
            }
            contents += '<div class="form-group">' +
                '<label class="col-sm-2 control-label">'+fields[i].label+'</label>' +
                '<div class="col-sm-10">' +
                '<select class="form-control" id="IN_'+fields[i].name+'" name="'+fields[i].name+'">' +
                options +
                '</select>' +
                '</div>' +
                '</div>';
        }
    }
    contents += '</form>'
    return contents;
}

// get data from datatable
// this may contain multi row data
function get_data(tableSelector, rows)
{
    var data = [];
    var return_data = $(tableSelector).DataTable().rows(rows).data();
    for(var i=0; i<return_data.length; i++){
        data.push(return_data[i]);
    }
    return data;
}

})(jQuery);
