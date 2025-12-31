from datetime import datetime
import json
import re

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.clickjacking import xframe_options_sameorigin

from item.models import Item_info, Accessoryid, Accname, Cardprefixnametable, Num2cardillustnametable
from item.util import itemUtil
from item.util.dataUtil import deleteAllTableData, delete_data
from item.util.itemUtil import typeChange, strfilter
from service.accessoryidService import accessoryid_query, accessoryid_create, accessoryid_update
from service.accnameService import accname_create, accname_update, accname_query
from service.cardprefixnametableService import query_Cardprefixnametable, update_cardprefixnametable, \
    cardprefixnametable_create
from service.itemInfoService import item_query, createDataQuery, item_info_query, item_update, item_info_create
from service.num2cardillustnametableService import query_num2cardillustnametable, num2cardillustnametable_create, \
    update_num2cardillustnametable


@xframe_options_sameorigin
def query_item(request):
    if request.POST:
        name = request.POST.get('name')
        item = request.POST.get('item')
        req_type = request.POST.get('type')
        start = request.POST.get('start')
        end = request.POST.get('end')
        upDataNew = request.POST.get('upDataNew')
        itemList = request.POST.get('itemList')
        status = ""
        start_day = ""
        end_day = ""
        if upDataNew == 'delete':
            queryItemList = itemList.split(',')
            itemDataList = createDataQuery(queryItemList)
            for itemData in itemDataList:
                deleteAllTableData(itemData)
            status = "刪除成功，請重新查詢"
            ret = {'url': '/queryItem/', 'status': status}
        else:
            if start != "" and start:
                start_day = datetime.strptime(start, '%Y-%m-%d')
            if end != "" and end:
                end = end + " 23:59:59"
                end_day = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
            item_type = typeChange(req_type)
            jsonList = []
            if name == "" and item == "" and req_type == "" and start == "" and end == "":
                status = "至少輸入一種查詢條件"
            else:
                if (start == "" and end != "") or (start != "" and end == ""):
                    status = "日期選項請同時輸入或重整後不輸入日期"
                else:
                    if end != "" and start != "":
                        if end_day < start_day:
                            status = "結束日期不可小於起始日期"
                        else:
                            itemdb = item_query(item, name, item_type, start_day, end_day)
                            if itemdb:
                                ajax_view = serializers.serialize("json", itemdb)
                                jsonToList = json.loads(ajax_view)
                                for i in jsonToList:
                                    jsonList.append(i)
                    else:
                        itemdb = item_query(item, name, item_type, "", "")
                        if itemdb:
                            ajax_view = serializers.serialize("json", itemdb)
                            jsonToList = json.loads(ajax_view)
                            for i in jsonToList:
                                jsonList.append(i)
            ret = {'url': '/queryItem/', 'itemdb': jsonList, 'status': status}
        return HttpResponse(json.dumps(ret))
    return render(request, "item/queryItem_query.html", {
    })


@xframe_options_sameorigin
def create_item(request):
    if request.POST:
        user = request.user.username
        item = request.POST.get('item')
        name = request.POST.get('name')
        act = request.POST.get('act')
        caption = request.POST.get('caption')
        card = request.POST.get('card')
        view = request.POST.get('view')
        req_type = request.POST.get('type')
        status = ""
        try:
            if user == "":
                status = "請重新登入"
            else:
                if item == "" or name == "" or act == "" or caption == "" or view == "" or not req_type or not card:
                    status = "請輸入完整物品資訊"
                else:
                    item_type = itemUtil.typeChange(req_type)
                    itemQuery = Item_info
                    itemQuery.item = item
                    itemdb = item_info_query(item, None)
                    if itemdb:
                        status = "此物品編號已存在"
                    else:
                        if not item.isdigit():
                            status = "item只可為數字"
                        elif not view.isdigit():
                            status = "view只可為數字"
                        else:
                            itemCreate = Item_info
                            itemCreate.item = item
                            itemCreate.creat_user = user
                            itemCreate.name = name
                            itemCreate.name_scan = name
                            itemCreate.caption = caption
                            itemCreate.caption_scan = caption
                            itemCreate.card = card
                            itemCreate.act = act
                            itemCreate.act_scan = act
                            itemCreate.view = view
                            itemCreate.item_type = item_type
                            item_info_create(itemCreate)
                            if int(item) > 30000:
                                accnameList = accname_query(act)
                                if item_type == '4':
                                    if accnameList:
                                        accname = accnameList[0]
                                        accname_update(accname.view_name, act)
                                        accessoryidList = accessoryid_query(accname.view_name)
                                        if accessoryidList:
                                            accessoryid = accessoryidList[0]
                                            accessoryid_update(accessoryid.view_name, view)
                                        else:
                                            accessoryid = Accessoryid
                                            accessoryid.creat_user = request.user.username
                                            accessoryid.view_name = accname.view_name
                                            accessoryid.view = view
                                            accessoryid_create(accessoryid)
                                    else:
                                        accname = Accname
                                        accname.creat_user = request.user.username
                                        accname.view_name = item
                                        accname.act = act
                                        accname_create(Accname)
                                        accessoryidList = accessoryid_query(item)
                                        if accessoryidList:
                                            accessoryid = accessoryidList[0]
                                            accessoryid_update(accessoryid.view_name, view)
                                        else:
                                            accessoryid = Accessoryid
                                            accessoryid.creat_user = request.user.username
                                            accessoryid.view_name = accname.view_name
                                            accessoryid.view = view
                                            accessoryid_create(accessoryid)
                                elif item_type == '3' or item_type == '5':
                                    query_Card_List = query_Cardprefixnametable(item)
                                    if query_Card_List:
                                        update_cardprefixnametable(item, name)
                                    else:
                                        cardprefixnametable = Cardprefixnametable
                                        cardprefixnametable.item = item
                                        cardprefixnametable.creat_user = request.user.username
                                        cardprefixnametable.card_name = name
                                        cardprefixnametable_create(cardprefixnametable)
                                    if item_type == '3':
                                        query_cardillustList = query_num2cardillustnametable(item)
                                        if query_cardillustList:
                                            update_num2cardillustnametable(item)
                                        else:
                                            num2cardillustnametable = Num2cardillustnametable
                                            num2cardillustnametable.creat_user = request.user.username
                                            num2cardillustnametable.item = item
                                            num2cardillustnametable.card_act = item
                                            num2cardillustnametable_create(num2cardillustnametable)
                            status = "新增成功"
            print(status)
            ret = {'url': '/createitem/', 'status': status}
            pass
        except:
            print("發生例外狀況")
            return
        return HttpResponse(json.dumps(ret))
    return render(request, "item/createItem.html", {

    })


@xframe_options_sameorigin
def change_item(request):
    item = request.GET.get('item')
    status = ""
    if request.POST:
        user = request.user.username
        item = request.POST.get('item')
        name = request.POST.get('name')
        act = request.POST.get('act')
        caption = request.POST.get('caption')
        card = request.POST.get('card')
        view = request.POST.get('view')
        item_type = request.POST.get('type')
        try:
            if user == "":
                status = "請重新登入"
            else:
                if item == "" or name == "" or act == "" or caption == "" or view == "" or not type or not card:
                    status = "請輸入完整物品資訊"
                else:
                    # item_type = itemUtil.typeChange(type)
                    itemQuery = Item_info
                    itemQuery.item = item
                    itemdb = item_info_query(item, None)
                    if not itemdb:
                        status = "此物品編號不存在"
                    else:
                        if not view.isdigit():
                            status = "view只可為數字"
                        else:
                            itemCreate = Item_info
                            itemCreate.item = item
                            itemCreate.creat_user = user
                            itemCreate.name = name
                            itemCreate.name_scan = name
                            itemCreate.caption = caption
                            itemCreate.caption_scan = caption
                            itemCreate.card = card
                            itemCreate.act = act
                            itemCreate.act_scan = act
                            itemCreate.view = view
                            itemCreate.item_type = item_type
                            item_update(itemCreate)
                            if int(item) > 30000:
                                accnameList = accname_query(act)
                                if item_type == '4':
                                    if accnameList:
                                        accname = accnameList[0]
                                        accname_update(accname.view_name, act)
                                        accessoryidList = accessoryid_query(accname.view_name)
                                        if accessoryidList:
                                            accessoryid = accessoryidList[0]
                                            accessoryid_update(accessoryid.view_name, view)
                                        else:
                                            accessoryid = Accessoryid
                                            accessoryid.creat_user = request.user.username
                                            accessoryid.view_name = accname.view_name
                                            accessoryid.view = view
                                            accessoryid_create(accessoryid)
                                    else:
                                        accname = Accname
                                        accname.creat_user = request.user.username
                                        accname.view_name = item
                                        accname.act = act
                                        accname_create(Accname)
                                        accessoryidList = accessoryid_query(item)
                                        if accessoryidList:
                                            accessoryid = accessoryidList[0]
                                            accessoryid_update(accessoryid.view_name, view)
                                        else:
                                            accessoryid = Accessoryid
                                            accessoryid.creat_user = request.user.username
                                            accessoryid.view_name = accname.view_name
                                            accessoryid.view = view
                                            accessoryid_create(accessoryid)
                                elif item_type == '3' or item_type == '5':
                                    query_Card_List = query_Cardprefixnametable(item)
                                    if query_Card_List:
                                        update_cardprefixnametable(item, name)
                                    else:
                                        cardprefixnametable = Cardprefixnametable
                                        cardprefixnametable.item = item
                                        cardprefixnametable.creat_user = request.user.username
                                        cardprefixnametable.card_name = name
                                        cardprefixnametable_create(cardprefixnametable)
                                    if item_type == '3':
                                        query_cardillustList = query_num2cardillustnametable(item)
                                        if query_cardillustList:
                                            update_num2cardillustnametable(item)
                                        else:
                                            num2cardillustnametable = Num2cardillustnametable
                                            num2cardillustnametable.creat_user = request.user.username
                                            num2cardillustnametable.item = item
                                            num2cardillustnametable.card_act = item
                                            num2cardillustnametable_create(num2cardillustnametable)
                                delete_data(itemCreate)
                            status = "更新成功"
            print(status)
            ret = {'url': '/changeItem/', 'status': status}
            pass
        except:
            print("發生例外狀況")
            return
        return HttpResponse(json.dumps(ret))
    else:
        itemdb = item_info_query(item, None)
        for fromtest in itemdb:
            print(fromtest.item_type)
        return render(request, "item/changeItem.html", {
            "itemdb": itemdb
        })


@xframe_options_sameorigin
def text_Item(request):
    status = request.POST.get('status')
    err = ''
    resText = ''
    itemInfo = ''
    item = ''
    if status == "textmode":
        text = request.POST.get('retrxt')
        req_itemInfo = request.POST.get('itemInfo')
        itemMap = {}
        if text:
            resText = strfilter(text)
            resTextList = resText.split('\n')
            cleaned_lines = []
            itemdb_lines = []
            resource_override = ''
            header_present = False
            for line in resTextList:
                stripped = line.strip()
                if not stripped:
                    cleaned_lines.append(line)
                    continue
                if re.match(r'^\d+#\d*$', stripped):
                    header_present = True
                    cleaned_lines.append(stripped)
                    continue
                match = re.match(r'^圖檔套用\s*(\d+)$', stripped)
                if match:
                    resource_override = match.group(1)
                    continue
                if ',' in stripped:
                    parts = stripped.split(',')
                    if len(parts) >= 3 and parts[0].strip().isdigit():
                        itemdb_lines.append(stripped)
                        continue
                cleaned_lines.append(stripped)
            if itemdb_lines and not header_present:
                first_parts = itemdb_lines[0].split(',')
                item_id = first_parts[0].strip()
                resource_name = resource_override
                if not resource_name and len(first_parts) > 1 and first_parts[1].strip().isdigit():
                    resource_name = first_parts[1].strip()
                if resource_name:
                    cleaned_lines.insert(0, f"{item_id}#{resource_name}")
                else:
                    cleaned_lines.insert(0, f"{item_id}#")
            resTextList = cleaned_lines
            dataitem = ''
            itemInfo += (r'local tbl = {' + '\n')
            itemInfoShow = ''
            for str in resTextList:
                if '#' in str:
                    if itemInfoShow:
                        itemInfo += '		},\n'
                        itemInfo += itemInfoShow
                        itemInfoShow = ''
                        itemInfo += '		},\n'
                        itemInfo += '		slotCount = 0,\n'
                        itemInfo += '		ClassNum = 0\n'
                        itemInfo += '	},\n'
                    # dataitem = re.findall(r"\d+\.?\d*", str)
                    dataitem = str.split('#')
                    if not dataitem[0]:
                        continue
                    itemInfo += (r'	[' + dataitem[0] + r'] = {' + '\n')
                    itemInfo += (r'		unidentifiedDisplayName = "' + dataitem[0] + '",' + '\n')
                    if len(dataitem) > 1 and dataitem[1]:
                        itemInfo += (r'		unidentifiedResourceName  = "' + dataitem[1] + '",' + '\n')
                    else:
                        itemInfo += (r'		unidentifiedResourceName  = "' + dataitem[0] + '",' + '\n')
                    itemInfo += (r'		unidentifiedDescriptionName = {' + '\n')

                    itemInfoShow += (r'		identifiedDisplayName = "' + dataitem[0] + r'",' + '\n')
                    if len(dataitem) > 1 and dataitem[1]:
                        itemInfoShow += (r'		identifiedResourceName = "' + dataitem[1] + r'",' + '\n')
                    else:
                        itemInfoShow += (r'		identifiedResourceName  = "' + dataitem[0] + '",' + '\n')
                    itemInfoShow += (r'		identifiedDescriptionName = {' + '\n')
                    pass
                elif str and str != ' ' and str != '    ':
                    if '(紅字)' in str:
                        itemInfo += ('			"^ff0000' + str.replace('	', '').replace(' ', '').replace('(紅字)',
                                                                                                               '') + '^000000",' + '\n')
                        itemInfoShow += (
                                '			"^ff0000' + str.replace('	', '').replace(' ', '').replace('(紅字)',
                                                                                                          '') + '^000000",' + '\n')
                    elif '(藍字)' in str:
                        itemInfo += ('			"^0000ff' + str.replace('	', '').replace(' ', '').replace('(藍字)',
                                                                                                               '') + '^000000",' + '\n')
                        itemInfoShow += (
                                '			"^0000ff' + str.replace('	', '').replace(' ', '').replace('(藍字)',
                                                                                                          '') + '^000000",' + '\n')
                    else:
                        itemInfo += ('			"' + str.replace('	', '').replace(' ', '') + '",' + '\n')
                        itemInfoShow += ('			"' + str.replace('	', '').replace(' ', '') + '",' + '\n')
            if itemInfoShow:
                itemInfo += '		},\n'
                itemInfo += itemInfoShow
                itemInfoShow = ''
                itemInfo += '		},\n'
                itemInfo += '		slotCount = 0,\n'
                itemInfo += '		ClassNum = 0\n'
                itemInfo += '	},\n'
            itemInfo += (r'}' + '\n')
            itemInfo += r'return tbl'
        ret = {'resText': itemInfo, 'url': '/textItem/', 'err': err}
        return HttpResponse(json.dumps(ret))
    if status == "itemmode":
        resText = request.POST.get('retrxt')
        itemInfo = request.POST.get('itemInfo')
        itemList = itemInfo.split('\n')
        rtitem = ''
        itemMap = {}
        if itemList and 'local tbl = {' in itemList[0]:
            if resText:
                resTextList = resText.split('\n')
                for resText_split in resTextList:
                    if resText_split:
                        resText_reList = resText_split.split(',')
                        # if resText_reList[10]:
                        #     print(resText_reList[0] + ' : ' + resText_reList[2] + ' : ' + resText_reList[10])
                        # else:
                        #     print(resText_reList[0] + ' : ' + resText_reList[2] + ' : ' + '0')
                        if resText_reList[18]:
                            if resText_reList[10]:
                                itemMap[resText_reList[0]] = [resText_reList[2], resText_reList[18], resText_reList[10]]
                            else:
                                itemMap[resText_reList[0]] = [resText_reList[2], resText_reList[18], '0']
                        else:
                            if resText_reList[10]:
                                itemMap[resText_reList[0]] = [resText_reList[2], '0', resText_reList[10]]
                            else:
                                itemMap[resText_reList[0]] = [resText_reList[2], '0', '0']
                for itemfor in itemList:
                    if '] = {' in itemfor:
                        item = itemfor.replace('] = {', '').replace('	[', '')
                    if 'ClassNum' in itemfor:
                        if itemMap.get(item):
                            itemfor = '		ClassNum = ' + itemMap.get(item)[1]
                    if 'slotCount' in itemfor:
                        itemfor = '		slotCount = ' + itemMap.get(item)[2]
                    if 'unidentifiedDisplayName' in itemfor:
                        if itemMap.get(item):
                            itemfor = '		unidentifiedDisplayName = "' + strfilter(itemMap.get(item)[0]) + '",'
                    if 'identifiedDisplayName' in itemfor and 'unidentifiedDisplayName' not in itemfor:
                        itemfor = '		identifiedDisplayName = "' + strfilter(itemMap.get(item)[0]) + '",'
                    rtitem += itemfor + '\n'
        ret = {'resText': rtitem, 'url': '/textItem/', 'err': err}
        return HttpResponse(json.dumps(ret))

    if status == "hatmode":
        req_itemInfo = request.POST.get('itemInfo')
        resText = request.POST.get('retrxt')
        itemdbList = resText.split('\n')
        accessoryid = 'ACCESSORY_IDs = {\n'
        accname = 'AccNameTable = {\n'
        if itemdbList:
            for itemdb in itemdbList:
                if itemdb:
                    itemList = itemdb.split(',')
                    if itemList[3] == '5' and int(itemList[18]) > 100:
                        accessoryid += '  ACCESSORY_' + itemList[0] + ' = ' + itemList[18] + '\n'
                        accname += ' [ACCESSORY_IDs.ACCESSORY_' + itemList[0] + ']= "_' + itemList[0] + '",\n'
        ret = {'accessoryid': accessoryid, 'accname': accname, 'url': '/textItem/', 'err': err}
        return HttpResponse(json.dumps(ret))
    if status == 'cardmode':
        resText = request.POST.get('retrxt')
        cardprefixnametable = ''
        num2cardillustnametable = ''
        itemdbList = resText.split('\n')
        if itemdbList:
            for itemdb in itemdbList:
                if itemdb:
                    itemList = itemdb.split(',')
                    if itemList[3] == '6' or itemList[3] == '3':
                        cardprefixnametable += itemList[0] + '#' + itemList[2] + '#\n'
                        # print(itemList[2])
                        if itemList[3] == '6':
                            num2cardillustnametable += itemList[0] + '#' + itemList[0] + '#\n'
        print(cardprefixnametable)
        ret = {'cardprefixnametable': cardprefixnametable,
               'num2cardillustnametable': num2cardillustnametable, 'url': '/textItem/', 'err': err}
        return HttpResponse(json.dumps(ret))

    return render(request, 'item/text_Item.html', {
    })


@xframe_options_sameorigin
def download_page(request):
    itemList = request.POST.get('itemList')
    status = request.POST.get('status')
    outFileItemList = None
    if itemList:
        outFileItemList = itemList.replace(' ', '').split(',')
    items = []
    hatActList = []
    hatItemList = []
    accessoryid = ""
    accname = ""
    itemInfo = ""
    cardprefixnametable = ""
    num2cardillustnametable = ""
    if outFileItemList:
        for outFileItem in outFileItemList:
            if outFileItem != '':
                items.append(outFileItem)
        itemListShow = createDataQuery(items)
        # 功髏許蓋成枯淚閱餐豹琵穀骷%罡夥豐願搖擺愧靈α縷允>證精
        accname += (r'AccNameTable = {' + '\n')
        itemInfo += (r'local tbl = {' + '\n')
        accessoryid += ('ACCESSORY_IDs = {' + '\n')
        for item in itemListShow:
            itemInfo += (r'	[' + item.item.__str__() + r'] = {' + '\n')
            item_name = strfilter(item.name)
            itemInfo += (r'		unidentifiedDisplayName = "' + item_name + '",' + '\n')
            itemInfo += (r'		unidentifiedResourceName  = "' + item.act + '",' + '\n')
            itemInfo += (r'		unidentifiedDescriptionName = {' + '\n')
            captionList = strfilter(item.caption).split('\n')
            for caption in captionList:
                if caption != '':
                    itemInfo += ('			"' + caption + '",' + '\n')
            captionList = ''
            itemInfo += (r'		},' + '\n')
            item_name_scan = strfilter(item.name_scan)

            itemInfo += (r'		identifiedDisplayName = "' + item_name_scan + r'",' + '\n')
            itemInfo += (r'		identifiedResourceName = "' + item.act_scan + r'",' + '\n')
            itemInfo += (r'		identifiedDescriptionName = {' + '\n')
            caption_scanList = strfilter(item.caption_scan).split('\n')
            # caption_scanList = item.caption_scan.split('\n')
            for caption_scan in caption_scanList:
                if caption_scan != '':
                    itemInfo += ('			"' + caption_scan + '",' + '\n')
            caption_scanList = ''
            itemInfo += (r'		},' + '\n')
            itemInfo += (r'		slotCount = ' + item.card + r',' + '\n')
            itemInfo += (r'		ClassNum = ' + item.view + '\n')
            itemInfo += (r'	},' + '\n')
            # 頭飾
            if item.item_type == '4':
                accnameDataList = accname_query(item.act)
                accnameData = accnameDataList[0]
                accname += (
                        r'  [ACCESSORY_IDs.ACCESSORY_' + accnameData.view_name + r'] = "_' + accnameData.act + '"\n')
                accessoryid += '  ACCESSORY_' + accnameData.view_name + ' = ' + item.view + ',\n'
            if item.item_type == '3' or item.item_type == '5':
                cardprefixnList = query_Cardprefixnametable(item.item)
                if cardprefixnList:
                    cardprefixn = cardprefixnList[0]
                    # print(cardprefixn.item)
                    cardprefixnametable += (cardprefixn.item + r'#' + cardprefixn.card_name + r'#' + '\n')
                if item.item_type == '3':
                    cardillustList = query_num2cardillustnametable(item.item)
                    if cardillustList:
                        cardillust = cardillustList[0]
                        num2cardillustnametable += (cardillust.item + r'#' + cardillust.card_act + r'#' + '\n')
        itemInfo += (r'}' + '\n')
        itemInfo += (r'return tbl')
        accessoryid += '}'
        accname += '}'
    return render(request, "item/download_page.html", {
        "itemInfo": itemInfo,
        "accessoryid": accessoryid,
        "accname": accname,
        "cardprefixnametable": cardprefixnametable,
        "cardillustnametable": num2cardillustnametable,
    })
