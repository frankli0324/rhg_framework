import json
import judge_utils
import os

BRUTE = True # 所有题把所有的exp和fix都试一遍


def exec_python(cmd, pyver='python2'):
    p = os.popen(pyver+' '+cmd)
    r = p.read()
    p.close()
    return r


vuls = json.load(open('vulnerabilities.json', 'r'))

api_base = vuls['api_base']
questions = judge_utils.get_questions(api_base)
vuls = vuls['vuls']
for i in questions:
    for j in vuls:
        if not BRUTE and 'vulnerable' in exec_python(j['matcher']):
            flags = exec_python(j['exploit'])
            for flag in flags.split('\n'):
                if judge_utils.submit_flag(api_base, i, flag):
                    print(f'攻击成功,flag为{flag}')  # logger
                    break  # 攻击成功
            for i in j['fix']:
                exec_python(i)
                judge_utils.call_check(api_base, i)
            judge_utils.update_check_info(api_base)
            #if success: print('防御成功')
