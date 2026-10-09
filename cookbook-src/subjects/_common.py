def bilingual(en,zh):return {'en':en,'zh-hans':zh}

def lesson(identifier,number,slug,en_title,zh_title,en_summary,zh_summary,snapshots,functions,category,en_category,zh_category,**extra):
    return dict(id=identifier,number=number,slug=slug,title=bilingual(en_title,zh_title),summary=bilingual(en_summary,zh_summary),
        discipline=extra.pop('discipline','data-science'),minutes=extra.pop('minutes',50),difficulty=extra.pop('difficulty',2),
        snapshots=snapshots,functions=functions,packages=extra.pop('packages',['numpy','pandas','matplotlib','IPython']),
        category=category,category_title=bilingual(en_category,zh_category),**extra)

def step(en_title,zh_title,en,zh,code=None,cover=False):
    return dict(title=bilingual(en_title,zh_title),text=bilingual(en,zh),code=code,**({'tag':'cover'} if cover else {}))

def exercises(en,zh):
    assert len(en)==len(zh)==6
    return {'en':en,'zh-hans':zh}
