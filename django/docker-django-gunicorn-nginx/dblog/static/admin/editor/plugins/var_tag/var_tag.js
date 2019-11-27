// @lbh 20130625
// 模板中插入umail的一些链接内容的插件

KindEditor.plugin('var_tag', function(K) {
	var self = this, name = 'var_tag';

	var service = K.undef(self.service, false);
	var template_id = K.undef(self.tpl_id, false);

    var customer_var_link = eval(self.customer_var_link);
    var customer_var_content = eval(self.customer_var_content);
	var customer_var_link_dataary = {};
	for (var i = 0, j = customer_var_link.length; i < j; i++){
		for (var key in customer_var_link[i]) {
			customer_var_link_dataary[key] = customer_var_link[i][key];
		}
	}

	self.plugin.var_tag = {
		list : function() {
			//var link = self.lang('var_tag.items');
			var link = customer_var_link_dataary;
			menu = self.createMenu({
				name : 'var_tag',
				width : 300
			});
			K.each(link, function(key, val) {
				menu.addItem({
					title : '<span style="font-size:' + val + ';" >' + val + '</span>',
					height : 20,
					click : function() {
						self.plugin.var_tag.insert(key);
					}
				});
			});
		},

		// 点击图标直接插入退订链接 -- @lbh 20130620
		insert : function(key) {
			//var default_content = self.lang('var_tag.itemDefaultContent');
			var default_content = customer_var_content;
			var content = default_content[key];

			self.exec('inserthtml', content ).hideMenu();

		},

		'delete' : function() {
			//self.exec('unsubscribe', null);
		}
	};
	self.clickToolbar(name, self.plugin.var_tag.list);
});