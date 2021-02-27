from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from loguru import logger
from typing import List
import importlib
import os
from pip._internal import main
import toml

saya = Saya.current()
channel = Channel.current()

CONFFILE = "sayaproject.toml"
    
def check_config() -> dict:
    if not os.path.exists(CONFFILE):
        logger.info('未找到配置文件，将自动创建并使用默认配置')
        with open(CONFFILE, 'w+') as f:
            toml.dump({'mods_dir': ['mods'], 'mods': []}, f)
    return toml.load(CONFFILE)
    
def load_mods():
    config = check_config()
    with saya.module_context():
        for dir in config['mods_dir']:
            for mod in os.listdir(dir):
                if mod.startswith('__'):
                    continue
                if os.path.isdir(dir + '.' + mod):
                    saya.require(dir + '.' + mod)
                else:
                    saya.require(dir + '.' + mod[:-3])

        for mod in config['mods']:
            try:
                timp = importlib.import_module(mod)
            except ModuleNotFoundError:
                main.main(['install', mod])
            else:
                del timp
            finally:
                saya.require(mod)
                
load_mods()