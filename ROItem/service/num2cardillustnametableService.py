from item import models


def num2cardillustnametable_create(Num2cardillustnametable):
    createData = models.Num2cardillustnametable.objects
    createData.create(creat_user=Num2cardillustnametable.creat_user, card_act=Num2cardillustnametable.card_act,
                      item=Num2cardillustnametable.item)


def update_num2cardillustnametable(item):
    createData = models.Num2cardillustnametable.objects
    createData.filter(item=item).update(card_act=item)


def query_num2cardillustnametable(item):
    createData = models.Num2cardillustnametable.objects
    queryData = createData.filter(item=item)
    return queryData


def delete_num2cardillustnametable(item):
    createData = models.Num2cardillustnametable.objects
    createData.filter(item=item).delete()
