// @lbh 20130625
// 模板中插入umail的一些链接内容的插件

KindEditor.plugin('common_var', function(K) {
    var self = this, name = 'common_var';

    var service = K.undef(self.service, false);
    var template_id = K.undef(self.tpl_id, false);

    // var  common_var_link = K.undef(self.common_var_content, self.lang('common_var.items'));
    // var  common_var_content = K.undef(self.common_var_content, self.lang('common_var.itemDefaultContent'));
    var common_var_link = eval(self.common_var_link);
    var common_var_content = eval(self.common_var_content);

    self.plugin.common_var = {
        list : function() {
            // var link = self.lang('common_var.items');
            var link = common_var_link;
            menu = self.createMenu({
                name : 'common_var',
                width : 300,
            });
            K.each(link, function(key, val) {
                menu.addItem({
                    title : '<span style="font-size:' + val + ';" >' + val + '</span>',
                    height : 20,
                    click : function() {
                        self.plugin.common_var.insert(key);
                    }
                });
            });
        },

        // 点击图标直接插入退订链接 -- @lbh 20130620
        insert : function(key) {
            // var default_content = self.lang('common_var.itemDefaultContent');
            var default_content = common_var_content;
            var content = default_content[key];

            self.exec('inserthtml', content ).hideMenu();

        },

        'delete' : function() {
            //self.exec('unsubscribe', null);
        }

        // 点击图标直接插入退订链接 -- @lbh 20130620
        //insert : function(key) {
        //    jQuery.post("/core/ajax/common_var/", {'var_type': key}, function(data){
        //        var inserthtml = data.data;
        //        if (inserthtml == '' || inserthtml == undefined){
        //            var default_content = self.lang('common_var.itemDefaultContent');
        //            inserthtml = default_content[key];
        //        }
        //        self.exec('inserthtml', inserthtml ).hideMenu();
        //    });
        //},
        //
        //'delete' : function() {
        //    //self.exec('unsubscribe', null);
        //}
    };
    self.clickToolbar(name, self.plugin.common_var.list);
});