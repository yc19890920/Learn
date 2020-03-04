import random
from email.mime.text import MIMEText
from email.header import Header
from itertools import count

C = count()

# 随机中文字符串使用
CHINESE_CHARS = ['鲁', '迅', '又', '谈', '到', '他', '把', '狂', '人', '日', '记', '等', '小', '说', '投', '稿', '新', '青', '年', '的',
                 '经', '过', '曾', '问', '办', '朋', '友', '假', '如', '一', '间', '铁', '屋', '子', '是', '绝', '无', '窗', '户', '而',
                 '万', '难', '破', '毁', '里', '面', '有', '许', '多', '熟', '睡', '们', '不', '久', '都', '要', '闷', '死', '了', '然',
                 '从', '昏', '感', '就', '悲', '哀', '现', '在', '灭', '你', '大', '嚷', '起', '来', '惊', '较', '为', '清', '醒', '几',
                 '个', '使', '这', '幸', '少', '数', '者', '受', '可', '挽', '救', '临', '终', '苦', '楚', '倒', '以', '对', '得', '么',
                 '那', '答', '道', '既', '能', '决', '没', '坏', '希', '望', '于', '便', '写', '此', '后', '还', '陆', '续', '推', '出',
                 '另', '外', '十', '余', '篇', '自', '己', '作', '品', '叫', '国', '本', '已', '并', '非', '切', '迫', '言', '收', '入',
                 '先', '生', '且', '用', '象', '征', '主', '义', '手', '法', '含', '双', '关', '表', '述', '产', '极', '强', '艺', '术',
                 '染', '力', '着', '反', '映', '妇', '女', '惨', '命', '运', '之', '通', '寡', '单', '四', '嫂', '痛', '失', '独', '描',
                 '令', '震', '悚', '地', '展', '示', '幅', '中', '孤', '立', '助', '图', '景', '孔', '乙', '塑', '造', '封', '建', '社',
                 '会', '落', '知', '识', '分', '典', '型', '形', '特', '色', '结', '构', '严', '谨', '加', '工', '和', '创', '成', '革',
                 '民', '众', '流', '血', '牺', '牲', '被', '所', '理', '解', '深', '省', '剖', '析', '辛', '亥', '功', '历', '史', '原',
                 '因', '其', '意', '蕴', '丰', '富', '长', '洋', '鬼', '阶', '级', '家', '庭', '身', '资', '机', '王', '胡', '赵', '司',
                 '晨', '弱', '肉', '食', '折', '射', '同', '时', '也', '增', '勇', '气', '喝', '酒', '看', '笑', '每', '口', '似', '乎',
                 '蓝', '皮', '阿', '五', '声', '音', '候', '虽', '很', '降', '下', '员', '天', '将', '却', '愿', '乳', '房', '孩', '目',
                 '批', '判', '性', '揭', '露', '任', '何', '具', '体', '物', '暗', '引', '发', '尖', '恐', '怖', '画', '央', '毛', '骨',
                 '正', '我', '边', '走', '转', '向', '伸', '远', '处', '栏', '杆', '高', '度', '夸', '张', '蒙', '克', '彩', '与', '保',
                 '持', '定', '程', '联', '样', '紫', '空', '水', '扭', '动', '曲', '线', '桥', '粗', '壮', '挺', '直', '斜', '式', '鲜',
                 '明', '比', '种', '波', '像', '化', '或', '凡', '名', '量', '相', '系', '由', '内', '焦', '虑', '尽', '头', '缘', '觉',
                 '回', '忆', '旋', '围', '绕', '晴', '朗', '蔚', '心', '好', '黑', '消', '荒', '刻', '哭', '诉', '恶', '噩', '哪', '平',
                 '静', '踏', '上', '步', '愤', '怨', '领', '导', '存', '谁', '亦', '迷', '途', '愁', '泪', '做', '信', '怯', '摇', '繁',
                 '盛', '萧', '条', '患', '病', '治', '疗', '著', '旧', '去', '见', '证', '致', '敬', '亢', '奋', '蹦', '跳', '渐', '厂',
                 '舍', '兴', '沿', '岸', '鱼', '村', '洩', '振', '再', '进', '唱', '调', '它', '永', '最', '朴', '素', '笔', '耐', '颗',
                 '浮', '华', '搭', '坛', '让', '灯', '初', '街', '方', '宁', '想', '梦', '第', '次', '认', '学', '报', '纸', '登', '载',
                 '某', '校', '座', '讲', '话', '更', '事', '只', '残', '疾', '仍', '耕', '辍', '激', '励', '鼓', '逆', '境', '屈', '挠']


def make_message():
    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    content = "".join([CHINESE_CHARS[random.randint(0, len(CHINESE_CHARS) - 1)] for i in range(100)])
    subject = "".join([CHINESE_CHARS[random.randint(0, len(CHINESE_CHARS) - 1)] for i in range(20)])
    contents = [
        ("Thank you for creating a new Case: 5885079822", "Thank you for creating a new Case: 5885079822", 'html'),

        ("RE:[CASE 5884881212] Problem with SKU FBA-UKCZ6c-D9-5525",
         "RE:[CASE 5884881212] Problem with SKU FBA-UKCZ6c-D9-5525", 'html'),

        ("[Case ID 6800944271] *UPDATE* Please Investigate SKU F2881", """<div id=":1c8" class="a3s aXjCH ">Greetings,<br>
Thanks for your continued patience. We are currently researching your issue in partnership with the responsible team and will provide an update as soon as any additional information becomes available.</div>""",
         'html'),

        ("Forward Verification - 1548097882.678057", "Forward Verification - 1548097882.678057", 'html'),

        ("Microsoft account security code", """
Microsoft account
Security code
Please use the following security code for the Microsoft account or*****@outlook.com.
Security code: 5292
If you didn't request this code, you can safely ignore this email. Someone else might have typed your email address by mistake.
Thanks,
The Microsoft account team
        """, 'plain'),

        ("ohert message aaaaaaaaaaa", "ohert message aaaaaaaaaaa", 'html'),

        ("验证码：138950", """
        <table align="center" cellspacing="0" id="container" cellpadding="0" style="width: 540px; margin: 0px auto;">   <tbody>    <tr>  <td>
        <table cellspacing="0" id="content" cellpadding="0" style="width: 500px; margin: 0px 20px;">      <tbody>   <tr>
        <td id="header" style="border-bottom: 1px solid rgb(234, 234, 234); padding: 10px 0px;">
        <table cellspacing="0" cellpadding="0">  <tbody> <tr>
        <td width="250" id="logo"><img id="amazonLogo" style="border: 0px; margin: 0px;width: 107px; height: 31px;" src="https://images-na.ssl-images-amazon.com/images/G/01/x-locale/cs/te/logo._CB152417367_.png">   </td>
        <td width="250" id="title" valign="top" align="right">
        <p style="margin: 0px;font-size: 20px; font-family: arial, sans-serif;">验证您的新亚马逊账户</p>     </td>      </tr>      </tbody>     </table>    </td>  </tr>   <tr>
        <td id="verificationMsg" style="padding-left: 0px; padding-top: 9px; padding-bottom: 9px;">
        <p style="margin: 0px;font-size: 14px; font-family: arial, sans-serif;">请输入以下代码：</p>
        <p class="otp">138950</p></td>   </tr><tr>
        <td id="accountSecurity" style="padding-left: 0px; padding-top: 9px; padding-bottom: 9px;">
        <p style="margin: 0px;font-size: 14px; font-family: arial, sans-serif;">请勿与任何人共享此代码，因为它会帮助他们访问您的亚马逊账户。   </p> </td></tr> <tr>
        <td id="closing" style="padding-left: 0px; padding-top: 9px; padding-bottom: 9px;">
        <p style="margin: 0px;font-size: 14px; font-family: arial, sans-serif;">感谢您的惠顾！ 我们希望很快就能再见到您。 </p>    </td>     </tr>   </tbody>      </table>    </td>     </tr>   </tbody>  </table>
        """, 'html'),

        ("您受邀成为授权用户", """
        <table align="center"border="0"cellpadding="0"cellspacing="0"height="100%"width="100%"id="m_6574936496685152314bodyTable"style="border-collapse:collapse;height:100%;margin-top:0;margin-bottom:0;margin-right:0;margin-left:0;padding-top:0;padding-bottom:0;padding-right:0;padding-left:0;width:100%;background-color:#e4e3e4;color:#5a5a5a;font-family:'Lato',Helvetica,Arial,sans-serif"><tbody><tr><td align="center"valign="top"id="m_6574936496685152314bodyCell"style="height:100%;margin-top:0;margin-bottom:0;margin-right:0;margin-left:0;width:100%;padding-top:10px;padding-bottom:10px;border-top-width:0"><table border="0"cellpadding="0"cellspacing="0"style="width:100%;max-width:600px;border-collapse:collapse"><tbody><tr><td><div style="display:none;font-size:1px;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;font-family:sans-serif"></div><table border="0"cellpadding="0"cellspacing="0"width="100%"style="border-spacing:0"><tbody><tr valign="top"style="border-top-width:0;border-bottom-width:0;font-size:14px;line-height:185%;text-align:left"><td valign="top"style="background-color:#2a323a"><table border="0"cellpadding="0"cellspacing="0"width="100%"style="min-width:100%;border-collapse:collapse;background-color:#2a323a"bgcolor="#2a323a"><tbody><tr><td valign="top"><table align="left"border="0"cellpadding="0"cellspacing="0"width="100%"style="min-width:100%;border-collapse:collapse"bgcolor="#2a323a"><tbody><tr><td valign="top"style="padding:20px 0;padding-left:40px"><img align="center"alt=""src="https://ci6.googleusercontent.com/proxy/YAejXmo7HR7N7Q3K0wzjvGrShv1LjxN5Uxialv97_UgcYoQyug_xh3_zUXkul7qJBR9R4dAULiqmagIRLVsh5ZoCqmxRbjnHLQqsF3IfOdTuRk3NC8b9qXnJo3S9BZS0sHpIOPZ9cDxZrq4=s0-d-e1-ft#http://g-ecx.images-amazon.com/images/G/01/tmtdefaulttemplate/img/logo-selling_coach.png"width="200"style="max-width:200px;padding-bottom:0;display:inline!important;vertical-align:bottom;border-width:0;height:auto;outline-style:none;text-decoration:none"class="CToWUd"></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table><table border="0"cellpadding="0"cellspacing="0"width="100%"style="width:100%;max-width:600px;border-collapse:collapse;background-color:#ffffff"bgcolor="#ffffff"><tbody><tr><td><table><tbody><tr valign="top"><td valign="top"><table><tbody><tr><td valign="top"><table align="left"><tbody><tr><td valign="top"><h1>卖家平台邀请<br></h1><h2>成为KINGONE的授权用户！</h2><p>尊敬的RefundHunter,</p><p>我们使用亚马逊卖家平台网站来管理KINGONE业务。我想邀请您成为卖家平台的授权（即受信任的）用户。<wbr>操作过程很简单，您只需执行以下步骤。</p><p>完成后，您将可以访问KINGONE的卖家平台账户。请注意，此邀请将在14天后过期。</p><p></p><p>要开始使用卖家平台，请完成以下步骤：</p><ol><li>在新的浏览器窗口中打开以下URL。请确保您尚未登录亚马逊账户。<br><a href="https://www.amazon.com/gp/f.html?C=2QBL8SZF65SLN&amp;M=urn:rtn:msg:20200215025605cedfcfa09786492183b372cf1bd0p0na&amp;R=Y3RCFSV30RJ5&amp;T=C&amp;U=https%3A%2F%2Fsellercentral.amazon.com%2Finvitation%2Faccept%3FmerchantId%3DAW9CCHSKC8AHK%26invitationId%3De31b87e5-7cdc-4558-a255-36e83df14c2a%26ref_%3Dpe_24880500_411550830&amp;H=KCAZTN09JJJLJPQI5XRWQNMRHTQA&amp;ref_=pe_24880500_411550830"target="_blank"data-saferedirecturl="https://www.google.com/url?q=https://www.amazon.com/gp/f.html?C%3D2QBL8SZF65SLN%26M%3Durn:rtn:msg:20200215025605cedfcfa09786492183b372cf1bd0p0na%26R%3DY3RCFSV30RJ5%26T%3DC%26U%3Dhttps%253A%252F%252Fsellercentral.amazon.com%252Finvitation%252Faccept%253FmerchantId%253DAW9CCHSKC8AHK%2526invitationId%253De31b87e5-7cdc-4558-a255-36e83df14c2a%2526ref_%253Dpe_24880500_411550830%26H%3DKCAZTN09JJJLJPQI5XRWQNMRHTQA%26ref_%3Dpe_24880500_411550830&amp;source=gmail&amp;ust=1581905125413000&amp;usg=AFQjCNEb9FqyNSXwmnfdgcoF8sYn-FiPLw">https:</a></li><li>现在，您需要登录账户。<wbr>如果您已经有一个工作用的亚马逊买家账户，请使用此账户。否则，请使用您的工作电子邮件创建新的用户账户及密码。<br>否则，请使用您的工作电子邮件创建新的用户账户及密码。</li><li>如果您的亚马逊账户使用的是本邀请中使用的电子邮箱地址或电话号<wbr>码，您将自动获得基本访问权限。<br>否则，当成功接受邀请后，<wbr>您将看到一条消息提示您正在等待我的确认。如果我迟迟没有批准，<wbr>请告诉我您在等待批准。</li><li>获取批准后，您就可以开始使用卖家平台了：<a href="https://www.amazon.com/gp/f.html?C=2QBL8SZF65SLN&amp;M=urn:rtn:msg:20200215025605cedfcfa09786492183b372cf1bd0p0na&amp;R=WVV8KGJR1YIB&amp;T=C&amp;U=https%3A%2F%2Fsellercentral.amazon.com.&amp;H=YCX3OPEMKTOBTPMUCBFUAQRSSSAA"target="_blank"data-saferedirecturl="https://www.google.com/url?q=https://www.amazon.com/gp/f.html?C%3D2QBL8SZF65SLN%26M%3Durn:rtn:msg:20200215025605cedfcfa09786492183b372cf1bd0p0na%26R%3DWVV8KGJR1YIB%26T%3DC%26U%3Dhttps%253A%252F%252Fsellercentral.amazon.com.%26H%3DYCX3OPEMKTOBTPMUCBFUAQRSSSAA&amp;source=gmail&amp;ust=1581905125413000&amp;usg=AFQjCNHcHF3jdJsUMJ-AUURGAxMqd8SJFg">https:<wbr>sellercentral.amazon.com.</a></li><li>为了让您能够在卖家平台执行操作，<wbr>我需要向您授予某些功能的权限。如果您无法访问工作所需的功能，<wbr>请告诉我，我会向您授予相应权限。</li></ol><p></p><p>谢谢！<br>jianzhou zhao</p></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table><img width="1"height="1"src="https://ci6.googleusercontent.com/proxy/cXesVf-uoAUtKFM_t5lRsTYlZ3FinJkPneqMYs0jZs-b90ik2pCqmX4Ao9OoNpycmx1IZ30sdP-l754Kc4-1LWhgiW4EkrdDpdESZjq3uOSSUZtlfYGXxDPn8dNC1vI5GyBs4yTD9h_WdXfOkOgxq1Y1JOPc1Gc13f-uOxghNEi8yFVW_NLqMbkF6nQGclIt68GVRj4CDTPxXkAAhzsrnOMMDqsVDumhcLTjcncuRiFsh1qm7qTrlsICZq-OEUksczUmCQoffYRe0v09oNRBcjbIOW1bSTC_M_egYsuoibTKci5sRA-3TGS-gqBibY6849bgCr8qmczTHCopVkHhwy8vBkH_3ugmKxjVOkyP9df46n-IOnsCpW9a2WCC63TM0NqC980AjQ8M=s0-d-e1-ft#https://www.amazon.com/gp/r.html?C=2QBL8SZF65SLN&amp;M=urn:rtn:msg:20200215025605cedfcfa09786492183b372cf1bd0p0na&amp;R=2JA8M5TP9QTR1&amp;T=E&amp;U=https%3A%2F%2Fimages-na.ssl-images-amazon.com%2Fimages%2FG%2F01%2Fnav%2Ftransp.gif&amp;H=9PZG7WJSWJWIOWKLYJSPM7JZTZSA&amp;ref_=pe_24880500_411550830_open"class="CToWUd"></td></tr></tbody></table></td></tr></tbody></table>
        """, "html"),

        ('{} {}'.format(subject, next(C)), content, 'html'),

    ]
    subject, content, _subtype = random.choice(contents)
    return subject, content, _subtype
