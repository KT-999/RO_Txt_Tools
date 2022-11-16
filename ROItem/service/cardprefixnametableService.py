from item import models


def query_Cardprefixnametable(item):
    createData = models.Cardprefixnametable.objects
    if item:
        query_Data = createData.filter(item=item)
    return query_Data


def query_Cardprefixnametable(item):
    createData = models.Cardprefixnametable.objects
    if item:
        queryData = createData.filter(item=item)
    return queryData


def delete_update_cardprefixnametable(item):
    createData = models.Cardprefixnametable.objects
    createData.filter(item=item).delete()



def query_Cardprefixnametable(item):
    createData = models.Cardprefixnametable.objects
    if item:
        queryData = createData.filter(item=item)
    return queryData


def update_cardprefixnametable(item, name):
    createData = models.Cardprefixnametable.objects
    createData.filter(item=item).update(card_name=name)


def cardprefixnametable_create(Cardprefixnametable):
    createData = models.Cardprefixnametable.objects
    createData.create(creat_user=Cardprefixnametable.creat_user, card_name=Cardprefixnametable.card_name,
                      item=Cardprefixnametable.item)

