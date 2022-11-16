from item import models


def accessoryid_query(view_name):
    createData = models.Accessoryid.objects
    if view_name:
        rtn_data = createData.filter(view_name=view_name)
    return rtn_data


def delete_Accessoryid_Table(view_name):
    createData = models.Accessoryid.objects
    createData.filter(view_name__in=view_name).delete()


def accessoryid_query(view_name):
    createData = models.Accessoryid.objects
    rtn_data = None
    if view_name:
        rtn_data = createData.filter(view_name=view_name)
    return rtn_data


def accessoryid_update(view_name, view):
    createData = models.Accessoryid.objects
    if view_name and view:
        createData.filter(view_name=view_name).update(view=view)


def accessoryid_create(Accessoryid):
    createData = models.Accessoryid.objects
    createData.create(creat_user=Accessoryid.creat_user, view=Accessoryid.view, view_name=Accessoryid.view_name)
