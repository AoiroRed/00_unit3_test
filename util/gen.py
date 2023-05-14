import random
import json
import math

config = json.load(open('config.json', 'r'))

CHANGE_FREQ = min(config['cases']//20+1, 50)
SETTING = config['gen_setting']
LEN = SETTING['max_input']
MAX_NAME_LEN = 10
MAX_AGE = 200
MAX_ID = 0x7fffffff
MIN_ID = -0x7fffffff-1
MIN_VALUE = 1
MAX_VALUE = 100
MIN_MODIFY_VALUE = -100
MAX_MODIFY_VALUE = 100
MIN_SOCIAL_VALUE = -1000
MAX_SOCIAL_VALUE = 1000
MAX_MONEY = 200
MIN_MONEY = 0
MAX_NOTICE_LEN = 100
USED_ID_PROB = 0.95
NEW_ID_PROB = 0.95
USED_EDGE_PROB = 0.9
NEW_EDGE_PROB = 0.9
NO_EDGE_PROB = 0.05

person_id = set()
group_id = set()
message_id = set()
emoji_id = set()
has_edge = set()
no_edge = []
cnt = 0


def to_rand_upper(s):
    return ''.join(random.choice([c.upper(), c]) for c in s)


def rand_name():
    name = random.choices('abcdefghijklmnopqrstuvwxyz',
                          k=random.randint(1, MAX_NAME_LEN))
    return to_rand_upper(''.join(name))


def rand_age():
    return random.randint(0, MAX_AGE)


def rand_value():
    return random.randint(MIN_VALUE, MAX_VALUE)


def rand_modify_value():
    return random.randint(MIN_MODIFY_VALUE, MAX_MODIFY_VALUE)


def rand_social_value():
    return random.randint(MIN_SOCIAL_VALUE, MAX_SOCIAL_VALUE)


def rand_money():
    return random.randint(MIN_MONEY, MAX_MONEY)


def rand_notice():
    notice = random.choices('abcdefghijklmnopqrstuvwxyz',
                            k=random.randint(1, MAX_NOTICE_LEN))
    return to_rand_upper(''.join(notice))


def new_id(id_set=person_id):
    id = random.randint(MIN_ID, MAX_ID)
    while id in id_set:
        id = random.randint(MIN_ID, MAX_ID)
    return id


def gen_id(id_set=person_id, new_id_prob=None):
    if new_id_prob is None:
        new_id_prob = NEW_ID_PROB
    if random.random() < new_id_prob or len(id_set) == 0:
        id = new_id(id_set)
        no_edge += [min((id, idd), (idd, id)) for idd in id_set]
        id_set.add(id)
    else:
        id = random.choice(list(id_set))
    return id


def get_id(id_set=person_id, used_id_prob=None):
    if used_id_prob is None:
        used_id_prob = USED_ID_PROB
    return random.choice(list(id_set)) if len(id_set) and random.random() < used_id_prob \
        else new_id(id_set)


def gen_edge(new_edge_prob=None):
    if new_edge_prob is None:
        new_edge_prob = NEW_EDGE_PROB
    if len(no_edge) and random.random() < new_edge_prob:
        edge = no_edge.pop(random.randint(0, len(no_edge)-1))
        has_edge.add(edge)
        e = '%d %d' % edge
    else:
        e = get_edge(used_edge_prob=0)
    return e


def get_edge(used_edge_prob=None, no_edge_prob=None):
    if used_edge_prob is None:
        used_edge_prob = USED_EDGE_PROB
    if no_edge_prob is None:
        no_edge_prob = NO_EDGE_PROB
    prob = random.random()
    if len(has_edge) and prob < used_edge_prob:
        id1, id2 = random.choice(list(has_edge))
    elif len(no_edge) and prob < used_edge_prob + no_edge_prob:
        id1, id2 = random.choice(no_edge)
    else:
        id1 = new_id()
        id2 = get_id()
    return random.choice([f'{id1} {id2}', f'{id2} {id1}'])


"""
add_person id(int) name(String) age(int)
add_relation id(int) id(int) value(int)
query_value id(int) id(int)
query_circle id(int) id(int)
query_block_sum
query_triple_sum 
    
add_group id(int)
add_to_group id(int) id(int)
del_from_group id(int) id(int)
query_group_value_sum id(int)
query_group_age_var id(int)
modify_relation id(int) id(int) value(int)
query_best_acquaintance id(int)
query_couple_sum
add_message id(int) socialValue(int) type(int)
    person_id1(int) person_id2(int)|group_id(int)
send_message id(int)
query_social_value id(int)
query_received_messages id(int)
    
add_red_envelope_message id(int) money(int) type(int)
    person_id1(int) person_id2(int)|group_id(int)
add_notice_message id(int) string(String) type(int)
    person_id1(int) person_id2(int)|group_id(int)
clear_notices id(int)
add_emoji_message id(int) emoji_id(int) type(int)
    person_id1(int) person_id2(int)|group_id(int)
store_emoji_id id(int)
query_popularity id(int)
delete_cold_emoji limit(int)
query_money id(int)
delete_cold_emoji_ok_test
query_least_moment id(int)

| name                      | inst  |
| ------------------------- | ----- |
| add_person                | ap    |
| add_relation              | ar    |
| query_value               | qv    |
| query_circle              | qci   |
| query_block_sum           | qbs   |
| query_triple_sum          | qts   |
| add_group                 | ag    |
| add_to_group              | atg   |
| del_from_group            | dfg   |
| query_group_value_sum     | qgvs  |
| query_group_age_var       | qgav  |
| modify_relation           | mr    |
| query_best_acquaintance   | qba   |
| query_couple_sum          | qcs   |
| add_message               | am    |
| send_message              | sm    |
| query_social_value        | qsv   |
| query_received_messages   | qrm   |
| add_red_envelope_message  | arem  |
| add_notice_message        | anm   |
| clean_notices             | cn    |
| add_emoji_message         | aem   |
| store_emoji_id            | sei   |
| query_popularity          | qp    |
| delete_cold_emoji         | dce   |
| query_money               | qm    |
| delete_cold_emoji_ok_test | dceok |
| query_least_moment        | qlm   |
"""


def gen_add_person():
    return f'ap {gen_id()} {rand_name()} {rand_age()}'


def gen_add_relation():
    return f'ar {gen_edge()} {rand_value()}'


def gen_query_value():
    return f'qv {get_edge()}'


def gen_query_circle():
    return f'qci {get_id()} {get_id()}'


def gen_query_block_sum():
    return 'qbs'


def gen_query_triple_sum():
    return 'qts'


def gen_add_group():
    return f'ag {gen_id(group_id)}'


def gen_add_to_group():
    return f'atg {get_id(group_id)} {get_id()}'


def gen_del_from_group():
    return f'dfg {get_id(group_id)} {get_id()}'


def gen_query_group_value_sum():
    return f'qgvs {get_id(group_id)}'


def gen_query_group_age_var():
    return f'qgav {get_id(group_id)}'


def gen_modify_relation():
    return f'mr {get_edge()} {rand_modify_value()}'


def gen_query_best_acquaintance():
    return f'qba {get_id()}'


def gen_query_couple_sum():
    return 'qcs'


def gen_add_message():
    type = random.randint(0, 1)
    return f'am {gen_id(message_id)} {rand_social_value()} {type} ' + \
        (f'{get_id(person_id, used_id_prob=1)} {get_id(group_id, used_id_prob=1)}'
         if type else get_edge())


def gen_send_message():
    return f'sm {get_id(message_id)}'


def gen_query_social_value():
    return f'qsv {get_id()}'


def gen_query_received_messages():
    return f'qrm {get_id()}'


def gen_add_red_envelope_message():
    type = random.randint(0, 1)
    return f'arem {gen_id(message_id)} {rand_money()} {type} ' + \
        (f'{get_id(person_id, used_id_prob=1)} {get_id(group_id, used_id_prob=1)}'
         if type else get_edge())


def gen_add_notice_message():
    type = random.randint(0, 1)
    return f'anm {gen_id(message_id)} {rand_notice()} {type} ' + \
        (f'{get_id(person_id, used_id_prob=1)} {get_id(group_id, used_id_prob=1)}'
         if type else get_edge())


def gen_clean_notices():
    return f'cn {get_id()}'


def gen_add_emoji_message():
    type = random.randint(0, 1)
    return f'aem {gen_id(message_id)} {get_id(emoji_id)} {type} ' + \
        (f'{get_id(person_id, used_id_prob=1)} {get_id(group_id, used_id_prob=1)}'
            if type else get_edge())


def gen_store_emoji_id():
    return f'sei {gen_id(emoji_id)}'


def gen_query_popularity():
    return f'qp {get_id(emoji_id)}'


def gen_delete_cold_emoji():
    return f'dce {random.randint(1, 10)}'


def gen_query_money():
    return f'qm {get_id()}'


def gen_query_least_moment():
    return f'qlm {get_id()}'


def op_normal():
    ops = [gen_add_person] * 10
    ops += [gen_add_relation] * 20
    ops += [gen_query_value] * 1
    ops += [gen_query_circle] * 1
    ops += [gen_query_block_sum] * 1
    ops += [gen_query_triple_sum] * 1
    ops += [gen_add_group] * 6
    ops += [gen_add_to_group] * 8
    ops += [gen_del_from_group] * 3
    ops += [gen_query_group_value_sum] * 1
    ops += [gen_query_group_age_var] * 1
    ops += [gen_modify_relation] * 6
    ops += [gen_query_best_acquaintance] * 1
    ops += [gen_query_couple_sum] * 1
    ops += [gen_add_message] * 1
    ops += [gen_send_message] * 4
    ops += [gen_query_social_value] * 1
    ops += [gen_query_received_messages] * 1
    ops += [gen_add_red_envelope_message] * 3
    ops += [gen_add_notice_message] * 3
    ops += [gen_clean_notices] * 5
    ops += [gen_add_emoji_message] * 3
    ops += [gen_store_emoji_id] * 1
    ops += [gen_query_popularity] * 1
    ops += [gen_delete_cold_emoji] * 1
    ops += [gen_query_money] * 3
    ops += [gen_query_least_moment] * 1
    return ops


def emoji_strong():
    set_global_prob(1, 1, 1, 1)
    ops = [gen_add_person] * 10
    ops += [gen_add_relation] * 20
    ops += [gen_add_group] * 6
    ops += [gen_add_to_group] * 8
    ops += [gen_del_from_group] * 3
    ops += [gen_add_emoji_message] * 3
    ops += [gen_store_emoji_id] * 1
    ops += [gen_query_popularity] * 1
    ops += [gen_delete_cold_emoji] * 1
    ops += [gen_send_message] * 4
    ops += [gen_query_social_value] * 1
    ops += [gen_query_received_messages] * 1


def red_envelope_strong():
    set_global_prob(1, 1, 1, 1)
    ops = [gen_add_person] * 10
    ops += [gen_add_relation] * 20
    ops += [gen_add_group] * 6
    ops += [gen_add_to_group] * 8
    ops += [gen_del_from_group] * 3
    ops += [gen_add_emoji_message] * 3
    ops += [gen_store_emoji_id] * 1
    ops += [gen_query_popularity] * 1
    ops += [gen_delete_cold_emoji] * 1
    ops += [gen_send_message] * 4
    ops += [gen_query_social_value] * 1
    ops += [gen_query_received_messages] * 1


def set_global_prob(new_id_prob, used_id_prob, new_edge_prob, used_edge_prob, no_edge_prob=0.0):
    global NEW_ID_PROB, USED_ID_PROB, NEW_EDGE_PROB, USED_EDGE_PROB, NO_EDGE_PROB
    NEW_ID_PROB = new_id_prob
    USED_ID_PROB = used_id_prob
    NEW_EDGE_PROB = new_edge_prob
    USED_EDGE_PROB = used_edge_prob
    NO_EDGE_PROB = no_edge_prob


def inst_normal():
    global cnt, ops
    if cnt % CHANGE_FREQ == 0:
        ops = get_ops()
    cnt += 1
    inst = [gen_add_person() for _ in range(min_ap)]
    inst += [gen_add_group() for _ in range(min_ag)]
    inst += [gen_add_relation() for _ in range(min_ar)]
    inst += [op() for op in random.choices(ops, k=LEN-min_ap-min_ag-min_ar)]
    return inst


def qlm_strong():
    edges = []
    set_global_prob(1, 1, 1, 1)
    ap = random.randint(int(math.sqrt(LEN)), LEN//4)
    ar = LEN - ap * 3
    inst = [f'ap {i} {i} {1}' for i in range(ap)]
    for i in range(ap):
        person_id.add(i)
        inst += [f'ar {i} {i+1} 100']
        edges += [(i, j) for j in range(i+2, ap)]
    inst.pop()
    for _ in range(ar):
        edge = edges.pop(random.randint(0, len(edges)-1))
        inst += ['ar %d %d ' % edge + f'{rand_value()}']
    inst += [f'qlm {i}' for i in range(ap)]
    inst += ['qbs']
    return inst


get_inst = inst_normal
get_ops = op_normal
min_ar = min(LEN // 10, 10)
min_ap = min(LEN // 10, 10)
min_ag = 1
TYPE = SETTING['type']
if config['mode'] != 'rand':
    None
elif TYPE == 'emoji' or TYPE in SETTING['emoji']:
    print('emoji')
    get_ops = emoji_strong
elif TYPE == 'qlm' or TYPE in SETTING['emoji']:
    print('qlm')
    get_inst = qlm_strong
else:
    print('normal')
    get_ops = op_normal
ops = get_ops()


def gen():
    person_id.clear()
    group_id.clear()
    message_id.clear()
    emoji_id.clear()
    return '\n'.join(get_inst())


if __name__ == '__main__':
    MAX_ID = 100
    MIN_ID = 0
    LEN = 15
    min_ar = min(LEN // 10, 10)
    min_ap = min(LEN // 10, 10)
    print(gen())
