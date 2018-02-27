import requests
import tarfile
import os

servers = ['Coursera', 'Google_Drive']

server_choice = 'Google_Drive'

if server_choice == 'Google_Drive':
    #url = 'https://doc-04-8c-docs.googleusercontent.com/docs/securesc/jom54uhlm38kbdbc4ieju7iinr3l6rtq/718st97db1d4pbvcq1oo32sbg34i10s0/1517853600000/14245259923038140095/14245259923038140095/1dprlnrrkEW1EFCjH3LT3fAebKli5WT-I?h=00618131565082042131&e=download'

    url = 'https://doc-04-8c-docs.googleusercontent.com/docs/securesc/jom54uhlm38kbdbc4ieju7iinr3l6rtq/m8qs7efhckbcbn5ainae6g76dfdn35jg/1519711200000/14245259923038140095/14245259923038140095/1dprlnrrkEW1EFCjH3LT3fAebKli5WT-I?e=download&h=00618131565082042131&nonce=9hub0pi9eu6jg&user=04550493931720650046&hash=ug8dggfc0mf2basr5famhgfeug5u35rj'
    #params = {'Cookie': 'AUTH_hqnkml8mu55ivs1c2tqkjvtfh1nl4uhg=14245259923038140095|1517832000000|16qdno1t9lu0tj31lptbcbcs5puknlm0'}
    params = {'Cookie': 'AUTH_hqnkml8mu55ivs1c2tqkjvtfh1nl4uhg_nonce=4f5u7k71cns0i'}
    params = {'Cookie': 'AUTH_hqnkml8mu55ivs1c2tqkjvtfh1nl4uhg_nonce=4f5u7k71cns0iNID=123=idYj-LOBoUwhSM4-ICUGAhRpOmw9vKWdc0vnnTyHdG3yWLRBWLE-d6sbF9EVMSswcDB1tk6L5UoKCCnEo_tbKHTJaUWLonKy1UYaRpFaXr1zmUb2yvndUJvVNVlBj7e1'}

    print('Downloading weights.tar')
    # r = requests.get(url, headers = params)
    # print('Extracting weights.tar')
    # with open('weights.tar', 'wb') as f:
    #     for chunk in r.iter_content(chunk_size = 2**20):
    #         f.write(chunk)

    tar = tarfile.open('weights.tar', 'r')
    tar.extractall()
    tar.close()

    # os.remove('weights.tar')
else:
    os.mkdir('weights')
    os.chdir('weights')
    WEIGHTS = [
      'conv1', 'bn1', 'conv2', 'bn2', 'conv3', 'bn3',
      'inception_3a_1x1_conv', 'inception_3a_1x1_bn',
      'inception_3a_pool_conv', 'inception_3a_pool_bn',
      'inception_3a_5x5_conv1', 'inception_3a_5x5_conv2', 'inception_3a_5x5_bn1', 'inception_3a_5x5_bn2',
      'inception_3a_3x3_conv1', 'inception_3a_3x3_conv2', 'inception_3a_3x3_bn1', 'inception_3a_3x3_bn2',
      'inception_3b_3x3_conv1', 'inception_3b_3x3_conv2', 'inception_3b_3x3_bn1', 'inception_3b_3x3_bn2',
      'inception_3b_5x5_conv1', 'inception_3b_5x5_conv2', 'inception_3b_5x5_bn1', 'inception_3b_5x5_bn2',
      'inception_3b_pool_conv', 'inception_3b_pool_bn',
      'inception_3b_1x1_conv', 'inception_3b_1x1_bn',
      'inception_3c_3x3_conv1', 'inception_3c_3x3_conv2', 'inception_3c_3x3_bn1', 'inception_3c_3x3_bn2',
      'inception_3c_5x5_conv1', 'inception_3c_5x5_conv2', 'inception_3c_5x5_bn1', 'inception_3c_5x5_bn2',
      'inception_4a_3x3_conv1', 'inception_4a_3x3_conv2', 'inception_4a_3x3_bn1', 'inception_4a_3x3_bn2',
      'inception_4a_5x5_conv1', 'inception_4a_5x5_conv2', 'inception_4a_5x5_bn1', 'inception_4a_5x5_bn2',
      'inception_4a_pool_conv', 'inception_4a_pool_bn',
      'inception_4a_1x1_conv', 'inception_4a_1x1_bn',
      'inception_4e_3x3_conv1', 'inception_4e_3x3_conv2', 'inception_4e_3x3_bn1', 'inception_4e_3x3_bn2',
      'inception_4e_5x5_conv1', 'inception_4e_5x5_conv2', 'inception_4e_5x5_bn1', 'inception_4e_5x5_bn2',
      'inception_5a_3x3_conv1', 'inception_5a_3x3_conv2', 'inception_5a_3x3_bn1', 'inception_5a_3x3_bn2',
      'inception_5a_pool_conv', 'inception_5a_pool_bn',
      'inception_5a_1x1_conv', 'inception_5a_1x1_bn',
      'inception_5b_3x3_conv1', 'inception_5b_3x3_conv2', 'inception_5b_3x3_bn1', 'inception_5b_3x3_bn2',
      'inception_5b_pool_conv', 'inception_5b_pool_bn',
      'inception_5b_1x1_conv', 'inception_5b_1x1_bn'
    ]
   
    NEW_WEIGHTS = ['dense_b', 'dense_w']    

    for layer_name in WEIGHTS:
        NEW_WEIGHTS.append(layer_name + '_b')
        NEW_WEIGHTS.append(layer_name + '_w')

        if 'bn' in layer_name:
            NEW_WEIGHTS.append(layer_name + '_m')
            NEW_WEIGHTS.append(layer_name + '_v')   

    params = {'Cookie':'jupyter-hub-token-kngzqonpjojizletqbceeg="2|1:0|10:1517821781|40:jupyter-hub-token-kngzqonpjojizletqbceeg|44:Y2Q2MjM4MjBiM2JmNDZmMDkzNWI0YzNiODA5MTMzYWU=|5ab769de058661d35f614c91e384d85246643a7ea97efdfeceaa75a78226aa84"; _xsrf=2|af1e3c79|4846acb1c78b5bfb49597a6b022b8e43|1517071435; AWSALB=iWCwjr3BUjfyAHhp8ff/a//gdAl8R3SWLP8HypvCiBcvGf2c8840DT7da6JQjOyIxGKh1EQ7zGNrNCyQJWJ4Ygl9ceodLBWdxhT2OpEOwHOnzCB3zyht/WWquwKb'}

    base_url = 'https://hub.coursera-notebooks.org/user/kngzqonpjojizletqbceeg/files/week4/Face%20Recognition/weights/'

    for layer_name in NEW_WEIGHTS:
        print(layer_name)
        file_name = layer_name + '.csv'
        r = requests.get(base_url + file_name, headers=params)
        with open(file_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=128):
                f.write(chunk)


	        
