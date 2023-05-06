import random

MAX_NAME_LEN = 10
MAX_AGE = 200
MAX_VALUE = 100
MIN_MODIFY_VALUE = -100
MAX_MODIFY_VALUE = 100
MIN_SOCIAL_VALUE = -1000
MAX_SOCIAL_VALUE = 1000

person_id = set()
group_id = set()
message_id = set()


def to_rand_upper(s):
    return ''.join(random.choice([c.upper(), c]) for c in s)


def rand_name(maxlen=MAX_NAME_LEN):
    name = random.choices('abcdefghijklmnopqrstuvwxyz',
                          k=random.randint(1, maxlen))
    return to_rand_upper(''.join(name))


def rand_age():
    return random.randint(0, MAX_AGE)


def rand_value():
    return random.randint(0, MAX_VALUE)


def rand_modify_value():
    return random.randint(MIN_MODIFY_VALUE, MAX_MODIFY_VALUE)


def rand_social_value():
    return random.randint(MIN_SOCIAL_VALUE, MAX_SOCIAL_VALUE)


def rand_id(used_id=person_id):
    if len(used_id) == 0 or random.choice([True, True, False]):
        id = random.randint(-10, 100)
        used_id.add(id)
    else:
        id = random.choice(list(used_id))
    return id


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
modify_relation_ok_test
query_best_acquaintance id(int)
query_couple_sum
add_message id(int) socialValue(int) type(int)
    person_id1(int) person_id2(int)|group_id(int)
send_message id(int)
query_social_value id(int)
query_received_messages id(int)

| name                    | inst |
| ----------------------- | ---- |
| add_person              | ap   |
| add_relation            | ar   |
| query_value             | qv   |
| query_circle            | qci  |
| query_block_sum         | qbs  |
| query_triple_sum        | qts  |
| add_group               | ag   |
| add_to_group            | atg  |
| del_from_group          | dfg  |
| query_group_value_sum   | qgvs |
| query_group_age_var     | qgav |
| modify_relation         | mr   |
| modify_relation_ok_test | mrok |
| query_best_acquaintance | qba  |
| query_couple_sum        | qcs  |
| add_message             | am   |
| send_message            | sm   |
| query_social_value      | qsv  |
| query_received_messages | qrm  |
"""


def gen_add_person():
    return f'ap {rand_id()} {rand_name()} {rand_age()}'


def gen_add_relation():
    return f'ar {rand_id()} {rand_id()} {rand_value()}'


def gen_query_value():
    return f'qv {rand_id()} {rand_id()}'


def gen_query_circle():
    return f'qci {rand_id()} {rand_value()}'


def gen_query_block_sum():
    return 'qbs'


def gen_query_triple_sum():
    return 'qts'


def gen_add_group():
    return f'ag {rand_id(group_id)}'


def gen_add_to_group():
    return f'atg {rand_id(group_id)} {rand_id()}'


def gen_del_from_group():
    return f'dfg {rand_id(group_id)} {rand_id()}'


def gen_query_group_value_sum():
    return f'qgvs {rand_id(group_id)}'


def gen_query_group_age_var():
    return f'qgav {rand_id(group_id)}'


def gen_modify_relation():
    return f'mr {rand_id()} {rand_id()} {rand_modify_value()}'


def gen_query_best_acquaintance():
    return f'qba {rand_id()}'


def gen_query_couple_sum():
    return 'qcs'


def gen_add_message():
    type = random.randint(0, 1)
    return f'am {rand_id(message_id)} {rand_social_value()} {type} ' + \
        f'{random.choice(list(person_id))} {random.choice(list(group_id if type else person_id))}'


def gen_send_message():
    return f'sm {rand_id(message_id)}'


def gen_query_social_value():
    return f'qsv {rand_id()}'


def gen_query_received_messages():
    return f'qrm {rand_id()}'


def gen(max_len=1000):
    length = random.randint(1, max_len)
    min_ap = min(length // 10, 10)
    min_ag = 1

    ops = [gen_add_person] * 30
    ops += [gen_add_relation] * 60
    ops += [gen_query_value] * 5
    ops += [gen_query_circle] * 15
    ops += [gen_query_block_sum] * 5
    ops += [gen_query_triple_sum] * 5
    ops += [gen_add_group] * 30
    ops += [gen_add_to_group] * 40
    ops += [gen_del_from_group] * 15
    ops += [gen_query_group_value_sum] * 5
    ops += [gen_query_group_age_var] * 5
    ops += [gen_modify_relation] * 30
    ops += [gen_query_best_acquaintance] * 10
    ops += [gen_query_couple_sum] * 10
    ops += [gen_add_message] * 25
    ops += [gen_send_message] * 20
    ops += [gen_query_social_value] * 5
    ops += [gen_query_received_messages] * 5

    return '\n'.join([gen_add_person() for _ in range(min_ap)]
                     + [gen_add_group() for _ in range(min_ag)]
                     + [op() for op in random.choices(ops, k=length-min_ap-min_ag)])


def gen_modify_relation_ok_test():
    ret = 'mrok '
    type = random.choice([i for i in range(-1, 21)]-[13, 14, 18, 19])
    n = random.randint(1, 20)
    people = random.sample(range(-0x7fffffff-1, 0x7fffffff), n)


if __name__ == '__main__':
    print(gen())