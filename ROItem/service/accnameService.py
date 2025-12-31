from item import models


def accname_query(act):
    createData = models.Accname.objects
    rtn_data = None
    if act:
        rtn_data = createData.filter(act=act)
    return rtn_data


def accname_update(view_name, act):
    createData = models.Accname.objects
    if act and view_name:
        createData.filter(view_name=view_name).update(act=act)


def accname_create(Accname):
    createData = models.Accname.objects
    createData.create(creat_user=Accname.creat_user, act=Accname.act, view_name=Accname.view_name)


def delete_Accname_Table(view_name):
    createData = models.Accname.objects
    if not view_name:
        return
    if isinstance(view_name, (list, tuple, set)):
        createData.filter(view_name__in=view_name).delete()
    else:
        createData.filter(view_name=view_name).delete()
