import shutil
import re
import datetime
from src.project import Project
import json
from collections import OrderedDict

def launch_new_project():
    print("  ______  _____  ______   _____  _______       ")
    print(" |_____/ |     | |_____] |     |    |          ")
    print(" |    \_ |_____| |_____] |_____|    |          ")
    print("                                               ")
    print(" _______  _____  __   _ _     _ _______ __   __")
    print(" |  |  | |     | | \  | |____/  |______   \_/  ")
    print(" |  |  | |_____| |  \_| |    \_ |______    |   ")
    print("                                               ")
    print(" ______  _     _ _______        _______  ______")
    print(" |_____] |     |    |    |      |______ |_____/")
    print(" |_____] |_____|    |    |_____ |______ |    \_")
    print()
    print("Press Enter to proceed")
    input()

    try:
        shutil.move('/Users/lcvista/Downloads/config.json', '/Users/lcvista/dev/rmb/config/config.json')
        # shutil.copy('/Users/lcvista/Downloads/config.json', '/Users/lcvista/dev/rmb/config/config.json')
    except Exception as e:
        print('Error retrieving config file: {}'.format(str(e)))
        # print("shutil.copy('/Users/lcvista/Downloads/config.json', '/Users/lcvista/dev/rmb/config/config.json')")
        print("shutil.move('/Users/lcvista/Downloads/config.json', '/Users/lcvista/dev/rmb/config/config.json')")
        import pdb; pdb.set_trace()
    f = open('/Users/lcvista/dev/rmb/config/config.json')
    project_config = json.load(f)
    feature = project_config.get('feature')
    # feature = feature[0:-1] if feature[-1] == 's' else feature  # make singular for demo
    camel_case = ''.join(x for x in feature.title() if not x.isspace())
    project_config['env']['replaces'] = OrderedDict({
        **project_config['env']['replaces'],  # revisit this later -- project should overwrite -- THIS IS STILL MESSED UP FOR PERMISSIONS AND REPORTING
        'RobotMonkeyButlers': camel_case,  # Added all these extras to handle plural -- think of better way
        'RobotMonkeyButler': camel_case,
        'robotmonkeybutlers': ''.join(feature.lower().split(' ')),
        'robotmonkeybutler': ''.join(feature.lower().split(' ')),
        'Robot Monkey Butlers': feature.title(),
        'Robot Monkey Butler': feature.title(),
        'robot_monkey_butlers': '_'.join(feature.split(' ')).lower(),
        'robot_monkey_butler': '_'.join(feature.split(' ')).lower(),
        'robotMonkeyButlers': camel_case[0].lower() + camel_case[1:],
        'robotMonkeyButler': camel_case[0].lower() + camel_case[1:],
    })
    f.close()
    Project(**project_config).go()
    timestamp = re.sub(' ', '', str(datetime.datetime.now()))
    shutil.move('/Users/lcvista/dev/rmb/config/config.json', '/Users/lcvista/dev/rmb/config/config{}.json'.format(timestamp))


if __name__ == "__main__":
    print('__main__')
    launch_new_project()
