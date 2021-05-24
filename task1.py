import json
import datetime as dt
import logging
from django.core.serializers.json import DjangoJSONEncoder
import traceback

class Assessment:
    def __init__(self):
        self.key_metrics_path='key_metrics.json'
        self.products_path = 'products.json'
        logging.basicConfig(level=logging.INFO)
        self.logger=logging.getLogger('assessment_logs')
        self.logger.setLevel(logging.INFO)

    def format_key_metrics(self, ):
        try:
            with open(self.key_metrics_path) as f:
                json_data=json.load(f)
        except Exception as ex:
            self.logger.error('Problem opening file. Check file path. '+ str(ex))
            return
        output=[]

        self.logger.info('Creating metrics dynamically')
        #The metrics dict would prove efficient if new key metrics are added
        metrics=[]
        for i,metric in enumerate(json_data['report']['metrics']):
            metrics.append((metric['id'],metric['type']))

        for val in json_data['report']['data']:
            temp={}
            try:
                dt_obj=dt.datetime(year=val['year'],month=val['month'],day=val['day'])
                temp['Date']=dt_obj
            except Exception as ex:
                self.logger.error('Problem creating datetime object. '+ str(ex))
                continue

            for i,metric in enumerate(metrics):
                try:
                    if metric[1]=='number':
                        temp[metric[0]]=float(val['counts'][i])
                    else:
                        temp[metric[0]] = val['counts'][i]
                except Exception as ex:
                    self.logger.error('Problem accessing the record for metrics. ' + str(ex))
                    temp={}
            if len(temp):
                output.append(temp)

        self.logger.info('Key Metric formatting complete')

        print(output)
        with open('key_metric_output.json','w') as f:
            json.dump(output,f, cls=DjangoJSONEncoder)

        return

    '''
    def format_products(self, ):
        self.logger.info("Start execution")
        try:
            with open(self.products_path) as f:
                json_data=json.load(f)
        except Exception as ex:
            self.logger.error('Problem opening file. Check file path. '+ str(ex))
            return
        hierarchy_depth = len(json_data['report']['elements'])
        elements=[]
        for val in json_data['report']['elements']:
            elements.append(val['name'])
        #use stack to go to deapest breakdown

        output=[]
        for packaged_data in json_data['report']['data']:
            temp_hierarchy=[]
            #traverse through all to collect the hierarchies except the last one.
            #for i in range(hierarchy_depth-2):
            #    temp_hierarchy.append(packaged_data['name'])
            try:
                stack=[packaged_data['name']]
                while len(stack):
                    stack_val=stack.pop()
                    stack_val=stack_val.split(':')

                    if len(stack_val)!=hierarchy_depth-1:
                        temp_data = packaged_data
                        temp_data = temp_data['breakdown']
                        print(stack_val, temp_data)
                        print(len(temp_data))
                        while len(temp_data):
                            temp_data_val=temp_data.pop()
                            temp_stackval=stack_val
                            temp_stackval.append(temp_data_val['name'])
                            stack.append(':'.join(temp_stackval))

                    else:
                        temp_dict = {}
                        print('in else: ',temp_data)
                        temp_dict['page_views'] = temp_data['counts'][0]
                        temp_dict['visits'] = temp_data['counts'][1]
                        for i in range(len(stack_val)):
                            temp_dict[elements[i]] = stack_val[i]
                        output.append(temp_dict)

            except Exception as ex:
                self.logger.error("Problem processing data. "+str(ex) + traceback.print_exc())

        print(output)
        with open('products_output.json', 'w') as f:
            json.dump(output, f)
        self.logger.info("Excution complete")


        return
    '''

    def format_products(self, ):

        output=[]
        elements = []

        def flatten(data, name=''):
            try:
                if type(data) is list:
                    i = 0
                    for val in data:
                        if 'breakdown' in val:
                            flatten(val['breakdown'], name + val['name'] + '::')
                        else:
                            out={}

                            temp_name=name+val['name']
                            temp_name = temp_name.split('::')
                            temp_name=list(filter(None, temp_name))
                            #print(temp_name)
                            for i,value in enumerate(temp_name):
                                out[elements[i]]=value
                            out['page_views'] = val['counts'][0]
                            out['visits'] = val['counts'][1]
                            output.append(out)
            except Exception as ex:
                self.logger.error('Problem processing data. '+str(ex)+traceback.print_exc())

        try:
            with open(self.products_path) as f:
                json_data = json.load(f)
        except Exception as ex:
            self.logger.error('Problem opening file. Check file path. ' + str(ex))
            return

        for val in json_data['report']['elements']:
            elements.append(val['name'])

        flatten(json_data['report']['data'])
        print(output)
        with open('products_output.json', 'w') as f:
            json.dump(output, f)
        self.logger.info("Excution complete")
        return output


obj=Assessment()
#obj.format_key_metrics()
obj.format_products()

