def typeChange(itemType):
    map = {'其他': '1', '披肩(有外觀)': '2', '卡片': '3', '頭飾': '4', '鑲嵌': '5', '': ''}
    # print(itemType + map[itemType])
    if itemType:
        return map[itemType]
    return ''


def strfilter(text):
    # 功髏許蓋枯淚閱餐豹琵穀骷 % 罡夥豐願搖擺愧靈α縷允 > 證精
    text = text.replace('功', '功\\').replace('髏', '髏\\').replace('許', '許\\').replace('蓋', '蓋\\').replace(
        '枯', '枯\\').replace('淚',
                            '淚\\').replace(
        '閱', '閱\\').replace('餐', '餐\\').replace('豹', '豹\\').replace('琵', '琵\\').replace('穀', '穀\\').replace('骷',
                                                                                                            '骷\\').replace(
        '%', '%\\').replace('罡', '罡\\').replace('罡', '罡\\').replace('夥', '夥\\').replace('豐', '豐\\').replace('願',
                                                                                                            '願\\').replace(
        '搖', '搖\\').replace('擺', '擺\\').replace('愧', '愧\\').replace('靈', '靈\\').replace('α', 'α\\').replace('縷',
                                                                                                            '縷\\').replace(
        '允',
        '允\\').replace(
        '>', '>\\').replace('證', '證\\').replace('精', '精\\')
    return text
