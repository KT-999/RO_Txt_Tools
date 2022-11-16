from item import models


def item_info_query(item, name):
    queryData = models.Item_info.objects
    queryDB = None
    queryDB = queryData.filter(item=item)
    if (item != "" and item is not None) and (name == "" or name is None):
        queryDB = queryData.filter(item=item)
    return queryDB


def createDataQuery(item):
    queryData = models.Item_info.objects
    queryDB = None
    if item:
        queryDB = queryData.filter(item__in=item).order_by('item')
    return queryDB


def delete_Item(item):
    createData = models.Item_info.objects
    createData.filter(item=item).delete()


def item_query(item, name, item_type, start, end):
    queryData = models.Item_info.objects
    queryDB = None
    if start != "" and end != "":
        if (item != "" and item is not None):
            queryDB = queryData.filter(item=item, name__contains=name, item_type__contains=item_type,
                                       last_modify_date__gt=start, last_modify_date__lt=end).order_by('item')
        else:
            queryDB = queryData.filter(name__contains=name, item_type__contains=item_type, last_modify_date__gt=start,
                                       last_modify_date__lt=end).order_by('item')
    else:
        if (item != "" and item is not None):
            queryDB = queryData.filter(item=item, name__contains=name, item_type__contains=item_type).order_by('item')
        else:
            queryDB = queryData.filter(name__contains=name, item_type__contains=item_type).order_by('item')
    return queryDB


def item_info_query(item, name):
    queryData = models.Item_info.objects
    queryDB = None
    queryDB = queryData.filter(item=item)
    if (item != "" and item is not None) and (name == "" or name is None):
        queryDB = queryData.filter(item=item)
    return queryDB


def item_info_create(Item_Info):
    createData = models.Item_info.objects
    createData.create(item=Item_Info.item, name=Item_Info.name, name_scan=Item_Info.name_scan,
                      creat_user=Item_Info.creat_user,
                      caption_scan=Item_Info.caption_scan, caption=Item_Info.caption, card=Item_Info.card,
                      act=Item_Info.act,
                      act_scan=Item_Info.act_scan, view=Item_Info.view, item_type=Item_Info.item_type)


def item_update(Item_Info):
    createData = models.Item_info.objects.filter(item=Item_Info.item)[0]
    createData.name = Item_Info.name
    createData.name_scan = Item_Info.name_scan
    createData.creat_user = Item_Info.creat_user
    createData.caption = Item_Info.caption
    createData.caption_scan = Item_Info.caption_scan
    createData.card = Item_Info.card
    createData.act = Item_Info.act
    createData.act_scan = Item_Info.act_scan
    createData.view = Item_Info.view
    createData.item_type = Item_Info.item_type
    createData.save()
