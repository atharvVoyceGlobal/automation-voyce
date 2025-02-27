import os

class EV:
    
    AGENT_URL = os.getenv('AGENT_URL')
    CUSTOMER_URL = os.getenv('CUSTOMER_URL')
    AGENT_LOGIN = os.getenv('AGENT_LOGIN')
    AGENT_PASSWORD = os.getenv('AGENT_PASSWORD')
    AGENT_ALT_LOGIN  = os.getenv('AGENT_ALT_LOGIN')
    OPERATOR_LOGIN = os.getenv('OPERATOR_LOGIN')
    AGENT_ALT_PASSWORD = os.getenv('AGENT_ALT_PASSWORD')
    COPERATOR_PASSWORD = os.getenv('OPERATOR_PASSWORD')
    CUSTOMER_LOGIN = os.getenv('CUSTOMER_LOGIN')
