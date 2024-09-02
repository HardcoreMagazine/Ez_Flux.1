import pathlib
from program.config.common_image_presets import common_presets
from program.config.available_models import available_models
from program.utility.ImageFilenameProvider import get_next_filename
from program.utility.PromptLogProvider import log_call_to_file
from program.utility.AppSettingsProvider import AppSettingsProvider
from program.FluxPipelineProvider import FluxPipelineProvider
from program.FluxConfigurationProvider import FluxConfigurationProvider
from program.FluxImageGeneratorProvider import FluxImageGeneratorProvider

class FluxContoller():
    __sys_prefix: str = 'Ez_Flux.1 >>'
    __usr_prefix: str = 'Ez_Flux.1 <<'
    
    __app_settings_provider: AppSettingsProvider
    
    __flux_pipeline: any
    
    __proj_dir: str 
    __proj_out_img_dir: str
    __proj_out_log_dir: str


    def __init__(self) -> None:
        self.__app_settings_provider = AppSettingsProvider()
        self.__proj_dir = str(pathlib.Path().resolve())
        self.__proj_out_img_dir = f'{self.__proj_dir}\\output\\images\\'
        self.__proj_out_log_dir = f'{self.__proj_dir}\\output\\history\\'

        
    def __begin_img_generation_loop(self, flux_img_gen: FluxImageGeneratorProvider, flux_config: FluxConfigurationProvider) -> None:
        while True:
            print(f'{self.__sys_prefix} Enter your prompt or type "exit" to exit the program')
            
            prompt = input(f'{self.__usr_prefix} ')
            
            if len(prompt) > 1 and not str.isspace(prompt): 
                
                if prompt.strip().lower() == 'exit':
                    break
                
                image = flux_img_gen.generate_image(prompt, flux_config)
                next_full_filename = f'{self.__proj_out_img_dir}{get_next_filename(self.__proj_out_img_dir)}'
                image.save(next_full_filename)
                
                print(f'{self.__sys_prefix} Saved result as "{next_full_filename}"')
                
                if self.__app_settings_provider.settings.getboolean('settings', 'save_prompt_history'):
                    params = f"scale={flux_config.scale}, steps={flux_config.steps}, max_seq_len={flux_config.max_seq_len}"
                    log_call_to_file(self.__proj_out_log_dir, prompt, params, next_full_filename)
            else:
                print(f'{self.__sys_prefix} Bad input, try again')
    
    
    def __display_menu(self):
        pass # TODO
    
    
    def __setup_first_launch(self) -> any:
        model_path: str
        online_mode: bool = True
        auth_token: str = None
        
        print(f'{self.__sys_prefix} First launch condition was detected, program needs to be configured before use')
        
        print(f'{self.__sys_prefix} Do you have Flux.1 model downloaded on a local hard drive? [Y/n]')
        
        user_has_model_locally = input(f'{self.__usr_prefix} ').strip().lower()
        
        if user_has_model_locally == 'n':
            print(f'{self.__sys_prefix} Type model number that needs to be downloaded:\n')
            
            for id, info in available_models.items():
                print(f'[{id}] {info["name"]} -- {info["desc"]}')
            
            sel_mod_id: int

            while True:
                try:
                    usr_in = input(f'{self.__usr_prefix} ').strip()
                    if len(usr_in) == 0:
                        raise Exception()
                    else:
                        sel_mod_id = int(usr_in)
                        if 1 <= sel_mod_id <= len(available_models.items()):
                            break
                        else:
                            raise Exception()
                except Exception:
                    print(f'{self.__sys_prefix} Bad input, try again')
            
            model_path = available_models[sel_mod_id]['name']
            
            print(f'{self.__sys_prefix} Selected model "{model_path}"')

            if sel_mod_id == 2:
                print(f'{self.__sys_prefix} This model requires huggingface user authentication token in order to be downloaded')
                
                try:
                    from program.config.user_secrets import user_secrets

                    if not user_secrets['huggingface_auth_token'] or len(user_secrets['huggingface_auth_token']) == 0:
                        raise Exception()
                    else:
                        auth_token = user_secrets['huggingface_auth_token']

                except Exception: # also handles case when 'user_secrets.py' does not exists
                    print(f'{self.__sys_prefix} The user authentication token is not set or not valid, follow the guide on how to inside README.md file and restart the program')
                    exit(0)
        else:
            online_mode = False
            model_path = input(f'{self.__sys_prefix} Enter full path to the catalog with your model (should contain "model_index.json" symlink): ').replace('/','\\\\').replace('\\', '\\\\')

        print(f'{self.__sys_prefix} Would you like to save all of your prompt history along with call parameters on your local drive? [Y/n]')
        
        log_call_history = input(f'{self.__usr_prefix} ')
        
        if log_call_history.lower() == 'n':
            self.__app_settings_provider.settings['settings']['save_prompt_history'] = str(False)

        self.__app_settings_provider.settings['settings']['model_path'] = model_path
        self.__app_settings_provider.settings['settings']['initilized'] = str(True)
        
        return FluxPipelineProvider(model_path=model_path, online_mode=online_mode, use_optimized_settings=True, auth_token=auth_token).pipeline
    
    
    def __get_user_params(self) -> FluxConfigurationProvider:
        flux_config = FluxConfigurationProvider()

        print(f'{self.__sys_prefix} Description for each parameter is available inside "./program/FluxConfigurationProvider.py" file')
        
        aar_keys_arr = list(common_presets.keys()) # Available Aspect Ratios
        aar_values_str = '   '.join([f'[{i + 1}] {val}' for i, val in enumerate(aar_keys_arr)])
        print(f'{self.__sys_prefix} Type aspect ratio preset number, available aspect ratios (default: {aar_keys_arr.index(flux_config.img_aspect_ratio) + 1}):\n{aar_values_str}')
        
        try:
            r_idx = int(input(f'{self.__usr_prefix} ')) - 1
            flux_config.img_aspect_ratio = aar_keys_arr[r_idx]
        except:
            pass # index out of bounds / failed cast to int -> use default (don't change)
        finally:
            del aar_keys_arr
            del aar_values_str
            print(f'{self.__sys_prefix} Selected aspect ratio: {flux_config.img_aspect_ratio}')
        
        r_keys_arr = list(common_presets[flux_config.img_aspect_ratio].keys())
        r_values_str = '   '.join([f'[{i + 1}] {val}' for i, val in enumerate(r_keys_arr)])
        print(f'{self.__sys_prefix} Type image resolution preset number, available resolutions (default: {r_keys_arr.index(flux_config.img_size) + 1}):\n{r_values_str}')
        
        try:
            r_idx = int(input(f'{self.__usr_prefix} ')) - 1
            flux_config.img_size = r_keys_arr[r_idx]
        except:
            pass # index out of bounds / failed cast to int -> use default (don't change)
        finally:
            del r_keys_arr
            del r_values_str
            print(f'{self.__sys_prefix} Selected image resolution: {flux_config.img_size}')
        
        print(f'{self.__sys_prefix} Type scale factor value (integer or floating-point number) (default: {flux_config.scale}):')
        try:
            scale = float(input(f'{self.__usr_prefix} '))
            flux_config.scale = scale
        except:
            pass # failed cast to float -> use default (don't change)
        finally:
            print(f'{self.__sys_prefix} Selected scale factor: {flux_config.scale}')
        
        print(f'{self.__sys_prefix} Type number of generative steps (integer) (default: {flux_config.steps}):')
        try:
            steps = int(input(f'{self.__usr_prefix} '))
            flux_config.steps = steps
        except:
            pass # failed cast to int -> use default (don't change)
        finally:
            print(f'{self.__sys_prefix} Selected number of steps: {flux_config.steps}')
        
        return flux_config
    
    def run(self) -> None:
        print(f'{self.__sys_prefix} Initializing...')
        
        if not self.__app_settings_provider.settings.getboolean('settings', 'initilized'):
            self.__flux_pipeline = self.__setup_first_launch()
            self.__app_settings_provider.update_config()
        else:
            model_path = self.__app_settings_provider.settings['settings']['model_path']
            self.__flux_pipeline = FluxPipelineProvider(model_path=model_path, use_optimized_settings=True).pipeline
        
        print('\n\n\n') # workaround for some nasty visual bug
        
        flux_config: FluxConfigurationProvider = FluxConfigurationProvider()
        
        print(f'{self.__sys_prefix} Loading default image generator parameters:\n'
              f'\'image_aspect_ratio\' = {flux_config.img_aspect_ratio}\n'
              f'\'image_resolution\' = {flux_config.img_size}\n'
              f'\'scale\' = {flux_config.scale}\n'
              f'\'steps\' = {flux_config.steps}\n')
        
        print(f'{self.__sys_prefix} Would you like to change these parameters before initializing image generator? [y/N]')
        
        change_params = input(f'{self.__usr_prefix} ')
        if change_params.strip().lower() == 'y':
            flux_config = self.__get_user_params()
            print(f'{self.__sys_prefix} Note that these settings are stored in-memory and will be lost on program exit, '
                  f'if you wish to change the defaults - see README.md file')

        flux_img_gen = FluxImageGeneratorProvider(self.__flux_pipeline)
        
        self.__begin_img_generation_loop(flux_img_gen=flux_img_gen, flux_config=flux_config)

