from typing import Dict
import os
import toml

default_config = {
    'min_channel_size_sat': -1,  # -1 equals not set
    'allow_tor_only_nodes': True,
    'strict_tor_only_node_check': False
}


class ChannelAcceptorConfig:
    def __init__(self, config=None):
        self.user_config = {}
        if config is not None:
            self.user_config = config
        self.public_config, self.private_config = self.merge_configs(self.user_config)

    def merge_configs(self, config: Dict):
        user_general = config.get('general', {})
        user_public = config.get('public_channels', {})
        user_private = config.get('private_channels', {})

        public_config = {**default_config, **user_general, **user_public}
        private_config = {**default_config, **user_general, **user_private}
        return public_config, private_config

    @classmethod
    def load_from_toml(cls, path) -> 'ChannelAcceptorConfig':
        if os.path.exists(path):
            with open(path) as file:
                config = toml.loads(file.read())
        else:
            config = {}
        return ChannelAcceptorConfig(config)