#!/usr/bin/env python

# load the profile
def load_profile(filename='Tmap_Remote_Disk_Info.ini'):
    """
    to load the profile info,including:
    code: remote password
    ip: remote ip
    cmd: the command run in the remote machines
    path: the path for command
    grep_kw:grep keyword
    """
    import ConfigParser
    config = ConfigParser.ConfigParser()

    config.read(filename)
    password = config.get('installation','code')
    ips = config.items('server_ips')
    keyword = config.get('installation','grep_kw')
    print(password,ips,keyword)
    return password,ips,keyword


# load excecute the command in the remote servers
def get_remote_disk_info(kws_dict):
    """
    to get the disk info from remote servers,and the command line is like:
    df -hl | grep workspace
    """
    import subprocess
    remote_cmd = r'sshpass -p {password} ssh jenkins@{ip} df -hl | grep {keyword}'
    print(remote_cmd.format(**kws_dict))
    result_Popen = subprocess.Popen(remote_cmd.format(**kws_dict),shell=True,stdout=subprocess.PIPE)
    #print(result_Popen.stdout.read())
    #pass
    result_data = result_Popen.stdout.readlines()
        
    # print the data
    for line in result_data:
        #print(line)
        detail_info = line.split()
        #print("_*"*10)
        #print(detail_info)
        left_space = detail_info[4]
        #print(left_space[:left_space.index("%")])
        
        # free space percent
        free_percent_value = left_space[:left_space.index("%")]
        if int(free_percent_value) > 95 or int(detail_info[3][:detail_info[3].index('G')]) < 6:
            print("free space is {0} :: not enough,please take care of it".format(detail_info[3]))
        else:
            print('free space is {0} ::: enough space'.format(detail_info[3]))
        
############################################################################
# script start

password,ips,keyword = load_profile()
print('_*'*10, 'cmd result', '_*'*10)
for ip in ips:
    kws_dict={'password':password,'ip':ip[1],'keyword':keyword}
    get_remote_disk_info(kws_dict)
    print

#get_remote_disk_info({'password':'navici','ip':'172.26.178.104','keyword':'workspace'})
#get_remote_disk_info(kws_dict)

