from datetime import datetime, timezone

from django.shortcuts import render, redirect, render_to_response
from .models import Milestones, Variants

def d2_public_milestones(request):
    """
    Show the Public Milestones
    """
    all_milestones = Milestones.objects.all()
    now_date = datetime.now(timezone.utc)
    data = {}
    # Build Each milestone
    for o in all_milestones:
        data[o.hash_id] = {}
        data[o.hash_id]['name'] = o.name
        data[o.hash_id]['milestone_type'] = o.event_type
        data[o.hash_id]['icon'] = o.icon
        data[o.hash_id]['start_date'] = o.start_date
        data[o.hash_id]['end_date'] = o.end_date
        # print(now_date, o.end_date)
        if o.end_date is not None:
            data[o.hash_id]['time_left'] = (o.end_date - now_date)
        data[o.hash_id]['has_variant'] = o.has_variant
        if o.has_variant == 1:
            data[o.hash_id]['variants'] = {}
            if o.hash_id == 2171429505 or o.hash_id == 463010297 or o.hash_id == 3660836525 or o.hash_id == 3551755444:
                related_quests = Variants.objects.get(parent_hash_id=o.hash_id, modifier_type='Quest')
                print(related_quests)
                data[o.hash_id]['icon'] = related_quests.icon
                data[o.hash_id]['quest_hash'] = o.hash_id
            related_variants = Variants.objects.all().filter(parent_hash_id=o.hash_id)
            print(related_variants)
            for v in related_variants:
                data[o.hash_id]['variants'][v.hash_id] = {}
                data[o.hash_id]['variants'][v.hash_id]['variant_hash'] = v.hash_id
                data[o.hash_id]['variants'][v.hash_id]['variant_type'] = v.modifier_type
                data[o.hash_id]['variants'][v.hash_id]['variant_name'] = v.name
                data[o.hash_id]['variants'][v.hash_id]['variant_desc'] = v.description
                data[o.hash_id]['variants'][v.hash_id]['variant_icon'] = v.icon
                if o.hash_id == 2171429505:
                    related_modifiers = Variants.objects.all().filter(parent_hash_id=o.hash_id, modifier_type='Modifier')
                    for m in related_modifiers:
                        data[o.hash_id]['variants'][m.hash_id] = {}
                        data[o.hash_id]['variants'][m.hash_id]['modifier_type'] = m.modifier_type
                        data[o.hash_id]['variants'][m.hash_id]['modifier_name'] = m.name
                        data[o.hash_id]['variants'][m.hash_id]['modifier_icon'] = m.icon
                        data[o.hash_id]['variants'][m.hash_id]['modifier_desc'] = m.description
                if o.hash_id == 2171429505 or o.hash_id == 3660836525 or o.hash_id == 3551755444:
                    related_challenges = Variants.objects.all().filter(parent_hash_id=v.hash_id,
                                                                       modifier_type='Challenge')
                    data[o.hash_id]['variants'][v.hash_id]['challenges'] = {}
                    i = 0
                    for c in related_challenges:
                        i+=1
                        print(i, c.hash_id)
                        data[o.hash_id]['variants'][v.hash_id]['challenges'][c.hash_id] = {}
                        data[o.hash_id]['variants'][v.hash_id]['challenges'][c.hash_id]['challenge_type'] = c.modifier_type
                        data[o.hash_id]['variants'][v.hash_id]['challenges'][c.hash_id]['challenge_name'] = c.name
                        data[o.hash_id]['variants'][v.hash_id]['challenges'][c.hash_id]['challenge_desc'] = c.description
                        data[o.hash_id]['variants'][v.hash_id]['challenges'][c.hash_id]['challenge_icon'] = c.icon

    print(data)
    return render(request, 'destiny_2/d2_public_milestones.html', {'data': data})


##### DESTINY 1 #####
def d1_quests(request, template_name='destiny_1/d1_quests.html'):
    print('quests - dpd')
    import json
    from warmind_d1 import JSON_Actions
    json_actions = JSON_Actions.JSONFunctions()
    data = json_actions.readjson('data/quests.json')
    print(data)
    print('template:', template_name)
    return render(request, template_name, {'data': data})