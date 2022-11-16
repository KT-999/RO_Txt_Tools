from service.accessoryidService import accessoryid_query, delete_Accessoryid_Table
from service.accnameService import accname_query, delete_Accname_Table
from service.cardprefixnametableService import query_Cardprefixnametable, delete_update_cardprefixnametable
from service.itemInfoService import delete_Item
from service.num2cardillustnametableService import query_num2cardillustnametable, delete_num2cardillustnametable


def deleteAllTableData(item):
    accnameList = accname_query(item.act)
    if accnameList:
        accname = accnameList[0]
        accessoryidList = accessoryid_query(accname.view_name)
        if accessoryidList:
            accessoryid = accessoryidList[0]
            delete_Accessoryid_Table(accessoryid.view_name)
        delete_Accname_Table(accname.view_name)
    query_card = query_Cardprefixnametable(item.item)
    if query_card:
        delete_update_cardprefixnametable(item.item)
    cardillust = query_num2cardillustnametable(item.item)
    if cardillust:
        delete_num2cardillustnametable(item.item)
    delete_Item(item.item)


def delete_data(item):
    if item.item_type != '4':
        accnameList = accname_query(item.act)
        if accnameList:
            accname = accnameList[0]
            accessoryidList = accessoryid_query(accname.view_name)
            if accessoryidList:
                accessoryid = accessoryidList[0]
                delete_Accessoryid_Table(accessoryid.view_name)
            delete_Accname_Table(accname.view_name)
    if item.item_type != '3' and item.item_type != '5':
        query_card = query_Cardprefixnametable(item.item)
        if query_card:
            delete_update_cardprefixnametable(item.item)
    if item.item_type != '3':
        cardillust = query_num2cardillustnametable(item.item)
        if cardillust:
            delete_num2cardillustnametable(item.item)
