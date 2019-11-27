// @lbh 20130625
// 模板中插入umail的一些链接内容的插件
KindEditor.plugin('umail_link', function(K) {
	var self = this, name = 'umail_link';

	var service = K.undef(self.service, false);
	var template_id = K.undef(self.tpl_id, false);
	var user_id = K.undef(self.user_id, false);
	var jsonUrl = self.jsonUrl;

	self.plugin.umail_link = {
		list : function() {
			var link = self.lang('umail_link.items');
			menu = self.createMenu({
				name : 'umail_link',
				width : 'auto',
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
			/*
			 如果邮件内容无法正常显示<a href="{CANNOTVIEW_LINK}" target="_blank">请点击这里</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="{UNSUBSCRIBE_LINK}" target="_blank">退订</a>&nbsp;&nbsp;<a href="{COMPLAINT_LINK}" target="_blank">投诉</a>
			 如果郵件內容無法正常顯示<a href="{CANNOTVIEW_LINK}" target="_blank">請點擊這裡</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="{UNSUBSCRIBE_LINK}" target="_blank">退訂</a>&nbsp;&nbsp;<a href="{COMPLAINT_LINK}" target="_blank">投訴</a>
			 If the message content does not display properly，<a href="{CANNOTVIEW_LINK}" target="_blank">click here</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="{UNSUBSCRIBE_LINK}" target="_blank">unsubscribe</a>&nbsp;&nbsp;<a href="{COMPLAINT_LINK}" target="_blank">complaint</a>
			 메시지 내용이 올바르게 표시되지 않으면<a href="{CANNOTVIEW_LINK}" target="_blank">여기를 클릭하십시오</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="{UNSUBSCRIBE_LINK}" target="_blank">해제</a>&nbsp;&nbsp;<a href="{COMPLAINT_LINK}" target="_blank">불만</a>
			 メッセージの内容が正しく表示されない場合<a href="{CANNOTVIEW_LINK}" target="_blank">ここをクリックしてください</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="{UNSUBSCRIBE_LINK}" target="_blank">キャンセル</a>&nbsp;&nbsp;<a href="{COMPLAINT_LINK}" target="_blank">不満</a>
			 Если содержание сообщения не отображается правильно<a href="{CANNOTVIEW_LINK}" target="_blank">Нажмите здесь</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="{UNSUBSCRIBE_LINK}" target="_blank">аннулирование</a>&nbsp;&nbsp;<a href="{COMPLAINT_LINK}" target="_blank">жалобы</a>
			 */
			var tpl_content = {
				'unsubscribezh'	: service.notview_unsub_complaint_zh?service.notview_unsub_complaint_zh:service.notview_unsub_complaint_en,
				'unsubscribetw'	: service.notview_unsub_complaint_tw?service.notview_unsub_complaint_tw:service.notview_unsub_complaint_en,
				'unsubscribeen'	: service.notview_unsub_complaint_en?service.notview_unsub_complaint_en:service.notview_unsub_complaint_en,
				'unsubscribeko'	: service.notview_unsub_complaint_ko?service.notview_unsub_complaint_ko:service.notview_unsub_complaint_en,
				'unsubscribeja'	: service.notview_unsub_complaint_ja?service.notview_unsub_complaint_ja:service.notview_unsub_complaint_en,
				'unsubscriberu'	: service.notview_unsub_complaint_ru?service.notview_unsub_complaint_ru:service.notview_unsub_complaint_en,
			}

			var url_obj = {
				// '{SUBSCRIBE_LINK}':    jsonUrl + '/template/ajax_unsubscribe_or_complaints/?mailist={MAILLIST_ID}&recipents={RECIPIENTS}&mode=1',
				'{UNSUBSCRIBE_LINK}':  jsonUrl + '/template/ajax_unsubscribe_or_complaints/?mailist={MAILLIST_ID}&recipents={RECIPIENTS}&mode=0',
				'{COMPLAINT_LINK}':    jsonUrl + '/template/ajax_unsubscribe_or_complaints/?mailist={MAILLIST_ID}&recipents={RECIPIENTS}&mode=2&template_id=' + (template_id?template_id:'{TEMPLATE_ID}') + '&user_id=' + (user_id?user_id:'{USER_ID}') + '&send_id={SEND_ID}&subject={SUBJECT_STRING}',
				'{CANNOTVIEW_LINK}':   jsonUrl + '/template/ajax_recipient_view_template/?recipents={RECIPIENTS}&fullname={FULLNAME}&send_id={SEND_ID}&template_id=' + (template_id?template_id:'{TEMPLATE_ID}'),
			}
			var tpl_variable = [
				// '{SUBSCRIBE_LINK}',
				'{UNSUBSCRIBE_LINK}',
				'{COMPLAINT_LINK}',
				'{CANNOTVIEW_LINK}'];
			var linkhtml = tpl_content[key];
			for (var i=0;i<tpl_variable.length;i++){
				var variable = tpl_variable[i];
				var url = url_obj[variable];
				url = K.formatUrl(url,'domain');
				var reg = new RegExp(variable,"g");
				linkhtml = linkhtml.replace(reg, K.escape(url));
			}

			self.exec('inserthtml', linkhtml ).hideMenu();
		},

		'delete' : function() {
			//self.exec('unsubscribe', null);
		}
	};
	self.clickToolbar(name, self.plugin.umail_link.list);
});