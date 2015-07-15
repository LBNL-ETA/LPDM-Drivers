from beautifulhue.api import Bridge

# Control functionality of bridge system wrapper to simplify interface
class HueBridge:
    def __init__(self, ip = '192.168.1.2', user_name = 'guest'):
        #New Hue control with ip and user name
        self.ip        = ip
        self.user_name = user
        self.bridge    = Bridge(device={'ip':ip}, user={'name':user_name})
           
    def create_config():
        #ideally this has already been configured 
        "Configures the Hue bridge"
        created = False
        print 'Press the button on the Hue bridge'

        # Looks for hue, continually sending message until successfull
        while not created:
            # Test message to the hue                                                              
            resource = {'user':{'devicetype': 'beautifulhuetest', 'name': user_name}}    
            # Attempt config with message
            response = self.bridge.config.create(resource)['resource']                       
            if 'error' in response[0]:                                                  
                if response[0]['error']['type'] != 101:                        
                    raise RuntimeError('Unhandled error creating configuration on the Hue')                                                           
            else:                                                                       
                created = True                                                          

    def get_system_data():
        "Return a dict object containing system information"
        resource = {'which':'system'}                                                     
        return self.bridge.config.get(resource)['resource']

    def get_new_lights():
        "Returns a dict object containing all newly added hue lights"
        resource = {'which':'new'}
        return self.bridge.light.get(resource)['resource']

    def get_all_lights():
        "Returns a dict object containing all hue lights"
        resource = {'which':'all'}
        return self.bridge.light.get(resource)['resource']

    def get_light(lightIndex):
        "Returns a dict object containing values of particular light"
        resources = {'which':lightIndex}
        return self.bridge.light.get(resource)['resource']

    def find_new_lights():
        "Discovers new lights associated with bridge"
        resource = {'which':'new'}
        return self.bridge.light.find(resource)['resource']   

    def update_light_attributes(whichLights, data):
        "Updates light attributes such as name, etc"
        resource = {
            'which': whichLights,
            # Data is an object in the form {'name', etc}
            'data' : {'attr':data}
        } 
        bridge.light.update(resource)

    def update_light_state(whichLights):
        "Updates light state such as on, brightness, hue, etc"
        resource = {
            'which': whichLights,
            # Data is an object in the form {'on', 'ct', 'bri', etc}
            'data' : {'state':data}
        } 
        bridge.light.update(resource)