import random


def randComment():
    comment = ('好喜欢呜呜呜', '好棒！！！', '哈哈哈，可以', '气质出众魅力十足', '好可爱', '感觉好熟悉', '好看！发现宝藏',
               '很好看!', '质量非常高', '(･∀･)', '好有违和感', '有点事，我先走了Σ( ￣□￣||)<Σ( ￣□￣||)<',
               '开门，FBI', 'this is so good', '真的好', '没那么简单。。', '喜欢！', '封 面 真 棒 ',
               '好棒', '哈哈哈，逗死', '啊耶', '啪啪啪', '这期好棒woc', '很喜欢',
               '点个赞,好棒!!!', '收藏', '转发', '可以，转发', '很好，收藏', '妙啊～', '棒棒棒', '三连必须的', '挺好的',
               '三连三连', '看了，很好', '看了，收藏', '收藏一波', '喵～～秒', '嘤嘤嘤嘤嘤嘤', '确认好看', '必须转发', '赞就丸了！',
               '太绝了呜呜呜', '好清晰', '绝(இдஇ )', '太优秀啦！赞丸都好棒！赞就丸了！！', '这版太棒啦！', '汪汪汪～',
               '阿噗~', '真实', 'hhh', 'its goods', '已踩不谢', '啊这', '前排', '好家伙,真是好家伙', '哈哈哈哈,笑死我了', 'giao',
               '滴滴滴。。。。', '三连...', '！！！爱了', '我，我能催更吗', '……', '讚！！！', '弥hotel', '一键返回，三连免了',
               '我知道了', '有亮点', '沙发～', '我的天，前排！', '粑粑', '那行吧，给你个赞', '你学废了吗', '楼上学会了吗', '楼下学废了吗',
               '讲真的，还是很受用', '涨知识了', '没学会，你觉得呢', '场景 气氛很到位', '第一次看就觉得很受用', '我来了', '每日一遍',
               'bgm是啥啊', '好看不火', '没看够啊', '(｀・ω・´)(｀・ω・´)', 'BGM什么')
    index = random.randint(0, 89)
    return comment[index]


def randExpression():
    index = random.randint(0, 8)
    if index == 8:
        return ''
    expr = ('[666]', '[呲牙]', '[赞]', '[玫瑰]', '[捂脸]', '[微笑]', '[耶]', '[鼓掌]')
    return expr[index]