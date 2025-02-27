class EV:
    AGENT_URL = None
    CUSTOMER_URL = None
    AGENT_LOGIN = None
    AGENT_PASSWORD = None
    AGENT_ALT_LOGIN = None
    OPERATOR_LOGIN = None
    AGENT_ALT_PASSWORD = None
    OPERATOR_PASSWORD = None
    CUSTOMER_LOGIN = None

    @classmethod
    def update_from_env(cls, env_dict):
        for key, value in env_dict.items():
            if hasattr(cls, key):
                setattr(cls, key, value) 