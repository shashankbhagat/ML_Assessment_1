import json
import datetime as dt
import logging
from django.core.serializers.json import DjangoJSONEncoder

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

    def format_products(self, ):
        self.logger.info("Start execution")
        try:
            with open(self.products_path) as f:
                json_data=json.load(f)
        except Exception as ex:
            self.logger.error('Problem opening file. Check file path. '+ str(ex))
            return
        hierarchy_depth = len(json_data['report']['elements'])
        #use stack to go to deapest breakdown


        return


obj=Assessment()
obj.format_key_metrics()