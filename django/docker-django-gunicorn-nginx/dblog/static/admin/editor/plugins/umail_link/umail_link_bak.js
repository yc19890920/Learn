// @lbh 20130625
// 模板中插入umail的一些链接内容的插件
KindEditor.plugin('umail_link', function(K) {
	var self = this, name = 'umail_link';

	var service = K.undef(self.service, false);
	var template_id = K.undef(self.tpl_id, false);
	var jsonUrl = self.jsonUrl

	self.plugin.umail_link = {
		list : function() {
			var link = self.lang('umail_link.items');
				menu = self.createMenu({
					name : 'umail_link',
					width : 177
				});
			K.each(link, function(key, val) {
				menu.addItem({
					title : '<span style="font-size:' + val + ';" >' + val + '</span>',
					height : 20,
					click : function() {
						self.plugin.umail_link.insert(key);
					}
				});
			});
		},

		// 点击图标直接插入退订链接 -- @lbh 20130620
		insert : function(key) {
			jQuery.post("/template/ajax_check_template_lang/", {content:editor.html()},
				function(data){
					var tpl_content = {
						'subscribe'		: service.subscribe_html,
						'unsubscribe'	: data == 'en'? service.unsubscribe_bottom_html_en:
                            (data == 'tw'? service.unsubscribe_bottom_html_tw:
                                (data == 'zh'? service.unsubscribe_bottom_html:
                                    (data == 'ko'? service.unsubscribe_bottom_html_ko:
                                        (data == 'ja'? service.unsubscribe_bottom_html_ja:
                                            (data == 'ru'? service.unsubscribe_bottom_html_ru:service.unsubscribe_html))))),
						'unsubscribezh'	: service.unsubscribe_bottom_html?service.unsubscribe_bottom_html:service.unsubscribe_html,
						'unsubscribetw'	: service.unsubscribe_bottom_html_tw?service.unsubscribe_bottom_html_tw:service.unsubscribe_html,
						'unsubscribeen'	: service.unsubscribe_bottom_html_en?service.unsubscribe_bottom_html_en:service.unsubscribe_html,
						'unsubscribeko'	: service.unsubscribe_bottom_html_ko?service.unsubscribe_bottom_html_ko:service.unsubscribe_html,
						'unsubscribeja'	: service.unsubscribe_bottom_html_ja?service.unsubscribe_bottom_html_ja:service.unsubscribe_html,
						'unsubscriberu'	: service.unsubscribe_bottom_html_ru?service.unsubscribe_bottom_html_ru:service.unsubscribe_html,
						'cannotview'	: service.cannotview_html
					};

					var tpl_variable = {
						'subscribe'		: '{SUBSCRIBE_LINK}',
						'unsubscribe'	: '{UNSUBSCRIBE_LINK}',
						'unsubscribezh'	: '{UNSUBSCRIBE_LINK}',
						'unsubscribetw'	: '{UNSUBSCRIBE_LINK}',
						'unsubscribeen'	: '{UNSUBSCRIBE_LINK}',
						'unsubscribeko'	: '{UNSUBSCRIBE_LINK}',
						'unsubscribeja'	: '{UNSUBSCRIBE_LINK}',
						'unsubscriberu'	: '{UNSUBSCRIBE_LINK}',
						'cannotview'	: '{CANNOTVIEW_LINK}'
					};

					var url_obj = {
						'subscribe'		: jsonUrl + '/template/ajax_unsubscribe_or_complaints/?mailist={MAILLIST_ID}&recipents={RECIPIENTS}&mode=1',
						'unsubscribe'	:     jsonUrl + '/template/ajax_unsubscribe_or_complaints/?mailist={MAILLIST_ID}&recipents={RECIPIENTS}&mode=0',
						'unsubscribezh'	: jsonUrl + '/template/ajax_unsubscribe_or_complaints/?mailist={MAILLIST_ID}&recipents={RECIPIENTS}&mode=0',
						'unsubscribetw'	: jsonUrl + '/template/ajax_unsubscribe_or_complaints/?mailist={MAILLIST_ID}&recipents={RECIPIENTS}&mode=0',
						'unsubscribeen'	: jsonUrl + '/template/ajax_unsubscribe_or_complaints/?mailist={MAILLIST_ID}&recipents={RECIPIENTS}&mode=0',
						'unsubscribeko'	: jsonUrl + '/template/ajax_unsubscribe_or_complaints/?mailist={MAILLIST_ID}&recipents={RECIPIENTS}&mode=0',
						'unsubscribeja'	: jsonUrl + '/template/ajax_unsubscribe_or_complaints/?mailist={MAILLIST_ID}&recipents={RECIPIENTS}&mode=0',
						'unsubscriberu'	: jsonUrl + '/template/ajax_unsubscribe_or_complaints/?mailist={MAILLIST_ID}&recipents={RECIPIENTS}&mode=0',
                        'cannotview':       jsonUrl + '/template/ajax_recipient_view_template/?recipents={RECIPIENTS}&fullname={FULLNAME}&send_id={SEND_ID}&template_id=' + (template_id?template_id:'{TEMPLATE_ID}'),
					};
                    //
					//var url_obj = {
					//	'subscribe'		: 'api/maillist.php?p=1:{MAILLIST_ID}:{RECIPIENTS}',
					//	'unsubscribe'	: 'api/maillist.php?p=0:{MAILLIST_ID}:{RECIPIENTS}',
					//	'unsubscribezh'	: 'api/maillist.php?p=0:{MAILLIST_ID}:{RECIPIENTS}',
					//	'unsubscribetw'	: 'api/maillist.php?p=0:{MAILLIST_ID}:{RECIPIENTS}',
					//	'unsubscribeen'	: 'api/maillist.php?p=0:{MAILLIST_ID}:{RECIPIENTS}',
					//	'unsubscribeko'	: 'api/maillist.php?p=0:{MAILLIST_ID}:{RECIPIENTS}',
					//	'unsubscribeja'	: 'api/maillist.php?p=0:{MAILLIST_ID}:{RECIPIENTS}',
					//	'unsubscriberu'	: 'api/maillist.php?p=0:{MAILLIST_ID}:{RECIPIENTS}',
					//	'cannotview'	: 'client-api/mm_ms.php?p=recipient-view-tpl:{RECIPIENTS}:{FULLNAME}:{SEND_ID}:'+(template_id?template_id:'{TEMPLATE_ID}')
					//};

					var default_content = self.lang('umail_link.itemDefaultContent');

					var url = url_obj[key];
					var variable = tpl_variable[key];
					var content = tpl_content[key];
					var sub = default_content[key];
					var range = self.cmd.range;


					if(self.urlType == '') {
						url = K.formatUrl(url,'domain');
					}

					var linkhtml = '';
					if(content) {
						var reg = new RegExp(variable,"g");
						linkhtml = content.replace(reg, K.escape(url));
					}else{
						self.cmd.selection();
						var a = self.plugin.getSelectedLink();
						if (a) {
							range.selectNode(a[0]);
							self.cmd.select();
							if(a.attr('_name') == key) {
								sub = a.html();
							}else{
								return false;
							}
						}else if( range.html() ){
							sub = range.html();
						}
						linkhtml = '<a href="' + K.escape(url) + '" data-ke-src="' + K.escape(url) + '" ';
						linkhtml += 'alt="' + K.escape(sub) + '" ';
						linkhtml += 'target="_blank" _name="'+ key +'" >';
						linkhtml += sub + '</a>';
					}
					self.exec('inserthtml', linkhtml ).hideMenu();
				}
			);
		},

		'delete' : function() {
			//self.exec('unsubscribe', null);
		}
	};
	self.clickToolbar(name, self.plugin.umail_link.list);
});