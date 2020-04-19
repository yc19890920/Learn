var ip_table;

$(document).ready(function() {


    if(!ip_table){

        $('#dataTables-example tr').click( function() {
            if ( $(this).hasClass('row_selected') )
                $(this).removeClass('row_selected');
            else
                $(this).addClass('row_selected');
        } );

        ip_table = $('#dataTables-example').dataTable({
            "iDisplayLength": -1,
            "lengthMenu": [[-1, 50, 100, 200, 500], ['ALL', 50, 100, 200, 500]],
            "oLanguage": {
                "sLengthMenu": "显示 _MENU_ 每页",
                "sZeroRecords": "对不起! 信息筛选结果为空!",
                "sInfo": "从 _START_ 到 _END_ 总计: _TOTAL_ 条记录",
                "sInfoEmpty": "总计: 0 条记录",
                "sInfoFiltered": "(从 _MAX_ 条记录筛选出)",
                "sSearch": "搜索: ",
                "oPaginate": {
                       "sFirst":    "第一页",
                       "sPrevious": " 上一页 ",
                       "sNext":     " 下一页 ",
                       "sLast":     " 最后一页 "
                   }
            }
        });


    }
});

$.fn.dataTableExt.oApi.fnGetFilteredNodes = function ( oSettings )
{
    var anRows = [];
    //var length = oSettings._iDisplayLength > 0 ? oSettings._iDisplayLength: oSettings.aiDisplay.length;
    var length = oSettings.aiDisplay.length;
    for ( var i=oSettings._iDisplayStart, iLen=length ; i<iLen ; i++ )
    {
        var nRow = oSettings.aoData[ oSettings.aiDisplay[i] ].nTr;
        anRows.push( nRow );
    }
    return anRows;
};

function fnGetAll()
{
    var aTrs = ip_table.fnGetFilteredNodes();

    for ( var i=0 ; i<aTrs.length ; i++ )
    {
        if ( !$(aTrs[i]).hasClass('row_selected') )
            $(aTrs[i]).addClass('row_selected');
    }
}

function fnGetReverse()
{
    var aTrs = ip_table.fnGetFilteredNodes();

    for (var i=0 ; i<aTrs.length ; i++ )
    {
        if ( $(aTrs[i]).hasClass('row_selected') )
        {
            $(aTrs[i]).removeClass('row_selected');
        }
    }
}

function fnGetSelected()
{
    var aReturn = new Array();
    var aTrs = ip_table.fnGetFilteredNodes();
    for ( var i=0 ; i<aTrs.length ; i++ )
    {
        if ( $(aTrs[i]).hasClass('row_selected') )
        {
            var aData = ip_table.fnGetData( aTrs[i]);
            var iId = aData[0];
            aReturn.push( iId );
        }
    }
    return aReturn;
}
