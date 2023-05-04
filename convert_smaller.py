import yaml

FILENAME = 'trusses/warren_rise.yaml'

with open(FILENAME, 'r') as f:
    data = yaml.safe_load(f)

joints = data['Joints']

csvOut = ''

for i, joint in enumerate(joints):
    x, y, z = joint

    # divide by a constant for the scaled version
    # scale = 40
    # scale = 0.4
    scale = 0.01
    x /= scale
    y /= scale
    z /= scale

    # print(f'Joint {i}: {x}, {y}, {z}')
    # csv = f'{x}, {y}, {z}\n'

    # Z and Y have to be swapped because fusion 360 is weird
    csv = f'{x}, {z}, {y}\n'

    csvOut += csv

with open('joints.csv', 'w') as f:
    f.write(csvOut)


membersCsv = ''
for i, member in enumerate(data['Members']):
    jointA, jointB, material, area = member

    # print(f'Member {i}: {jointA}, {jointB}')
    membersCsv += f'{jointA}, {jointB}\n'

with open('members.csv', 'w') as f:
    f.write(membersCsv)