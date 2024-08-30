from program.config.available_models import available_models
from program.utility.appsettings_loader import get_config, update_config
from program.image_generator import ImgGenerator

if __name__ == '__main__':
    sys_prefix = 'Ez_Flux.1 >>'
    usr_prefix = 'Ez_Flux.1 <<'
    
    model: str
    online: bool = True
    auth_token: str = None
    
    cfg = get_config()
    
    print(f'{sys_prefix} Initializing...')
    
    if not cfg.getboolean('settings','initilized'):
        print(f'{sys_prefix} First launch condition was detected, program needs to be configured before use')
        print(f'{sys_prefix} Do you have Flux.1 model downloaded on a local hard drive? [Y/n]')
        local_model = input(f'{usr_prefix} ')
        if local_model.lower() == 'n':
            print(f'{sys_prefix} Type model number that needs to be downloaded:\n')
            for id, info in available_models.items():
                print(f'[{id}] {info["name"]} -- {info["desc"]}')
            sel_mod_id: int
            while True:
                try:
                    usr_in = input(f'{usr_prefix} ').replace(' ', '')
                    if len(usr_in) == 0:
                        raise Exception()
                    else:
                        sel_mod_id = int(usr_in)
                        if 1 <= sel_mod_id <= len(available_models.items()):
                            break
                        else:
                            raise Exception()
                except Exception:
                    print(f'{sys_prefix} Bad input, try again')
            
            model = available_models[sel_mod_id]['name']
            
            print(f'{sys_prefix} Selected model "{model}"')

            if sel_mod_id == 2:
                print(f'{sys_prefix} This model requires huggingface user authentication token in order to be downloaded')
                try:
                    from program.config.user_secrets import user_secrets
                    if not user_secrets['huggingface_auth_token'] or len(user_secrets['huggingface_auth_token']) == 0:
                        print(f'{sys_prefix} The user auth token is not set, follow the guide on how to inside README.md file and restart the program')
                        exit(0)
                    else:
                        auth_token = user_secrets['huggingface_auth_token']
                except Exception:
                    print(f'{sys_prefix} The user auth token is not set, follow the guide on how to inside README.md file and restart the program')
                    exit(0)
        else:
            model = input(f'{sys_prefix} Enter full path to the catalog with your model (should contain "model_index.json" symlink): ')
            model = model.replace('/','\\\\').replace('\\', '\\\\')
            online = False
        
        print(f'{sys_prefix} Would you like to save all of your prompt history along with call parameters on your local drive? [Y/n]')
        save_history = input(f'{usr_prefix} ')
        if save_history.lower() == 'n':
            cfg['settings']['save_prompt_history'] = str(False)
        
        cfg['settings']['initilized'] = str(True)
        cfg['settings']['download_path'] = model
        update_config(cfg)
        
        generator = ImgGenerator(cfg, model, online, auth_token)
    else:
        model = cfg['settings']['download_path']
        generator = ImgGenerator(cfg, model, False, None)
    

